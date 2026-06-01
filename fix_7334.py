import re, os

BASE = r'C:\Users\Daniel Estrada\.gemini\antigravity\scratch\weekly-showing-reports'
AGENT_BASE = os.path.join(BASE, 'agents', 'joanna-jimenez')
slug = '7334-harding-unit-6'

for base in [BASE, AGENT_BASE]:
    html_path = os.path.join(base, slug, 'index.html')
    if not os.path.exists(html_path):
        continue
    with open(html_path, 'r', encoding='utf-8') as f:
        html = f.read()

    # Fix DOM: 148 -> 123
    html = re.sub(
        r'(Days on Market</div>\s*<div class="card-value[^"]*">\s*)148(\s*)',
        lambda m: m.group(1) + '123' + m.group(2),
        html
    )

    # Fix Physical Showings: last7=1 -> 2, grand=27 -> 28
    html = re.sub(
        r'(Physical Showings.*?last-7">\s*)1(\s*</div>\s*<div class="grand-total">\s*)27(\s*</div>)',
        lambda m: m.group(1) + '2' + m.group(2) + '28' + m.group(3),
        html, flags=re.DOTALL
    )

    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html)

    # Verify
    m_dom = re.search(r'Days on Market</div>\s*<div class="card-value[^"]*">\s*([\d,]+)', html)
    m_show = re.search(r'Physical Showings.*?last-7">\s*([^<]+)\s*</div>\s*<div class="grand-total">\s*([^<]+)\s*</div>', html, re.DOTALL)
    print(f"{base}/{slug}:")
    print(f"  DOM = {m_dom.group(1).strip() if m_dom else 'NOT FOUND'}")
    print(f"  Showings last7={m_show.group(1).strip() if m_show else '?'}, grand={m_show.group(2).strip() if m_show else '?'}")
