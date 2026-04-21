import fitz  # PyMuPDF
import os
import re

pdf_dir = 'progress_reports'
output_dir = 'visitor_maps'
os.makedirs(output_dir, exist_ok=True)

# Confirmed view counts from reading the PDF text output above
view_data = {}

for filename in sorted(os.listdir(pdf_dir)):
    if not filename.endswith('.pdf'):
        continue

    pdf_path = os.path.join(pdf_dir, filename)
    doc = fitz.open(pdf_path)

    full_text = ''
    for page in doc:
        full_text += page.get_text()

    # Extract address from first page
    first_page_text = doc[0].get_text()
    lines = [l.strip() for l in first_page_text.split('\n') if l.strip()]
    address_lines = []
    for i, line in enumerate(lines):
        if re.search(r'\d{4}|\d{3,4}\s+[A-Z]', line):
            address_lines.append(line)
            if i + 1 < len(lines) and lines[i+1].lower().startswith('unit'):
                address_lines.append(lines[i+1])
            break
    address = ' '.join(address_lines) if address_lines else lines[0] if lines else 'Unknown'

    # Extract "Total views for your listing"
    views_match = re.search(r'(\d+)\s*\n[\d.]+%?\s*\nOver 7 days\s*\nTotal views for your listing', full_text, re.IGNORECASE)
    if not views_match:
        # Try alternate
        views_match = re.search(r'(\d+)\n[\d.]+%\nOver 7 days\nTotal views', full_text)
    views = views_match.group(1) if views_match else None

    # Save visitor map page (the "Views By City" page as a screenshot)
    map_saved = None
    for page_num, page in enumerate(doc):
        page_text = page.get_text()
        if 'Views By City' in page_text or 'Views by City' in page_text:
            mat = fitz.Matrix(2, 2)
            pix = page.get_pixmap(matrix=mat)
            # Create slug from address
            clean_addr = re.sub(r'[^\w]', '_', address.lower())[:50]
            map_filename = f"{output_dir}/{clean_addr}.png"
            pix.save(map_filename)
            map_saved = map_filename
            break

    print(f"FILE: {filename}")
    print(f"  Address: {address}")
    print(f"  Views (last 7 days): {views}")
    print(f"  Map saved: {map_saved}")
    view_data[address] = {'views': views, 'map': map_saved}
    print()

print("=== FINAL SUMMARY ===")
for addr, data in view_data.items():
    print(f"  {addr}: {data['views']} views | {data['map']}")
