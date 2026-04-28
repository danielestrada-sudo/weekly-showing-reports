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
    
    # Extract address
    # Usually "Progress report: [Address]"
    address_match = re.search(r'Progress report[:\s]+(.+?)(?:\n|$)', full_text, re.IGNORECASE)
    address = address_match.group(1).strip() if address_match else 'Unknown'
    
    # Extract Views (Last 7 Days)
    # Look for the "Views" section and the number below it or "X total views for your listing last 7 days"
    views_match = re.search(r'(\d[\d,]*)\s*total\s+views\s+for\s+your\s+listing\s+last\s+7\s+days', full_text, re.IGNORECASE)
    if not views_match:
        views_match = re.search(r'Views\s*\n\s*(\d[\d,]+)', full_text, re.IGNORECASE)
    
    views = views_match.group(1).replace(',', '') if views_match else '0'
    
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
    
    # Extract Saves
    saves_match = re.search(r'(\d[\d,]*)\s*saves\s+for\s+your\s+listing\s+last\s+7\s+days', full_text, re.IGNORECASE)
    if not saves_match:
        # Sometimes it's just "X Saves" in the summary
        saves_match = re.search(r'Saves\s*\n\s*(\d[\d,]+)', full_text, re.IGNORECASE)
    
    saves = saves_match.group(1).replace(',', '') if saves_match else '0'
    
    results.append({
        'filename': filename,
        'address': address,
        'total_views': views,
        'compass_views': compass_views,
        'external_views': external_views,
        'saves': saves
    })
    doc.close()

print(json.dumps(results, indent=2))
