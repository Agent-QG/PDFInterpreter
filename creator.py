import threading
from utils import read_pdf, split_text, fix_markdown_issues
from tqdm import tqdm
import os

class Creator:

    def __init__(self, file_path, chat_gpt):
        self.file_path = file_path
        self.file_name = os.path.basename(file_path)  # Add this line
        self.chat_gpt = chat_gpt


    def process(self):
        pdf_contents = read_pdf(self.file_path)

        # for organize report order
        sequential_mapping = {}
        result_list = []

        target_num = 0

        for page_num, page_content in enumerate(pdf_contents):
            # every request target number

            sequential_mapping[page_num] = []

            # split to paragraphs
            paragraphs = page_content.split("\n\n")

            for paragraph in paragraphs:
                # judge whether this paragraph efficient
                if len(paragraph.strip()) > 0:

                    # split paragraph to sub_paragraphs to avoid too long
                    sub_paragraphs = split_text(paragraph, 3000)

                    for sub_paragraph in sub_paragraphs:
                        t = threading.Thread(target=self.chat_gpt.go_thread, args=(sub_paragraph, target_num,))
                        t.start()
                        sequential_mapping[page_num].append(target_num)
                        result_list.append(None)
                        target_num += 1

        done_request = 0
        with tqdm(total=target_num, position=0, desc=self.file_name) as pbar:
            while done_request != target_num:
                while not self.chat_gpt.content_queue.empty():
                    pos, content = self.chat_gpt.content_queue.get()
                    content = fix_markdown_issues(content)
                    result_list[pos] = content
                    done_request += 1
                    pbar.update(1)

        parsed_pdf = []

        for page_num in range(len(pdf_contents)):
            parsed_page = []
            for index in sequential_mapping[page_num]:
                parsed_page.append(result_list[index])
            parsed_page.append(f"[p{page_num + 1}]")
            parsed_pdf.append("\n\n".join(parsed_page))

        return parsed_pdf
