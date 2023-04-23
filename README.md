# PDFInterpreter
This is a Python script for parsing PDF files and interpreting and analyzing their text using OpenAI GPT. The script first reads the PDF file, breaking its content down into individual pages. Then, it processes the text of each page, breaking it down into paragraphs. Next, it sends the paragraphs to OpenAI GPT to obtain interpretations and analyses of the text. Finally, it converts the GPT responses to Markdown format and turns them back into PDF files. You can place PDF files you want to parse in the input folder, and the processed PDF files will be saved in the output folder.

这是一个用于解析PDF文件并使用OpenAI GPT进行文本解释和分析的Python脚本。脚本首先读取PDF文件，将其内容分解为单独的页面。然后，对每个页面的文本进行处理，将其分解为段落。接下来，将段落发送到OpenAI GPT以获得对文本的解释和分析。最后，将GPT的响应转换为Markdown格式，并将其转换回PDF文件。您可以在 input 文件夹中放置需要解析的PDF文件，处理后的PDF文件将保存在 output 文件夹中。

## Set Up
1. Download the repository
2. Install the requirements
```shell
pip install requirements.txt
```
3.  Change your openai api key in env.txt
4.  Change your target language and model in env.txt (Chinese and gpt-3.5-turbo are set as default
5.  rename env.txt as .env
## Usage
1. Copy your PDF files to input folder
2. Start by ```shell
python main.py
```
