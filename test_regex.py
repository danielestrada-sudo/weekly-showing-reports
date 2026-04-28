import fitz
import os
import re

pdf_dir = r'B:\Downloads Compass\Joannas Report 420-427'
for f in os.listdir(pdf_dir):
    if not f.endswith('.pdf'): continue
    doc = fitz.open(os.path.join(pdf_dir, f))
    text = ''.join([p.get_text() for p in doc])
    
    lines = text.split('\n')
    addr = lines[0].strip() + ' ' + lines[1].strip()
    
    # Try old format
    v_match = re.search(r'(\d[\d,]*)\s*total\s+views\s+for\s+your\s+listing', text, re.IGNORECASE)
    views = v_match.group(1).replace(',', '') if v_match else None
    
    if not views:
        # Try new format
        v_match = re.search(r'(\d[\d,]*)\n[\d.%-]+\nOver 7 days\nTotal views for your listing', text, re.IGNORECASE)
        views = v_match.group(1).replace(',', '') if v_match else '0'
        
    print(f"File: {f} | Addr: {addr} | Views: {views}")
