import subprocess, re

BASE = r'C:\Users\Daniel Estrada\.gemini\antigravity\scratch\weekly-showing-reports'

# Check DOM in the commit BEFORE baa3c23 (i.e., c19cca6 which is baa3c23~1)
slugs = [
    '234-washington-ave',
    '7334-harding-unit-6',
    '320-85-st-15',
    '8000-harding-avenue-unit-2b',
    '1710-nw-106-terr',
    '763-pennsylvania-avenue-unit-116',
    '6061-collins-avenue-unit-5f',
    '17301-biscayne-boulevard-unit-1401',
    '10449-sw-78th-st',
    '244-biscayne-3702',
    '1376-sw-4th-st-7',
    '1945-s-ocean-dr-unit-m2',
    '88-sw-7-st-1012',
]

print("DOM values BEFORE May 25-31 update (from baa3c23~1):\n")
for slug in slugs:
    try:
        result = subprocess.run(
            ['git', 'show', f'baa3c23~1:{slug}/index.html'],
            cwd=BASE, capture_output=True, text=True, encoding='utf-8'
        )
        html = result.stdout
        if not html:
            # try agents path
            result = subprocess.run(
                ['git', 'show', f'baa3c23~1:agents/joanna-jimenez/{slug}/index.html'],
                cwd=BASE, capture_output=True, text=True, encoding='utf-8'
            )
            html = result.stdout
        m = re.search(r'Days on Market</div>\s*<div class="card-value[^"]*">\s*([\d,]+)', html)
        dom = m.group(1).strip() if m else 'NOT FOUND'
        print(f"  {slug}: DOM was {dom}")
    except Exception as e:
        print(f"  {slug}: ERROR - {e}")
