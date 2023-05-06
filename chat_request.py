import openai
import time
from queue import Queue
import threading


class Chat_gpt:

    def __init__(self, api_key, language, model, prompt):
        openai.api_key = api_key
        self.language = language
        self.model = model
        self.prompt = prompt
        self.content_queue = Queue()

        # about threading, if you don't use threading, ignore it.
        self.sem = threading.Semaphore(12)

        # rate limit
        self.rate_limit = False

    # multiple
    def go_thread(self, text, tag_num):
        with self.sem:
            self.process(text, tag_num)

    # single
    def process(self, text, tag_num=0, max_tokens=3000, max_retries=5, retry_delay=5):
        language = self.language
        model = self.model
        retries = 0

        # first find rate limit threading
        first_find_threading_error = False

        while retries < max_retries:
            try:
                response = openai.ChatCompletion.create(
                    model=model,
                    messages=[{"role": "system", "content": "You are an AI assistant."},
                              {"role": "user",
                               "content": f"{self.prompt} Present the answer in {language} Markdown format. Thank you.：\n{text}"}],
                    max_tokens=max_tokens,
                    n=1,
                    temperature=0.5,
                )
                self.content_queue.put((tag_num, response['choices'][0]['message']['content'].strip()))

                self.rate_limit = False
                first_find_threading_error = False

                break
            except openai.error.RateLimitError as e:

                if not self.rate_limit:
                    first_find_threading_error = True
                    self.rate_limit = True
                else:
                    while self.rate_limit and not first_find_threading_error:
                        time.sleep(retry_delay)

                if retries < max_retries - 1:
                    retries += 1
                    time.sleep(retry_delay)
                else:
                    raise e
            except openai.error.InvalidRequestError as e:
                if "maximum context length" in str(e):
                    max_tokens -= 500
                    if max_tokens < 1:
                        print("This page is too long")
                        return "TOO LONG!"
                else:
                    raise e
