import re, os

BASE = r'C:\Users\Daniel Estrada\.gemini\antigravity\scratch\weekly-showing-reports'
AGENT_BASE = os.path.join(BASE, 'agents', 'joanna-jimenez')

def fmt(n):
    return f"{n:,}"

def fix_social(slug, new_last7):
    for base in [BASE, AGENT_BASE]:
        html_path = os.path.join(base, slug, 'index.html')
        if not os.path.exists(html_path):
            continue
        with open(html_path, 'r', encoding='utf-8') as f:
            html = f.read()

        # Read current grand total
        m = re.search(
            r'(Social Media Views.*?last-7">\s*)[^<]+(\s*</div>\s*<div class="grand-total">\s*)([^<]+)(\s*</div>)',
            html, re.DOTALL
        )
        if not m:
            print(f"  {slug} @ {base}: social row NOT FOUND")
            continue

        old_grand_str = m.group(3).strip()
        old_grand = int(old_grand_str.replace(',', ''))
        old_last7_str = m.group(1)

        # We previously applied +222 — compute correct grand total
        corrected_grand = old_grand - 222 + new_last7
        replacement = m.group(1) + f"+{fmt(new_last7)}" + m.group(2) + fmt(corrected_grand) + m.group(4)

        html = re.sub(
            r'(Social Media Views.*?last-7">\s*)[^<]+(\s*</div>\s*<div class="grand-total">\s*)[^<]+(\s*</div>)',
            lambda mo: mo.group(1) + f"+{fmt(new_last7)}" + mo.group(2) + fmt(corrected_grand) + mo.group(3),
            html, flags=re.DOTALL
        )

        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f"  Fixed {base}/{slug}: last7=+{fmt(new_last7)}, grand={fmt(corrected_grand)}")

print("Fixing social media views...")
fix_social('244-biscayne-3702', 1000)
fix_social('763-pennsylvania-avenue-unit-116', 20)
fix_social('6061-collins-avenue-unit-5f', 100)
print("Done.")
