import re
path = r'C:\Users\Daniel Estrada\.gemini\antigravity\scratch\weekly-showing-reports\agents\joanna-jimenez\17301-biscayne-boulevard-unit-1401\index.html'
with open(path, 'r', encoding='utf-8') as f:
    html = f.read()

def print_stat(name, regex):
    m = re.search(regex, html, re.DOTALL)
    print(f'{name}: last7={m.group(1).strip() if m else None}, grand={m.group(2).strip() if m else None}')

print_stat('Views', r'Listing Views.*?last-7">\s*([^<]+)\s*</div>\s*<div class="grand-total">\s*([^<]+)\s*</div>')
print_stat('Emails', r'Emails Sent.*?last-7">\s*([^<]+)\s*</div>\s*<div class="grand-total">\s*([^<]+)\s*</div>')
print_stat('Social', r'Social Media Views.*?last-7">\s*([^<]+)\s*</div>\s*<div class="grand-total">\s*([^<]+)\s*</div>')
print_stat('Showings', r'Physical Showings.*?last-7">\s*([^<]+)\s*</div>\s*<div class="grand-total">\s*([^<]+)\s*</div>')
