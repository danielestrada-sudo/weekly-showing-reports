import re, os

BASE = r'C:\Users\Daniel Estrada\.gemini\antigravity\scratch\weekly-showing-reports'
AGENT_BASE = os.path.join(BASE, 'agents', 'joanna-jimenez')

slug = '244-biscayne-3702'

for base in [BASE, AGENT_BASE]:
    html_path = os.path.join(base, slug, 'index.html')
    if not os.path.exists(html_path):
        continue
    with open(html_path, 'r', encoding='utf-8') as f:
        html = f.read()

    # Read current showings grand total
    m = re.search(
        r'(Physical Showings.*?last-7">\s*)([^<]+)(\s*</div>\s*<div class="grand-total">\s*)([^<]+)(\s*</div>)',
        html, re.DOTALL
    )
    if m:
        current_last7 = m.group(2).strip()
        current_grand = int(m.group(4).strip().replace(',', ''))
        print(f"{base}/{slug}: last7={current_last7}, grand={current_grand}")

        # Fix: last7 was 1 but should be 0, so grand should be -1
        corrected_grand = current_grand - 1

        html = re.sub(
            r'(Physical Showings.*?last-7">\s*)[^<]+(\s*</div>\s*<div class="grand-total">\s*)[^<]+(\s*</div>)',
            lambda mo: mo.group(1) + '0' + mo.group(2) + f'{corrected_grand:,}' + mo.group(3),
            html, flags=re.DOTALL
        )

        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f"  Fixed -> last7=0, grand={corrected_grand:,}")
    else:
        print(f"  Physical Showings row NOT FOUND in {html_path}")
