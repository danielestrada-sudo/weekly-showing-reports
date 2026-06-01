import re, os

BASE = r'C:\Users\Daniel Estrada\.gemini\antigravity\scratch\weekly-showing-reports'
AGENT_BASE = os.path.join(BASE, 'agents', 'joanna-jimenez')
slug = '8000-harding-avenue-unit-2b'

for base in [BASE, AGENT_BASE]:
    html_path = os.path.join(base, slug, 'index.html')
    if not os.path.exists(html_path):
        continue
    with open(html_path, 'r', encoding='utf-8') as f:
        html = f.read()

    html = re.sub(
        r'(Days on Market</div>\s*<div class="card-value[^"]*">\s*)17(\s*)',
        lambda m: m.group(1) + '88' + m.group(2),
        html
    )

    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html)

    m_dom = re.search(r'Days on Market</div>\s*<div class="card-value[^"]*">\s*([\d,]+)', html)
    print(f"{base}: DOM = {m_dom.group(1).strip() if m_dom else 'NOT FOUND'}")
