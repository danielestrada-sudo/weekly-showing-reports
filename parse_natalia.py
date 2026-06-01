import fitz
import sys

doc = fitz.open("natalia_may31.pdf")
text = ""
for page in doc:
    text += page.get_text("text")

print("PDF Extracted Text:")
print(text[:1000])

for line in text.split('\n'):
    if "Last 7 Days" in line or "Listing Views" in line or "Emails" in line:
        print(line.strip())
