import os
import re
import time
import PyPDF2
import markdown2
import openai
import pdfkit
from tqdm import tqdm
from dotenv import load_dotenv


load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")


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
                model = model,
                messages=[{"role": "system", "content": "You are an AI assistant."},
                          {"role": "user",
                           "content": f"Please use Markdown syntax to explain and analyze the following content in {language}：\n{text}"}],
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


def markdown_to_pdf(markdown_text, output_path):
    html = markdown2.markdown(markdown_text)
    options = {
        'encoding': "UTF-8"
    }
    pdfkit.from_string(html, output_path, options=options)


def main():
    input_folder = "input"
    output_folder = "output"

    for filename in os.listdir(input_folder):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(input_folder, filename)
            output_pdf = os.path.join(output_folder, os.path.splitext(filename)[0] + "_explained.pdf")

            pdf_contents = read_pdf(pdf_path)
            interpretations = []

            for index, content in enumerate(tqdm(pdf_contents, desc=f"Processing {filename} ")):
                interpretation_page = []
                paragraphs = content.split('\n\n')
                for paragraph in paragraphs:
                    if len(paragraph.strip()) > 0:
                        sub_paragraphs = split_text(paragraph, 3000)
                        for sub_paragraph in sub_paragraphs:
                            interpretation = chatgpt_interpret(sub_paragraph)
                            interpretation_page.append(interpretation)

                interpretation_page.append(f"[p{index + 1}]")

                interpretations.append("\n\n".join(interpretation_page))

            markdown_interpretations = "\n\n---\n\n".join(interpretations)
            markdown_to_pdf(markdown_interpretations, output_pdf)


if __name__ == "__main__":
    main()
