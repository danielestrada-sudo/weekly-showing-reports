import fitz  # PyMuPDF
import os
import re
import json

pdf_dir = r'B:\Downloads Compass\Joannas Report 420-427'
results = []

for filename in os.listdir(pdf_dir):
    if not filename.endswith('.pdf'):
        continue
    
    pdf_path = os.path.join(pdf_dir, filename)
    doc = fitz.open(pdf_path)
    
    full_text = ''
    for page in doc:
        full_text += page.get_text()
        
    lines = full_text.split('\n')
    address = lines[0].strip() + ' ' + lines[1].strip()
    
    # Extract Compass Views
    compass_match = re.search(r'(\d[\d,]*)\s*Compass\s+views', full_text, re.IGNORECASE)
    if not compass_match:
         compass_match = re.search(r'Compass\s*\n\s*(\d[\d,]+)', full_text, re.IGNORECASE)
    compass_views = compass_match.group(1).replace(',', '') if compass_match else '0'
    
    # Extract External Views (Zillow, etc)
    external_match = re.search(r'(\d[\d,]*)\s*external\s+views', full_text, re.IGNORECASE)
    if not external_match:
        external_match = re.search(r'External\s*\n\s*(\d[\d,]+)', full_text, re.IGNORECASE)
    external_views = external_match.group(1).replace(',', '') if external_match else '0'
    
    total_online_views = int(compass_views) + int(external_views)
    if total_online_views == 0:
        # fallback
        v_match = re.search(r'Views\s*\n\s*(\d[\d,]+)', full_text, re.IGNORECASE)
        if v_match:
            total_online_views = int(v_match.group(1).replace(',', ''))
    
    results.append({
        'filename': filename,
        'address': address,
        'compass_views': compass_views,
        'external_views': external_views,
        'total_online_views': total_online_views
    })
    doc.close()

print(json.dumps(results, indent=2))
