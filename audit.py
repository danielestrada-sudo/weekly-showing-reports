import re, os

BASE = r'C:\Users\Daniel Estrada\.gemini\antigravity\scratch\weekly-showing-reports'
AGENT_BASE = os.path.join(BASE, 'agents', 'joanna-jimenez')

properties = {
    '244-biscayne-3702':             {'expected_last7': '+1,000'},
    '763-pennsylvania-avenue-unit-116': {'expected_last7': '+20'},
    '6061-collins-avenue-unit-5f':   {'expected_last7': '+100'},
}

all_props = [
    '1376-sw-4th-st-7',
    '17301-biscayne-boulevard-unit-1401',
    '1945-s-ocean-dr-unit-m2',
    '244-biscayne-3702',
    '6061-collins-avenue-unit-5f',
    '7334-harding-unit-6',
    '763-pennsylvania-avenue-unit-116',
    '8000-harding-avenue-unit-2b',
    '88-sw-7-st-1012',
    '234-washington-ave',
    '320-85-st-15',
    '1710-nw-106-terr',
    '10449-sw-78th-st',
]

print("=== AUDIT OF ALL PROPERTIES ===\n")
for slug in all_props:
    # prefer root, fallback to agent
    html_path = os.path.join(BASE, slug, 'index.html')
    if not os.path.exists(html_path):
        html_path = os.path.join(AGENT_BASE, slug, 'index.html')
    if not os.path.exists(html_path):
        print(f"{slug}: FILE NOT FOUND")
        continue
    with open(html_path, 'r', encoding='utf-8') as f:
        html = f.read()

    period = re.search(r'Report Period:\s*(.*?)(?=\s*</div>)', html)
    dom = re.search(r'Days on Market</div>\s*<div class="card-value[^"]*">\s*([\d,]+)', html)
    last7_views = re.search(r'Last 7 Days Views</div>\s*<div class="card-value[^"]*">\s*([\d,]+)', html)
    social_row = re.search(r'Social Media Views.*?last-7">\s*([^<]+)\s*</div>\s*<div class="grand-total">\s*([^<]+)\s*</div>', html, re.DOTALL)
    email_row = re.search(r'Emails Sent.*?last-7">\s*([^<]+)\s*</div>\s*<div class="grand-total">\s*([^<]+)\s*</div>', html, re.DOTALL)
    views_row = re.search(r'Listing Views.*?last-7">\s*([^<]+)\s*</div>\s*<div class="grand-total">\s*([^<]+)\s*</div>', html, re.DOTALL)
    showings_row = re.search(r'Physical Showings.*?last-7">\s*([^<]+)\s*</div>\s*<div class="grand-total">\s*([^<]+)\s*</div>', html, re.DOTALL)
    footer = re.search(r'Generated on ([^.]+)\.', html)

    print(f"--- {slug} ---")
    print(f"  Period:       {period.group(1).strip() if period else 'N/A'}")
    print(f"  DOM:          {dom.group(1).strip() if dom else 'N/A'}")
    print(f"  Last7 Views:  {last7_views.group(1).strip() if last7_views else 'N/A'}")
    print(f"  Views:        last7={views_row.group(1).strip() if views_row else 'N/A'}, grand={views_row.group(2).strip() if views_row else 'N/A'}")
    print(f"  Emails:       last7={email_row.group(1).strip() if email_row else 'N/A'}, grand={email_row.group(2).strip() if email_row else 'N/A'}")
    print(f"  Social:       last7={social_row.group(1).strip() if social_row else 'N/A'}, grand={social_row.group(2).strip() if social_row else 'N/A'}")
    print(f"  Showings:     last7={showings_row.group(1).strip() if showings_row else 'N/A'}, grand={showings_row.group(2).strip() if showings_row else 'N/A'}")
    print(f"  Footer date:  {footer.group(1).strip() if footer else 'N/A'}")
    print()
