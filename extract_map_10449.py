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
    if '10449' in addr: slug = "10449-sw-78th-st"
    
    if slug:
        for page in doc:
            if 'Views By City' in page.get_text():
                mat = fitz.Matrix(150 / 72, 150 / 72)
                pix = page.get_pixmap(matrix=mat)
                out_path = os.path.join(os.getcwd(), slug, 'property_views_map_clean.png')
                if os.path.exists(os.path.join(os.getcwd(), slug)):
                    pix.save(out_path)
                    print(f"Saved rendered page for {slug}")
                break
