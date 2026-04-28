import fitz
import os

pdf_path = r'B:\Downloads Compass\Joannas Report 420-427\listing-insights-report-1175185e-43cf-45c9-b500-c05ac0c030a0-2026-04-27.pdf'
doc = fitz.open(pdf_path)
full_text = ''
for page in doc:
    full_text += f"--- PAGE {page.number} ---\n"
    full_text += page.get_text()
print(full_text)
doc.close()
