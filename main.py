import os

from chat_request import Chat_gpt
from dotenv import load_dotenv

from creator import Creator
from utils import markdown_to_pdf

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
language = os.getenv("LANGUAGE")
model = os.getenv("MODEL")
wkhtmltopdf_path = os.getenv(r"WKHTMLTOPDFPATH")
prompt=os.getenv(r"Prompt")

def main():
    input_folder = "input"
    output_folder = "output"

    for root, _, filenames in os.walk(input_folder):
        for filename in filenames:
            if filename.endswith(".pdf"):
                pdf_path = os.path.join(root, filename)
                relative_path = os.path.relpath(root, input_folder)
                output_subfolder = os.path.join(output_folder, relative_path)

                os.makedirs(output_subfolder, exist_ok=True)

                output_pdf = os.path.join(
                    output_subfolder, os.path.splitext(filename)[0] + "_explained.pdf"
                )
                chat_gpt = Chat_gpt(api_key=api_key, language=language, model=model, prompt=prompt)
                creator = Creator(pdf_path, chat_gpt)
                parsed_list = creator.process()
                markdown_interpretations = "\n\n---\n\n".join(parsed_list)
                markdown_to_pdf(markdown_interpretations, output_pdf, wkhtmltopdf_path)

if __name__ == "__main__":
    main()
