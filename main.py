import os
import re
import time
import PyPDF2
import markdown2
import openai
import pdfkit
from tqdm import tqdm
from dotenv import load_dotenv
from multiprocessing import Pool, cpu_count
from tqdm.auto import tqdm


load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
wkhtmltopdf_path = os.getenv("WKHTMLTOPDFPATH")

def read_pdf(file_path):
    with open(file_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        pages = []
        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            content = page.extract_text()
            pages.append(content)

    return pages


def chatgpt_interpret(text, max_tokens=3000, max_retries=5, retry_delay=5):
    language = os.getenv("LANGUAGE")
    model = os.getenv("MODEL")
    retries = 0
    while retries < max_retries:
        try:
            response = openai.ChatCompletion.create(
                model=model,
                messages=[{"role": "system", "content": "You are an AI assistant."},
                          {"role": "user",
                           "content": f"Please explain and analyze the following content in {language} and answer in Markdown：\n{text}"}],
                max_tokens=max_tokens,
                n=1,
                temperature=0.5,
            )
            return response['choices'][0]['message']['content'].strip()
        except openai.error.RateLimitError as e:
            if retries < max_retries - 1:
                retries += 1
                time.sleep(retry_delay)
            else:
                raise e
        except openai.error.InvalidRequestError as e:
            if "maximum context length" in str(e):
                max_tokens -= 500
                if max_tokens < 1:
                    print("max tokens is"+str(max_tokens))
                    return "TOO LONG!"
            else:
                raise e



def split_text(text, max_tokens):
    sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', text)
    chunks = []
    current_chunk = []

    for sentence in sentences:
        if len(current_chunk) + len(sentence.split()) <= max_tokens:
            current_chunk.append(sentence)
        else:
            chunks.append(' '.join(current_chunk))
            current_chunk = [sentence]

    if current_chunk:
        chunks.append(' '.join(current_chunk))

    return chunks

def fix_markdown_issues(text):
    text = text.replace("--", "—")
    text = re.sub(r'(?<!\\)(~~)', r'\\\1', text)

    return text


def markdown_to_pdf(markdown_text, output_path,wkhtmltopdf_path):
    html = markdown2.markdown(markdown_text)
    options = {
        'encoding': "UTF-8"
    }
    if wkhtmltopdf_path:
        config = pdfkit.configuration(wkhtmltopdf=wkhtmltopdf_path)
        pdfkit.from_string(html, output_path, options=options, configuration=config)
    else:
        pdfkit.from_string(html, output_path, options=options)


def process_pdf(filename, input_folder, output_folder):
    if filename.endswith(".pdf"):
        pdf_path = os.path.join(input_folder, filename)
        output_pdf = os.path.join(
            output_folder, os.path.splitext(filename)[0] + "_explained.pdf"
        )

        pdf_contents = read_pdf(pdf_path)
        interpretations = []

        for index, content in enumerate(
                tqdm(pdf_contents, desc=f"Processing {filename} ")
        ):
            interpretation_page = []
            paragraphs = content.split("\n\n")
            for paragraph in paragraphs:
                if len(paragraph.strip()) > 0:
                    sub_paragraphs = split_text(paragraph, 3000)
                    for sub_paragraph in sub_paragraphs:
                        interpretation = chatgpt_interpret(sub_paragraph)
                        if interpretation == "TOO LONG!":
                            print(f"Page {index + 1} is too LONG!")
                            break
                        interpretation = fix_markdown_issues(interpretation)
                        interpretation_page.append(interpretation)

            interpretation_page.append(f"[p{index + 1}]")

            interpretations.append("\n\n".join(interpretation_page))

        markdown_interpretations = "\n\n---\n\n".join(interpretations)
        markdown_to_pdf(markdown_interpretations, output_pdf,wkhtmltopdf_path)

def wrapped_process_pdf(args):
    return process_pdf(*args)

def main():
    input_folder = "input"
    output_folder = "output"

    filenames = [filename for filename in os.listdir(input_folder) if filename.endswith(".pdf")]

    num_workers = min(cpu_count(), len(filenames),5)

    with Pool(num_workers) as p:
        p.map(wrapped_process_pdf, [(filename, input_folder, output_folder) for filename in filenames])

if __name__ == "__main__":
    main()
