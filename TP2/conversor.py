import re
import sys

header = re.compile(r"#\w")
bold = re.compile(r"\*{2}\w*\*{2}")
italic = re.compile(r"\*\*\w*\*\*")
numlist = re.compile(r"^\d\.[\w ,.]*")
link = re.compile(r"(\[.*\])(\([\w\/:\.]*\))")
image = re.compile(r"(.*)(!\[.*\])(\([\w\/:\.]*\))")

def markdown_to_html(text):
    linhas = text.split("\n")
    return text

def main():
    if len(sys.argv) != 3:
        print("Uso: python main.py <input.md> <output.html>")
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