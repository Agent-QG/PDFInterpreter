# PDFInterpreter
This is a Python script for parsing PDF files and interpreting and analyzing their text using OpenAI GPT. The script first reads the PDF file, breaking its content down into individual pages. Then, it processes the text of each page, breaking it down into paragraphs. Next, it sends the paragraphs to OpenAI GPT to obtain interpretations and analyses of the text. Finally, it converts the GPT responses to Markdown format and turns them back into PDF files. You can place PDF files you want to parse in the input folder, and the processed PDF files will be saved in the output folder.

这是一个用于解析PDF文件并使用OpenAI GPT进行文本解释和分析的Python脚本。脚本首先读取PDF文件，将其内容分解为单独的页面。然后，对每个页面的文本进行处理，将其分解为段落。接下来，将段落发送到OpenAI GPT以获得对文本的解释和分析。最后，将GPT的响应转换为Markdown格式，并将其转换回PDF文件。您可以在 input 文件夹中放置需要解析的PDF文件，处理后的PDF文件将保存在 output 文件夹中。

## Project Structure

- `input/` - Folder to place your input PDF files.
- `output/` - Folder where the processed PDF files will be saved.
- `main.py` - Main script to run the project.
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
7.  Rename `env.txt` as `.env`
## Usage
1. Copy your PDF files to `input/` folder
2. Start
```shell
python main.py
```
## Read your PDFs
By running PDFReader.html, you can read two PDFs at the same time, which is convenient for comparing PDFs.

## 注意事项/已知限制

- 由于尚未获得GPT-4.0的访问权限，该项目目前无法读取PDF中的图片。会持续关注GPT-4.0的更新，并在获得访问权限后更新项目以支持图片解析。

- 本项目在处理大型PDF文件时可能会遇到性能瓶颈。将继续优化代码以提高处理速度和效率。

## Known Limitations/Notes

- As we currently do not have access to GPT-4.0, this project is unable to read images within PDFs. Will continue to monitor updates on GPT-4.0 and update the project to support image interpretation once access is granted.

- The project may encounter performance bottlenecks when processing large PDF files. Will continue to optimize the code to improve processing speed and efficiency.

