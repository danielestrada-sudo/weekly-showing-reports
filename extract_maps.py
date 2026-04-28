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
                images = page.get_images(full=True)
                for img in images:
                    xref = img[0]
                    pix = fitz.Pixmap(doc, xref)
                    if pix.width > 200 and pix.height > 200:
                        try:
                            # If it's CMYK or similar, we convert. If it's already RGB/Gray, we can just save.
                            if pix.n > 4:
                                pix = fitz.Pixmap(fitz.csRGB, pix)
                            out_path = os.path.join(os.getcwd(), slug, 'property_views_map_clean.png')
                            pix.save(out_path)
                            print(f"Saved map for {slug} ({pix.width}x{pix.height})")
                        except Exception as e:
                            print(f"Error saving {slug}: {e}")
                        break
