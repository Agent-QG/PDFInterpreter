import os

from chat_request import Chat_gpt
from dotenv import load_dotenv

from creator import Creator
from utils import markdown_to_pdf

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
language = os.getenv("LANGUAGE")
model = os.getenv("MODEL")
wkhtmltopdf_path = os.getenv("WKHTMLTOPDFPATH")


def main():
    input_folder = "input"
    output_folder = "output"
    filenames = [filename for filename in os.listdir(input_folder) if filename.endswith(".pdf")]
    chat_gpt = Chat_gpt(api_key=api_key, language=language, model=model)
    for file in filenames:
        pdf_path = os.path.join(input_folder, file)
        output_pdf = os.path.join(
            output_folder, os.path.splitext(file)[0] + "_explained.pdf"
        )
        creator = Creator(pdf_path, chat_gpt)
        parsed_list = creator.process()
        markdown_interpretations = "\n\n---\n\n".join(parsed_list)
        markdown_to_pdf(markdown_interpretations, output_pdf, wkhtmltopdf_path)


if __name__ == "__main__":
    main()
