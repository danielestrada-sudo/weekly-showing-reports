import os
import re
import csv

BASE = r'C:\Users\Daniel Estrada\.gemini\antigravity\scratch\weekly-showing-reports'
AGENT_BASE = os.path.join(BASE, 'agents', 'joanna-jimenez')
CSV_PATH = os.path.join(BASE, 'properties.csv')

def fmt(n):
    return f"{n:,}"

def unfmt(s):
    return int(s.replace(',', ''))

updates = {
    '244-biscayne-3702': 1000,
    '763-pennsylvania-avenue-unit-116': 20,
    '6061-collins-avenue-unit-5f': 100
}

# 1. Update properties.csv
props_info = []
with open(CSV_PATH, 'r', encoding='utf-8') as f:
    lines = f.readlines()
    reader = csv.reader(lines)
    header = next(reader)
    if "Remember this info" in header[0] or header[0].startswith(','):
        header2 = next(reader)
        props_info.append(header)
        props_info.append(header2)
        reader = csv.DictReader(lines[2:], fieldnames=header2)
    else:
        props_info.append(header)
        reader = csv.DictReader(lines[1:], fieldnames=header)
    for row in reader:
        props_info.append(row)

for slug, correct_social in updates.items():
    print(f"Fixing {slug}...")
    
    # Calculate difference
    diff = correct_social - 222
    
    # Fix properties.csv
    new_grand_social = 0
    for row in props_info:
        if isinstance(row, dict):
            addr = row.get('Property Address', '').strip()
            if slug.startswith(addr.split(' ')[0].lower()):
                current_grand = unfmt(row['Total Social Views'])
                new_grand_social = current_grand + diff
                row['Total Social Views'] = fmt(new_grand_social)
                break
                
    # Fix HTMLs
    for target in [BASE, AGENT_BASE]:
        html_path = os.path.join(target, slug, 'index.html')
        if not os.path.exists(html_path):
            continue
            
        with open(html_path, 'r', encoding='utf-8') as f:
            html = f.read()
            
        # Replace the +222 with +{correct_social} and update grand total
        # The line looks like: metric-name...>Social Media Views...</div> <div class="last-7">+222</div> <div class="grand-total">XX,XXX</div>
        def replace_social(m):
            return f'{m.group(1)}+{correct_social:,}{m.group(2)}{fmt(new_grand_social)}{m.group(3)}'
            
        html = re.sub(
            r'(metric-name[^>]*>Social Media Views.*?</div>\s*<div class="last-7">)[^<]*(</div>\s*<div class="grand-total">)[^<]*(</div>)',
            replace_social,
            html, flags=re.DOTALL
        )
        
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(html)

# Save properties.csv
with open(CSV_PATH, 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(props_info[0])
    writer.writerow(props_info[1])
    dict_writer = csv.DictWriter(f, fieldnames=props_info[1])
    for row in props_info[2:]:
        dict_writer.writerow(row)

print("Done fixing social views.")
