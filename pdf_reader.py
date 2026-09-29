from pypdf import PdfReader

file = input("PDF file: ")

reader = PdfReader(file)

for page in reader.pages:
    print(page.extract_text())
