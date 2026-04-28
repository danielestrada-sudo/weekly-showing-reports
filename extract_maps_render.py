import fitz
import os

pdf_dir = r'B:\Downloads Compass\Joannas Report 420-427'
for f in os.listdir(pdf_dir):
    if not f.endswith('.pdf'): continue
    doc = fitz.open(os.path.join(pdf_dir, f))
    text = doc[0].get_text()
    lines = text.split('\n')
    addr = lines[0].strip() + ' ' + lines[1].strip()
    
    slug = None
    if 'Washington' in addr: slug = "234-washington-ave"
    elif '7334 Harding' in addr: slug = "7334-harding-unit-6"
    elif '320 85' in addr: slug = "320-85-st-15"
    elif '8000 Harding' in addr: slug = "8000-harding-avenue-unit-2b"
    elif '1710' in addr: slug = "1710-nw-106-terr"
    elif '763 Pennsylvania' in addr: slug = "763-pennsylvania-avenue-unit-116"
    elif '6061' in addr: slug = "6061-collins-avenue-unit-5f"
    elif '17301' in addr: slug = "17301-biscayne-boulevard-unit-1401"
    
    if slug:
        for page in doc:
            if 'Views By City' in page.get_text():
                # Render the page
                mat = fitz.Matrix(150 / 72, 150 / 72)  # 150 DPI
                pix = page.get_pixmap(matrix=mat)
                out_path = os.path.join(os.getcwd(), slug, 'property_views_map_clean.png')
                if os.path.exists(os.path.join(os.getcwd(), slug)):
                    pix.save(out_path)
                    print(f"Saved rendered page for {slug}")
                break
