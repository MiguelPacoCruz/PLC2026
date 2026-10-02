import re
import sys

bold = re.compile(r"\*{2}(.*?)\*{2}")
italic = re.compile(r"\*{1}(.*?)\*{1}")
link = re.compile(r"([^!])\[(?P<texto>.*)\]\((?P<url>[\w\/:\.]*)\)")
image = re.compile(r"!\[(?P<texto>.*)\]\((?P<url>[\w\/:\.]*)\)")
header = re.compile(r"#\w")
numlist = re.compile(r"^\d\.[\w ,.]*")

def markdown_to_html(text):
    text = re.sub(bold,r"<b>\1</b>",text)
    text = re.sub(italic,r"<i>\1</i>",text)
    text = re.sub(link,r'\1<a href="\g<url>">\g<texto></a>',text)
    text = re.sub(image,r'<img src="\g<url>" alt="\g<texto>"/>',text)

    if re.match(r'^1\. (.*)$',text,re.MULTILINE)is not None:
        m = True
        text = re.sub(r'1\. (.*)',r'<ol>\n<li>\1</li>',text)
        i = 2
        while (m != None):
            m = re.match(rf'{i}\.(.*)',text)
            text = re.sub(rf'{i}\. (.*)',r'<li>\1</li>',text)
            i += 1
        text = re.sub(rf'{i}\. (.*)',r'<li>\1</li>\n</ol>',text)

    return text

def main():
    if len(sys.argv) != 3:
        #print("Uso: python main.py <input.md> <output.html>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    with open(input_file, "r", encoding="utf-8") as f:
        markdown = f.read()

    html = markdown_to_html(markdown)

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(html)


if __name__ == "__main__":
    main()