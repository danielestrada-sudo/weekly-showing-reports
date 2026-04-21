import fitz  # PyMuPDF
import os
import re

pdf_dir = 'progress_reports'
output_dir = 'visitor_maps'
os.makedirs(output_dir, exist_ok=True)

results = {}

for filename in sorted(os.listdir(pdf_dir)):
    if not filename.endswith('.pdf'):
        continue
    
    pdf_path = os.path.join(pdf_dir, filename)
    doc = fitz.open(pdf_path)
    
    full_text = ''
    for page in doc:
        full_text += page.get_text()
    
    # Extract property address - usually first line after "Progress report:"
    address_match = re.search(r'Progress report[:\s]+(.+?)(?:\n|$)', full_text, re.IGNORECASE)
    address = address_match.group(1).strip() if address_match else 'Unknown'
    
    # Extract total views for last 7 days
    # Common patterns: "X views" near "last 7 days" or "this week"
    views_match = re.search(r'(\d[\d,]*)\s*(?:total\s+)?views?\s+(?:for\s+your\s+listing|this\s+week|last\s+7)', full_text, re.IGNORECASE)
    if not views_match:
        # Try alternative: look for a standalone number near "Views"
        views_match = re.search(r'Views\s*\n\s*(\d[\d,]+)', full_text, re.IGNORECASE)
    if not views_match:
        views_match = re.search(r'(\d[\d,]+)\s*\n\s*Views', full_text, re.IGNORECASE)
    
    views = views_match.group(1).replace(',', '') if views_match else 'N/A'
    
    print(f"\n{'='*60}")
    print(f"File: {filename}")
    print(f"Address: {address}")
    print(f"Views (last 7 days): {views}")
    print(f"\n--- FULL TEXT (first 1500 chars) ---")
    print(full_text[:1500])
    
    results[filename] = {'address': address, 'views': views}
    
    # Extract visitor map image (usually on page 2 or 3)
    for page_num, page in enumerate(doc):
        images = page.get_images(full=True)
        page_text = page.get_text()
        
        # Look for the map page - it usually mentions "Views by" or "Where your"
        if 'views by' in page_text.lower() or 'where your' in page_text.lower() or 'city' in page_text.lower():
            # Save this page as image
            mat = fitz.Matrix(2, 2)  # 2x zoom for clarity
            pix = page.get_pixmap(matrix=mat)
            
            # Create a clean filename from the address
            clean_addr = re.sub(r'[^\w\s]', '', address).strip().replace(' ', '_')[:40]
            map_filename = f"{output_dir}/map_{clean_addr}.png"
            pix.save(map_filename)
            print(f"  -> Saved map: {map_filename}")
            results[filename]['map'] = map_filename
            break

print("\n\n=== SUMMARY ===")
for f, data in results.items():
    print(f"{data['address']}: {data['views']} views | map: {data.get('map', 'not found')}")
