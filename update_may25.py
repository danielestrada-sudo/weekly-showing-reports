"""
Update script for May 18 - May 24, 2026 (Joanna Jimenez properties)

Updates:
- Report period header
- Days on Market (+8, not 7 — Memorial Day holiday on Monday May 26)
- Last 7 Days Listing Views (from Compass PDF reports)
- Grand Total Listing Views (old + new)
- Last 7 Days Emails Opened (6,616 from Google Sheets)
- Grand Total Emails (old + new)
- Last 7 Days Social Views (255 from Google Sheets)
- Grand Total Social Views (old + new)
- City stats (from PDF last pages)
- Visitor map extracted from PDF (last page)
- Map src cache-bust timestamp
- Footer date
- Feedback (from weekly_data.json — to be added separately)

Properties with PDFs this week:
  6061-collins-avenue-unit-5f     -> 414 views
  1376-sw-4th-st-7               -> 75 views
  7334-harding-unit-6            -> 66 views
  8000-harding-avenue-unit-2b    -> 163 views
  17301-biscayne-boulevard-unit-1401 -> 86 views
  763-pennsylvania-avenue-unit-116 -> 125 views
  1945-s-ocean-dr-unit-m2        -> 33 views
  244-biscayne-3702              -> 52 views
  88-sw-7-st-1012                -> 190 views

No PDFs this week for:
  234-washington-ave, 320-85-st-15, 10449-sw-78th-st
  (these will get DOM +8, emails, social updated but no new view count)
"""

import re, os, fitz

BASE = r'C:\Users\Daniel Estrada\.gemini\antigravity\scratch\weekly-showing-reports'
AGENT_BASE = os.path.join(BASE, 'agents', 'joanna-jimenez')
PDF_DIR = r'B:\Downloads Compass\Weekly Reports\Joannas Properties Progress Reports\May 18 - May 23rd'

REPORT_PERIOD = '18 May 2026 - 24 May 2026'
FOOTER_DATE = 'May 25, 2026'
CACHE_TS = '20260525'
DOM_INCREMENT = 8  # +8 due to Memorial Day holiday

# Marketing data from Google Sheets (May 18 - May 23rd)
EMAILS_LAST7 = '+6,616'
SOCIAL_LAST7 = '255'

# PDF data: slug -> {last7_views, grand_views_old, emails_grand_old, social_grand_old, cities, pdf_file}
# Grand totals are OLD values from the current HTML (will compute new = old + this_week)
PROPERTIES = {
    '6061-collins-avenue-unit-5f': {
        'last7_views': 414,
        'old_grand_views': 2874,
        'old_grand_emails': 51706,
        'old_grand_social': 4197,
        'cities': [
            ('New City', '50%'), ('Miami Beach', '50%'),
        ],
        'pdf': 'listing-insights-report-1175185e-43cf-45c9-b500-c05ac0c030a0-2026-05-25.pdf',
        'map_page': 3,  # 4-page PDF, last page index
    },
    '1376-sw-4th-st-7': {
        'last7_views': 75,
        'old_grand_views': 836,
        'old_grand_emails': 38901,
        'old_grand_social': 255,
        'cities': [
            ('Miami', '55.6%'), ('Hialeah', '22.2%'),
            ('Gainesville', '11.1%'), ('Brooklyn', '11.1%'),
        ],
        'pdf': 'listing-insights-report-55bee243-6812-4ed2-add7-4e926d7e6b6a-2026-05-25.pdf',
        'map_page': 3,
    },
    '7334-harding-unit-6': {
        'last7_views': 66,
        'old_grand_views': 3892,
        'old_grand_emails': 108708,
        'old_grand_social': 3765,
        'cities': [
            ('Plymouth', '50%'), ('Hialeah', '50%'),
        ],
        'pdf': 'listing-insights-report-9d5fbd7b-ae93-4377-9288-752afac3b321-2026-05-25.pdf',
        'map_page': 3,
    },
    '8000-harding-avenue-unit-2b': {
        'last7_views': 163,
        'old_grand_views': 1748,
        'old_grand_emails': 62708,
        'old_grand_social': 3795,
        'cities': [
            ('Miami', '55.6%'), ('New Orleans', '22.2%'),
            ('Sunny Isles Beach', '11.1%'), ('Severna Park', '11.1%'),
        ],
        'pdf': 'listing-insights-report-c973bbe2-920d-44fe-b515-872566a2330f-2026-05-25.pdf',
        'map_page': 3,
    },
    '17301-biscayne-boulevard-unit-1401': {
        'last7_views': 86,
        'old_grand_views': 1703,
        'old_grand_emails': 51706,
        'old_grand_social': 6131,
        'cities': [
            ('Miami', '40%'), ('Tampa', '30%'),
            ('Miami Beach', '20%'), ('New York', '10%'),
        ],
        'pdf': 'listing-insights-report-d0b41ad2-5264-4e75-b8f5-ac938be71f16-2026-05-25.pdf',
        'map_page': 3,
    },
    '763-pennsylvania-avenue-unit-116': {
        'last7_views': 125,
        'old_grand_views': 8538,
        'old_grand_emails': 88470,
        'old_grand_social': 6414,
        'cities': [
            ('Boynton Beach', '50%'), ('Hollywood', '25%'), ('Hialeah', '25%'),
        ],
        'pdf': 'listing-insights-report-dc46c560-2361-4d60-85ce-90704665a067-2026-05-25.pdf',
        'map_page': 3,
    },
    '1945-s-ocean-dr-unit-m2': {
        'last7_views': 33,
        'old_grand_views': 256,
        'old_grand_emails': 38901,
        'old_grand_social': 457,
        'cities': [
            ('Miami', '100%'),
        ],
        'pdf': 'listing-insights-report-e4eb7d3c-fa29-4fa3-8c91-cd9c13c8e7e8-2026-05-25.pdf',
        'map_page': 3,
    },
    '244-biscayne-3702': {
        'last7_views': 52,
        'old_grand_views': 438,
        'old_grand_emails': 42168,
        'old_grand_social': 1763,
        'cities': [
            ('Miami', '87.5%'), ('Boston', '12.5%'),
        ],
        'pdf': 'listing-insights-report-e79c63ee-99fb-42cb-8e81-1a737f60157b-2026-05-25.pdf',
        'map_page': 3,
    },
    '88-sw-7-st-1012': {
        'last7_views': 190,
        'old_grand_views': 648,
        'old_grand_emails': 19593,
        'old_grand_social': 2893,
        'cities': [
            ('Miami', '24%'), ('Washington', '12%'), ('Los Angeles', '12%'),
            ('New York', '8%'), ('Forest City', '8%'), ('Bountiful', '8%'),
            ('The Bronx', '4%'), ('St. Cloud', '4%'), ('Seattle', '4%'),
            ('Miami Beach', '4%'), ('Houston', '4%'), ('Boston', '4%'),
        ],
        'pdf': 'listing-insights-report-ed9bd011-f677-4b5b-87bb-97f538831c9f-2026-05-25.pdf',
        'map_page': 4,  # 5-page PDF
    },
}

# Properties with no PDF this week — only DOM/email/social update
NO_PDF_PROPERTIES = {
    '234-washington-ave': {
        'old_grand_views': 10713,
        'old_grand_emails': 130175,
        'old_grand_social': 29303,
    },
    '320-85-st-15': {
        'old_grand_views': 1448,
        'old_grand_emails': 63723,
        'old_grand_social': 1926,
    },
    '10449-sw-78th-st': {
        'old_grand_views': 657,
        'old_grand_emails': 13221,
        'old_grand_social': 1495,
    },
}


def fmt(n):
    """Format integer with commas."""
    return f"{n:,}"


def build_city_stats_html(cities):
    if not cities:
        return ''
    html = '<div class="city-stats-grid" style="display: grid; grid-template-columns: 1fr 1fr; gap: 2rem; margin-top: 2rem; padding-top: 2rem; border-top: 1px solid var(--border);">'
    for city, pct in cities:
        html += f'<div style="display: flex; justify-content: space-between; padding: 0.5rem 0; border-bottom: 1px solid rgba(0,0,0,0.05);"><span style="font-weight: 600;">{city}</span><span style="color: var(--accent); font-weight: 700;">{pct}</span></div>'
    html += '</div>'
    return html


def extract_map(slug, pdf_name, map_page_idx):
    pdf_path = os.path.join(PDF_DIR, pdf_name)
    if not os.path.exists(pdf_path):
        print(f'  SKIP map extraction (PDF not found): {pdf_path}')
        return False

    doc = fitz.open(pdf_path)
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
    print(f'  Map saved: {slug} (page {map_page_idx + 1})')
    doc.close()
    return True


def update_html(html, d):
    new_grand_views = d['old_grand_views'] + d.get('last7_views', 0)
    new_grand_emails = d['old_grand_emails'] + 6616
    new_grand_social = d['old_grand_social'] + 255

    last7_views = d.get('last7_views', None)

    # 1. Report period
    html = re.sub(
        r'Report Period:.*?(?=\s*</div>)',
        f'Report Period: {REPORT_PERIOD}',
        html
    )

    # 2. Days on Market card (+8)
    html = re.sub(
        r'(card-label[^>]*>Days on Market</div>\s*<div class="card-value[^"]*">\s*)[\w/,]+(\s*\n)',
        lambda m: m.group(1) + f'\n                        {d["dom"]}\n',
        html
    )

    # 3. Last 7 Days Views card (only if we have PDF data)
    if last7_views is not None:
        html = re.sub(
            r'(card-label[^>]*>Last 7 Days Views</div>\s*<div class="card-value[^"]*">\s*)[\w/,]+',
            lambda m: m.group(1) + f'\n                        {last7_views}',
            html
        )

    # 4. Listing Views table row (last-7 and grand-total)
    if last7_views is not None:
        html = re.sub(
            r'(metric-name[^>]*>Listing Views.*?</div>\s*<div class="last-7">)[^<]*(</div>\s*<div class="grand-total">)[^<]*(</div>)',
            lambda m: m.group(1) + str(last7_views) + m.group(2) + fmt(new_grand_views) + m.group(3),
            html, flags=re.DOTALL
        )
    else:
        # No new views but still update grand total (keep last7 as is)
        html = re.sub(
            r'(metric-name[^>]*>Listing Views.*?</div>\s*<div class="last-7">)([^<]*)(</div>\s*<div class="grand-total">)[^<]*(</div>)',
            lambda m: m.group(1) + m.group(2) + m.group(3) + fmt(new_grand_views) + m.group(4),
            html, flags=re.DOTALL
        )

    # 5. Emails table row
    html = re.sub(
        r'(metric-name[^>]*>Emails Sent.*?</div>\s*<div class="last-7">)[^<]*(</div>\s*<div class="grand-total">)[^<]*(</div>)',
        lambda m: m.group(1) + EMAILS_LAST7 + m.group(2) + fmt(new_grand_emails) + m.group(3),
        html, flags=re.DOTALL
    )

    # 6. Social Views table row
    html = re.sub(
        r'(metric-name[^>]*>Social Media Views.*?</div>\s*<div class="last-7">)[^<]*(</div>\s*<div class="grand-total">)[^<]*(</div>)',
        lambda m: m.group(1) + SOCIAL_LAST7 + m.group(2) + fmt(new_grand_social) + m.group(3),
        html, flags=re.DOTALL
    )

    # 7. Map src cache-busting
    html = re.sub(
        r'property_views_map_clean\.png(?:\?v=\d+)?',
        f'property_views_map_clean.png?v={CACHE_TS}',
        html
    )

    # 8. City stats grid
    cities = d.get('cities', [])
    if cities:
        city_html = build_city_stats_html(cities)
        existing_pattern = r'<div class="city-stats-grid"[^>]*>.*?</div>\s*</div>'
        if re.search(existing_pattern, html, flags=re.DOTALL):
            html = re.sub(existing_pattern, city_html + '\n            </div>', html, flags=re.DOTALL)
        else:
            html = re.sub(
                r'(property_views_map_clean\.png[^>]*>.*?</div>)',
                lambda m: m.group(1) + '\n                ' + city_html,
                html, flags=re.DOTALL
            )

    # 9. Footer date
    html = re.sub(
        r'Generated on [^\.]+\.',
        f'Generated on {FOOTER_DATE}.',
        html
    )

    return html


def write_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f'  Written: {path}')


def process_property(slug, d, location_base):
    html_path = os.path.join(location_base, slug, 'index.html')
    if not os.path.exists(html_path):
        print(f'  SKIP (no file): {html_path}')
        return
    with open(html_path, encoding='utf-8') as f:
        html = f.read()
    updated = update_html(html, d)
    write_file(html_path, updated)


# ---- MAIN ----
print('=== May 18-24, 2026 Update for Joanna Jimenez properties ===\n')

# Properties WITH PDF data
for slug, data in PROPERTIES.items():
    # Compute DOM from current HTML
    html_path = os.path.join(AGENT_BASE, slug, 'index.html')
    if not os.path.exists(html_path):
        html_path = os.path.join(BASE, slug, 'index.html')
    dom_current = 0
    if os.path.exists(html_path):
        with open(html_path, encoding='utf-8') as f:
            h = f.read()
        m = re.search(r'Days on Market</div>\s*<div class="card-value[^"]*">\s*([\d,]+)', h)
        if m:
            dom_current = int(m.group(1).replace(',', ''))
    data['dom'] = dom_current + DOM_INCREMENT

    print(f'\nProcessing: {slug}')
    print(f'  DOM: {dom_current} -> {data["dom"]}')
    print(f'  Last 7 Views: {data["last7_views"]}')
    print(f'  Grand Views: {fmt(data["old_grand_views"])} -> {fmt(data["old_grand_views"] + data["last7_views"])}')

    extract_map(slug, data['pdf'], data['map_page'])
    process_property(slug, data, BASE)
    process_property(slug, data, AGENT_BASE)

# Properties WITHOUT PDF data
print('\n--- Properties without PDF (DOM + emails/social only) ---')
for slug, data in NO_PDF_PROPERTIES.items():
    html_path = os.path.join(AGENT_BASE, slug, 'index.html')
    if not os.path.exists(html_path):
        html_path = os.path.join(BASE, slug, 'index.html')
    dom_current = 0
    if os.path.exists(html_path):
        with open(html_path, encoding='utf-8') as f:
            h = f.read()
        m = re.search(r'Days on Market</div>\s*<div class="card-value[^"]*">\s*([\d,]+)', h)
        if m:
            dom_current = int(m.group(1).replace(',', ''))
    data['dom'] = dom_current + DOM_INCREMENT
    data['cities'] = []

    print(f'\nProcessing (no PDF): {slug}')
    print(f'  DOM: {dom_current} -> {data["dom"]}')
    process_property(slug, data, BASE)
    process_property(slug, data, AGENT_BASE)

print('\n=== All done! ===')
print('NOTE: Feedback section has NOT been updated yet.')
print('Please provide showing feedback for May 18-24 to complete the update.')
