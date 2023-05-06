import re
import PyPDF2
import markdown2
import pdfkit

def read_pdf(file_path):
    with open(file_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        pages = []
        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            content = page.extract_text()
            content = re.sub(r'\s*\d+\s*$', '', content)

            pages.append(content)

    return pages



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
