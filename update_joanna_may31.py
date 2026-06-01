import os
import re
import csv
import json
import fitz

BASE = r'C:\Users\Daniel Estrada\.gemini\antigravity\scratch\weekly-showing-reports'
AGENT_BASE = os.path.join(BASE, 'agents', 'joanna-jimenez')
PDF_DIR = r'B:\Downloads Compass\Weekly Reports\Joannas Properties Progress Reports\May 25th - 31st'

REPORT_PERIOD = '25 May 2026 - 31 May 2026'
FOOTER_DATE = 'June 01, 2026'
CACHE_TS = '20260601'
DOM_INCREMENT = 7

EMAILS_LAST7 = 3000
SOCIAL_LAST7 = 222

PROPERTIES = {
    '1376-sw-4th-st-7': {'pdf': '1376 sw st 7.pdf', 'map_page': 3},
    '17301-biscayne-boulevard-unit-1401': {'pdf': '17301.pdf', 'map_page': 3},
    '1945-s-ocean-dr-unit-m2': {'pdf': '1945 m2.pdf', 'map_page': 3},
    '244-biscayne-3702': {'pdf': '244 3702.pdf', 'map_page': 3},
    '6061-collins-avenue-unit-5f': {'pdf': '6061 5f.pdf', 'map_page': 3},
    '7334-harding-unit-6': {'pdf': '7334.pdf', 'map_page': 3},
    '763-pennsylvania-avenue-unit-116': {'pdf': '763.pdf', 'map_page': 3},
    '8000-harding-avenue-unit-2b': {'pdf': '8000 2b.pdf', 'map_page': 3},
    '88-sw-7-st-1012': {'pdf': '88 sw 1012.pdf', 'map_page': 4},
    # NO PDF THIS WEEK (Only DOM, emails, social get updated)
    '234-washington-ave': {'pdf': None},
    '320-85-st-15': {'pdf': None},
    '1710-nw-106-terr': {'pdf': None},
    '10449-sw-78th-st': {'pdf': None}
}

FEEDBACK_DATA = {
    '1376-sw-4th-st-7': {
        'showings': 2,
        'notes': ['Family went twice to see it last week and stated " the house is well distributed some of the bedrooms are small. What didnt work for the clients is the housing conditions surrouding the building. They also felt the price a bit high up for a up-coming neighborhood"; the tother stated " she liked another area better"']
    },
    '1945-s-ocean-dr-unit-m2': {
        'showings': 2,
        'notes': ['On Monday 5/25. Hello Connor, my client said it\'s to small for them , they Loking for 3bed in Ocean Marine. 2nd showing submitted the offer for herself.']
    },
    '763-pennsylvania-avenue-unit-116': {
        'showings': 0,
        'notes': ['Open House Held Wednesday and didnt have anyone show up']
    },
    '6061-collins-avenue-unit-5f': {
        'showings': 2,
        'notes': ['1) Wednesday AM - saw 16 condos all oceanfront with several under construction and picked two others at better prices and conditions Wed PM- My clients decided it\'s not a good fit as the property needs some updates and on top of that taking over an assessment is not something they are willing to do at that sales price. Best of luck and thank you!']
    },
    '7334-harding-unit-6': {
        'showings': 1,
        'notes': ['Received an offer from one of the showings']
    },
    '8000-harding-avenue-unit-2b': {
        'showings': 2,
        'notes': ['Received an offer from one of the showings.  The other stated: My client likes the unit, but we found other in a higher level']
    }
}

def fmt(n):
    return f"{n:,}"

def extract_pdf_data(pdf_path, map_page_idx, slug):
    if not os.path.exists(pdf_path):
        return None
    
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()

    publisher_data = {}
    publishers_list = ["Compass", "Trulia", "Zillow", "Realtor", "Others"]
    for pub in publishers_list:
        pattern = rf"{pub}\s*\n\s*(\d+)"
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            publisher_data[pub] = int(match.group(1))
        else:
            pattern = rf"{pub}\s+(\d+)"
            match = re.search(pattern, text, re.IGNORECASE)
            publisher_data[pub] = int(match.group(1)) if match else 0
            
    total_views = sum(publisher_data.values())

    city_data = []
    if "Views By City" in text:
        city_section = text.split("Views By City")[1]
        city_lines = [line.strip() for line in city_section.split('\n') if line.strip()]
        for i in range(len(city_lines)):
            if city_lines[i] == "CITY" and i+2 < len(city_lines):
                start_index = i + 2
                for j in range(start_index, len(city_lines), 2):
                    if j+1 < len(city_lines) and "%" in city_lines[j+1]:
                        city_name = city_lines[j]
                        if city_name == "Based on Compass data": break
                        pct = city_lines[j+1].replace("%", "")
                        try:
                            city_data.append({"name": city_name, "pct": float(pct)})
                        except: pass
                    else: break
                break

    if map_page_idx >= len(doc):
        map_page_idx = len(doc) - 1
    page = doc[map_page_idx]
    mat = fitz.Matrix(3, 3)
    pix = page.get_pixmap(matrix=mat)

    out_root = os.path.join(BASE, slug, 'property_views_map_clean.png')
    out_agent = os.path.join(AGENT_BASE, slug, 'property_views_map_clean.png')
    os.makedirs(os.path.dirname(out_root), exist_ok=True)
    os.makedirs(os.path.dirname(out_agent), exist_ok=True)
    pix.save(out_root)
    pix.save(out_agent)
    doc.close()

    return {
        'last7_views': total_views,
        'publishers': publisher_data,
        'cities': city_data
    }

def format_new_feedback(notes):
    combined = " ".join(notes)
    return f'''
                <div class="feedback-item">
                    <div class="feedback-text">
                        "{combined}"
                        <span class="agent-date" style="display: block; margin-top: 0.5rem; font-style: normal;">— May 25 - May 31, 2026</span>
                    </div>
                </div>'''

def build_city_stats_html(cities):
    if not cities: return ''
    html = '<div class="city-stats-grid" style="display: grid; grid-template-columns: 1fr 1fr; gap: 2rem; margin-top: 2rem; padding-top: 2rem; border-top: 1px solid var(--border);">'
    for city in cities:
        html += f'<div style="display: flex; justify-content: space-between; padding: 0.5rem 0; border-bottom: 1px solid rgba(0,0,0,0.05);"><span style="font-weight: 600;">{city["name"]}</span><span style="color: var(--accent); font-weight: 700;">{city["pct"]}%</span></div>'
    html += '</div>'
    return html

print("Updating Joanna's reports...")

csv_path = os.path.join(BASE, "properties.csv")
props_info = []
with open(csv_path, 'r', encoding='utf-8') as f:
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

for slug, pdata in PROPERTIES.items():
    print(f"Processing {slug}...")
    
    html_path = os.path.join(BASE, slug, 'index.html')
    if not os.path.exists(html_path):
        html_path = os.path.join(AGENT_BASE, slug, 'index.html')
        if not os.path.exists(html_path):
            print(f"  SKIP (no file): {html_path}")
            continue
        
    with open(html_path, 'r', encoding='utf-8') as f:
        html = f.read()
        
    dom_current = 0
    m_dom = re.search(r'Days on Market</div>\s*<div class="card-value[^"]*">\s*([\d,]+)', html)
    if m_dom: dom_current = int(m_dom.group(1).replace(',', ''))
    new_dom = dom_current + DOM_INCREMENT

    m_grand_views = re.search(r'metric-name[^>]*>Listing Views.*?grand-total">\s*([\d,]+)\s*</div>', html, flags=re.DOTALL)
    old_grand_views = int(m_grand_views.group(1).replace(',', '')) if m_grand_views else 0
    
    m_grand_emails = re.search(r'metric-name[^>]*>Emails Sent.*?grand-total">\s*([\d,]+)\s*</div>', html, flags=re.DOTALL)
    old_grand_emails = int(m_grand_emails.group(1).replace(',', '')) if m_grand_emails else 0
    
    m_grand_social = re.search(r'metric-name[^>]*>Social Media Views.*?grand-total">\s*([\d,]+)\s*</div>', html, flags=re.DOTALL)
    old_grand_social = int(m_grand_social.group(1).replace(',', '')) if m_grand_social else 0
    
    m_grand_showings = re.search(r'metric-name[^>]*>Physical Showings.*?grand-total">\s*([\d,]+)\s*</div>', html, flags=re.DOTALL)
    old_grand_showings = int(m_grand_showings.group(1).replace(',', '')) if m_grand_showings else 0

    pdf_data = None
    if pdata['pdf']:
        pdf_path = os.path.join(PDF_DIR, pdata['pdf'])
        pdf_data = extract_pdf_data(pdf_path, pdata['map_page'], slug)

    last7_views = pdf_data['last7_views'] if pdf_data else 0
    new_grand_views = old_grand_views + last7_views
    
    new_grand_emails = old_grand_emails + EMAILS_LAST7
    new_grand_social = old_grand_social + SOCIAL_LAST7
    
    fb = FEEDBACK_DATA.get(slug, {'showings': 0, 'notes': []})
    last7_showings = fb['showings']
    new_grand_showings = old_grand_showings + last7_showings

    html = re.sub(r'Report Period:.*?(?=\s*</div>)', f'Report Period: {REPORT_PERIOD}', html)

    html = re.sub(
        r'(card-label[^>]*>Days on Market</div>\s*<div class="card-value[^"]*">\s*)[\w/,]+(\s*\n)',
        lambda m: m.group(1) + f'\n                        {new_dom}\n',
        html
    )

    if pdf_data:
        html = re.sub(
            r'(card-label[^>]*>Last 7 Days Views</div>\s*<div class="card-value[^"]*">\s*)[\w/,]+',
            lambda m: m.group(1) + f'\n                        {last7_views:,}',
            html
        )

    if pdf_data:
        html = re.sub(
            r'(metric-name[^>]*>Listing Views.*?</div>\s*<div class="last-7">)[^<]*(</div>\s*<div class="grand-total">)[^<]*(</div>)',
            lambda m: m.group(1) + f"{last7_views:,}" + m.group(2) + fmt(new_grand_views) + m.group(3),
            html, flags=re.DOTALL
        )
    else:
        html = re.sub(
            r'(metric-name[^>]*>Listing Views.*?</div>\s*<div class="last-7">)([^<]*)(</div>\s*<div class="grand-total">)[^<]*(</div>)',
            lambda m: m.group(1) + m.group(2) + m.group(3) + fmt(new_grand_views) + m.group(4),
            html, flags=re.DOTALL
        )

    html = re.sub(
        r'(metric-name[^>]*>Emails Sent.*?</div>\s*<div class="last-7">)[^<]*(</div>\s*<div class="grand-total">)[^<]*(</div>)',
        lambda m: m.group(1) + f"+{EMAILS_LAST7:,}" + m.group(2) + fmt(new_grand_emails) + m.group(3),
        html, flags=re.DOTALL
    )

    html = re.sub(
        r'(metric-name[^>]*>Social Media Views.*?</div>\s*<div class="last-7">)[^<]*(</div>\s*<div class="grand-total">)[^<]*(</div>)',
        lambda m: m.group(1) + f"+{SOCIAL_LAST7:,}" + m.group(2) + fmt(new_grand_social) + m.group(3),
        html, flags=re.DOTALL
    )
    
    html = re.sub(
        r'(metric-name[^>]*>Physical Showings.*?</div>\s*<div class="last-7">)[^<]*(</div>\s*<div class="grand-total">)[^<]*(</div>)',
        lambda m: m.group(1) + str(last7_showings) + m.group(2) + fmt(new_grand_showings) + m.group(3),
        html, flags=re.DOTALL
    )

    html = re.sub(
        r'property_views_map_clean\.png(?:\?v=\d+)?',
        f'property_views_map_clean.png?v={CACHE_TS}',
        html
    )

    if pdf_data and pdf_data['cities']:
        city_html = build_city_stats_html(pdf_data['cities'])
        existing_pattern = r'<div class="city-stats-grid"[^>]*>.*?</div>\s*</div>'
        if re.search(existing_pattern, html, flags=re.DOTALL):
            html = re.sub(existing_pattern, city_html + '\n            </div>', html, flags=re.DOTALL)
        else:
            html = re.sub(
                r'(property_views_map_clean\.png[^>]*>.*?</div>)',
                lambda m: m.group(1) + '\n                ' + city_html,
                html, flags=re.DOTALL
            )
            
    if pdf_data:
        pubs = pdf_data['publishers']
        html = re.sub(r'const publishers = \{.*?\};', f"const publishers = {json.dumps(pubs)};", html)

    html = re.sub(r'Generated on [^\.]+\.', f'Generated on {FOOTER_DATE}.', html)
    
    if fb['notes']:
        new_fb = format_new_feedback(fb['notes'])
        html = re.sub(r'(<div class="feedback-item">)', lambda m: new_fb + '\n' + m.group(1), html, count=1)

    for target in [os.path.join(BASE, slug), os.path.join(AGENT_BASE, slug)]:
        os.makedirs(target, exist_ok=True)
        with open(os.path.join(target, "index.html"), 'w', encoding='utf-8') as f:
            f.write(html)
            
    for row in props_info:
        if isinstance(row, dict):
            addr = row.get('Property Address', '').strip()
            if slug.startswith(addr.split(' ')[0].lower()):
                row['Total Online Visits'] = fmt(new_grand_views)
                row['Total Physical Visits'] = str(new_grand_showings)
                row['Total Emails Opened'] = fmt(new_grand_emails)
                row['Total Social Views'] = fmt(new_grand_social)
                row['Days On Market'] = str(new_dom)
                break

with open(csv_path, 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(props_info[0])
    writer.writerow(props_info[1])
    
    dict_writer = csv.DictWriter(f, fieldnames=props_info[1])
    for row in props_info[2:]:
        dict_writer.writerow(row)

print("All Joanna properties updated locally!")
