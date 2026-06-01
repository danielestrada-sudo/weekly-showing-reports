import re, os

BASE = r'C:\Users\Daniel Estrada\.gemini\antigravity\scratch\weekly-showing-reports'
AGENT_BASE = os.path.join(BASE, 'agents', 'joanna-jimenez')

# Redfin confirmed DOM as of June 1, 2026
# slug -> correct DOM
CORRECT_DOM = {
    '244-biscayne-3702':               40,   # was 13 (stuck forever)
    '7334-harding-unit-6':            148,   # was 98 (Redfin ~148)
    '8000-harding-avenue-unit-2b':     17,   # was 98 (relisted May 15)
    '1710-nw-106-terr':                81,   # was 55 (pending ~81 days)
    '763-pennsylvania-avenue-unit-116':134,  # was 135 (minor)
    '6061-collins-avenue-unit-5f':     51,   # was 54 (minor)
    '1376-sw-4th-st-7':               64,   # was 69 (minor)
    '1945-s-ocean-dr-unit-m2':        46,   # was 48 (minor)
    '88-sw-7-st-1012':                26,   # was 29 (minor)
}

def fix_dom(slug, correct_dom):
    fixed = 0
    for base in [BASE, AGENT_BASE]:
        html_path = os.path.join(base, slug, 'index.html')
        if not os.path.exists(html_path):
            continue
        with open(html_path, 'r', encoding='utf-8') as f:
            html = f.read()

        # Fix the DOM card value
        new_html = re.sub(
            r'(Days on Market</div>\s*<div class="card-value[^"]*">\s*)[\d,]+(\s*)',
            lambda m: m.group(1) + str(correct_dom) + m.group(2),
            html
        )

        if new_html == html:
            print(f"  WARNING: No change made for {base}/{slug}")
        else:
            with open(html_path, 'w', encoding='utf-8') as f:
                f.write(new_html)
            fixed += 1

    return fixed

print("=== Fixing Days on Market for all properties ===\n")
for slug, dom in CORRECT_DOM.items():
    count = fix_dom(slug, dom)
    print(f"  {slug}: DOM set to {dom} ({count} files updated)")

print("\nAll DOM values fixed.")
