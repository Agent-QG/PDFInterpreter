import openai
import time
from queue import Queue
import threading


class Chat_gpt:

    def __init__(self, api_key, language, model):
        openai.api_key = api_key
        self.language = language
        self.model = model
        self.content_queue = Queue()

        # about threading, if you don't use threading, ignore it.
        self.sem = threading.Semaphore(20)

    # multiple
    def go_thread(self, text, tag_num):
        with self.sem:
            self.process(text, tag_num)

    # single
    def process(self, text, tag_num=0, max_tokens=3000, max_retries=5, retry_delay=5):
        language = self.language
        model = self.model
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
                self.content_queue.put((tag_num, response['choices'][0]['message']['content'].strip()))
                break
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
                        print("max tokens is" + str(max_tokens))
                        return "TOO LONG!"
                else:
                    raise e
