import re, os
import csv

BASE = r'C:\Users\Daniel Estrada\.gemini\antigravity\scratch\weekly-showing-reports'
AGENT_BASE = os.path.join(BASE, 'agents', 'natalia-figueroa')
slug = '1650-coral-way-unit-607'

html_path = os.path.join(AGENT_BASE, slug, 'index.html')
if os.path.exists(html_path):
    with open(html_path, 'r', encoding='utf-8') as f:
        html = f.read()

    m_dom = re.search(r'Days on Market</div>\s*<div class="card-value[^"]*">\s*([\d,]+)', html)
    print(f"Current DOM for {slug}: {m_dom.group(1).strip() if m_dom else 'NOT FOUND'}")
else:
    print("HTML NOT FOUND")

# Check feedback in content.md
content_path = r'C:\Users\Daniel Estrada\.gemini\antigravity\brain\a3049b86-fe12-4807-a724-d40f2852e20b\.system_generated\steps\20\content.md'
print("\nFeedback rows for Natalia:")
with open(content_path, 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    for row in reader:
        if len(row) > 2 and 'natalia' in row[1].lower():
            print(row)
