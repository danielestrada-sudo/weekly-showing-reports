import fitz, os, re

pdf_dir = r'B:\Downloads Compass\Joannas Report 420-427'
for f in os.listdir(pdf_dir):
    if not f.endswith('.pdf'): continue
    doc = fitz.open(os.path.join(pdf_dir, f))
    text = doc[0].get_text()
    lines = text.split('\n')
    addr = lines[0].strip() + ' ' + lines[1].strip()
    
    views_match = re.search(r'(\d[\d,]*)\s*total\s+views\s+for\s+your\s+listing\s+last\s+7\s+days', text, re.IGNORECASE)
    if not views_match:
        views_match = re.search(r'Views\s*\n\s*(\d[\d,]+)', text, re.IGNORECASE)
    views = views_match.group(1).replace(',', '') if views_match else '0'
    print(f"File: {f} | Address: {addr} | Views: {views}")
