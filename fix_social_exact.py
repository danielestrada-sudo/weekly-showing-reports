import os
import re

BASE = r'C:\Users\Daniel Estrada\.gemini\antigravity\scratch\weekly-showing-reports'
AGENT_BASE = os.path.join(BASE, 'agents', 'joanna-jimenez')

# 244-biscayne-3702
for base in [BASE, AGENT_BASE]:
    path = os.path.join(base, '244-biscayne-3702', 'index.html')
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            html = f.read()
        html = html.replace('<div class="last-7">+222</div>\n                            <div class="grand-total">1,985</div>', '<div class="last-7">+1,000</div>\n                            <div class="grand-total">2,763</div>')
        with open(path, 'w', encoding='utf-8') as f:
            f.write(html)

# 763-pennsylvania
for base in [BASE, AGENT_BASE]:
    path = os.path.join(base, '763-pennsylvania-avenue-unit-116', 'index.html')
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            html = f.read()
        html = html.replace('<div class="last-7">+222</div>\n                            <div class="grand-total">6,636</div>', '<div class="last-7">+20</div>\n                            <div class="grand-total">6,434</div>')
        with open(path, 'w', encoding='utf-8') as f:
            f.write(html)

# 6061-collins
for base in [BASE, AGENT_BASE]:
    path = os.path.join(base, '6061-collins-avenue-unit-5f', 'index.html')
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            html = f.read()
        html = html.replace('<div class="last-7">+222</div>\n                            <div class="grand-total">4,419</div>', '<div class="last-7">+100</div>\n                            <div class="grand-total">4,297</div>')
        with open(path, 'w', encoding='utf-8') as f:
            f.write(html)

# properties.csv
csv_path = os.path.join(BASE, 'properties.csv')
with open(csv_path, 'r', encoding='utf-8') as f:
    csv_text = f.read()

csv_text = csv_text.replace('244 Biscayne #3702,"1,985"', '244 Biscayne #3702,"2,763"')
csv_text = csv_text.replace('"763 Pennsylvania Avenue, Unit 116","6,636"', '"763 Pennsylvania Avenue, Unit 116","6,434"')
csv_text = csv_text.replace('"6061 Collins Avenue, Unit 5F","4,419"', '"6061 Collins Avenue, Unit 5F","4,297"')

with open(csv_path, 'w', encoding='utf-8') as f:
    f.write(csv_text)

print("Social views updated successfully.")
