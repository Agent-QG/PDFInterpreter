# PDFInterpreter
This is a Python script for parsing PDF files and interpreting and analyzing their text using OpenAI GPT. The script first reads the PDF file, breaking its content down into individual pages. Then, it processes the text of each page, breaking it down into paragraphs. Next, it sends the paragraphs to OpenAI GPT to obtain interpretations and analyses of the text. Finally, it converts the GPT responses to Markdown format and turns them back into PDF files. You can place PDF files you want to parse in the input folder, and the processed PDF files will be saved in the output folder. This version of the script employs multithreading to speed up the processing of a single PDF file.

这是一个用于解析PDF文件并使用OpenAI GPT进行文本解释和分析的Python脚本。脚本首先读取PDF文件，将其内容分解为单独的页面。然后，对每个页面的文本进行处理，将其分解为段落。接下来，将段落发送到OpenAI GPT以获得对文本的解释和分析。最后，将GPT的响应转换为Markdown格式，并将其转换回PDF文件。您可以在 input 文件夹中放置需要解析的PDF文件，处理后的PDF文件将保存在 output 文件夹中。此版本的脚本采用多线程来加快单个PDF文件的处理速度。

## Project Structure

- `input/` - Folder to place your input PDF files.
- `output/` - Folder where the processed PDF files will be saved.
- `main.py` - Main script to run the project.
- `chat_request.py` - Contains the Chat_gpt class, responsible for making API requests to the GPT model and managing concurrent threads for faster PDF processing.
- `creator.py` - Contains the Creator class, responsible for processing a single PDF file by extracting text, splitting it into chunks, and utilizing the Chat_gpt class to obtain explanations and analysis.
- `utils.py` - A utility file containing various helper functions such as reading PDF files, splitting text, fixing Markdown issues, and converting Markdown to PDF.
- `.env` - File to store environment variables such as API key, language, GPT model, and wkhtmltopdf path.
- `PDFReader.html` - A PDF reader to read two PDFs at the same time.

## Set Up
1. Download the repository
2. Install the requirements
```shell
pip install -r requirements.txt
```
3.  Install wkhtmltopdf

- Go to https://wkhtmltopdf.org/downloads.html to download `wkhtmltopdf`

5.  Change your openai api key in env.txt (You can get your key on https://platform.openai.com/account/api-keys)
6.  Change your target language and model in env.txt (Chinese and gpt-3.5-turbo are set as default)
7.  Rename the file 'env.txt' to '.env'
## Usage
1. Copy your PDF files to `input/` folder
2. Start
```shell
python main.py
```
## Read your PDFs
By running PDFReader.html, you can read two PDFs at the same time, which is convenient for comparing PDFs.

## General errors
- Please make sure you have installed `wkhtmltopdf`
- If you encounter a wkhtmltopdf error, please add the path to your wkhtmltopdf path in the .env file
- For MacOS, the default path is `/usr/local/bin/wkhtmltopdf`. You can get your wkhtmltopdf path by 
```shell
which wkhtmltopdf
```
- For Windows, the default path is `C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe`. You can get your wkhtmltopdf path by 
```shell
dir /s /b C:\ | findstr /i wkhtmltopdf.exe
```
(I assume you installed it in C:\)
- If you still encounter an error with wkhtmltopdf, consider granting administrator privileges to both your wkhtmltopdf and the project.
- If you encounter any other issues, please feel free to open an issue on GitHub or contact me directly at my.qgong@gmail.com.

## 未来发展
- 适配GPT-4模型和图片读取功能：我们正在努力将GPT-4模型整合到项目中以提高解析和生成结果的质量。
- 开发网页版：我们计划开发一个网页版并且添加更丰富的功能，让用户能够更方便地在线使用本工具。

## Future Development

- Adapting to GPT-4 Model and Image Reading Capability: We are working on integrating the GPT-4 model into the project to improve the quality of parsing and generated results.
- Developing a Web Version: We plan to develop a web-based version of this tool and add more functions to make it more accessible and convenient for users to use online.
