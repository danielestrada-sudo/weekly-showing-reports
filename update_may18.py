"""
Update script for May 11 - May 17, 2026 (Joanna Jimenez properties)

Updates:
- Report period
- Days on Market (+7)
- Last 7 Days Listing Views (from PDF)
- Grand Total Listing Views (old + new)
- Last 7 Days Emails Opened (+8,655)
- Grand Total Emails (old + new)
- Visitor map (rendered from PDF last page)
- City stats (from PDF)
- map src cache-bust timestamp

NOT updating yet (pending):
- Physical Showings / feedback
- Social Media Views
"""
import re, os, shutil, fitz

BASE = r'C:\Users\Daniel Estrada\.gemini\antigravity\scratch\weekly-showing-reports'
AGENT_BASE = os.path.join(BASE, 'agents', 'joanna-jimenez')
PDF_DIR = r'B:\Downloads Compass\Weekly Reports\Joannas Properties Progress Reports\May 11 - May 16'

REPORT_PERIOD = '11 May 2026 - 17 May 2026'
FOOTER_DATE = 'May 18, 2026'

# Computed from PDFs and spreadsheet
PROPERTIES = {
    '1376-sw-4th-st-7': {
        'dom': 54,
        'last7_views': 91,
        'grand_views': '836',
        'emails_last7': '+8,655',
        'emails_grand': '38,901',
        'cities': [
            ('Miami', '48.1%'), ('Hialeah', '18.5%'), ('Miramar', '11.1%'),
            ('Pompano Beach', '3.7%'), ('Miami Beach', '3.7%'), ('Metairie', '3.7%'),
            ('Los Angeles', '3.7%'), ('Gonzales', '3.7%'), ('Fort Lauderdale', '3.7%'),
        ],
        'pdf': '1376 Southwest 4th.pdf',
        'map_page': 4,  # 0-indexed: last page = 4 for 5-page PDF
    },
    '17301-biscayne-boulevard-unit-1401': {
        'dom': 39,
        'last7_views': 167,
        'grand_views': '1,703',
        'emails_last7': '+8,655',
        'emails_grand': '51,706',
        'cities': [
            ('Miami', '50%'), ('Tampa', '9.1%'), ('Pompano Beach', '9.1%'),
            ('Winter Park', '4.5%'), ('Queens', '4.5%'), ('Plantation', '4.5%'),
            ('New York', '4.5%'), ('Hollywood', '4.5%'), ('College Park', '4.5%'),
            ('Aventura', '4.5%'),
        ],
        'pdf': '17301 Biscayne.pdf',
        'map_page': 3,  # 4-page PDF, last page = 3
    },
    '1945-s-ocean-dr-unit-m2': {
        'dom': 33,
        'last7_views': 55,
        'grand_views': '256',
        'emails_last7': '+8,655',
        'emails_grand': '38,901',
        'cities': [
            ('Miami', '50%'), ('Prineville', '33.3%'), ('Silver Spring', '16.7%'),
        ],
        'pdf': '1945 South Ocean Drive,.pdf',
        'map_page': 4,  # 5-page PDF
    },
    '244-biscayne-3702': {
        'dom': 34,
        'last7_views': 57,
        'grand_views': '438',
        'emails_last7': '+8,655',
        'emails_grand': '42,168',
        'cities': [
            ('Miami', '35.7%'), ('New Rochelle', '14.3%'), ('Los Angeles', '14.3%'),
            ('Bradenton', '14.3%'), ('Orlando', '7.1%'), ('New York', '7.1%'),
            ('Miami Beach', '7.1%'),
        ],
        'pdf': '244 Biscayne Boulevard 3702,.pdf',
        'map_page': 3,  # 4-page PDF
    },
    '6061-collins-avenue-unit-5f': {
        'dom': 39,
        'last7_views': 395,
        'grand_views': '2,874',
        'emails_last7': '+8,655',
        'emails_grand': '51,706',
        'cities': [
            ('Miami Beach', '33.3%'), ('Bradenton', '23.3%'), ('Miami', '16.7%'),
            ('Hialeah', '6.7%'), ('Brooklyn', '6.7%'), ('Philadelphia', '3.3%'),
            ('Orlando', '3.3%'), ('Coral Springs', '3.3%'), ('Arlington', '3.3%'),
        ],
        'pdf': '6061 Collins Avenue,.pdf',
        'map_page': 3,  # 4-page PDF
    },
    '7334-harding-unit-6': {
        'dom': 112,
        'last7_views': 228,
        'grand_views': '3,892',
        'emails_last7': '+8,655',
        'emails_grand': '108,708',
        'cities': [
            ('Ocala', '16.7%'), ('Miami Beach', '16.7%'), ('Miami', '16.7%'),
            ('Los Angeles', '16.7%'), ('Weston', '8.3%'), ('Miramar', '8.3%'),
            ('Metairie', '8.3%'), ('Hollywood', '8.3%'),
        ],
        'pdf': '7334 Harding Avenue,.pdf',
        'map_page': 3,  # 4-page PDF
    },
    '763-pennsylvania-avenue-unit-116': {
        'dom': 120,
        'last7_views': 176,
        'grand_views': '8,538',
        'emails_last7': '+8,655',
        'emails_grand': '88,470',
        'cities': [
            ('Miami', '46.7%'), ('Miami Beach', '26.7%'), ('Orlando', '13.3%'),
            ('Los Angeles', '6.7%'), ('Aventura', '6.7%'),
        ],
        'pdf': '763 Pennsylvania.pdf',
        'map_page': 3,  # 4-page PDF
    },
    '8000-harding-avenue-unit-2b': {
        'dom': 83,
        'last7_views': 138,
        'grand_views': '1,748',
        'emails_last7': '+8,655',
        'emails_grand': '62,708',
        'cities': [
            ('Ocala', '20%'), ('New Orleans', '20%'), ('Hialeah', '20%'),
            ('Palm Bay', '10%'), ('Miami Beach', '10%'), ('Los Angeles', '10%'),
            ('Ft. Pierce', '10%'),
        ],
        'pdf': '8000 Harding Avenue,.pdf',
        'map_page': 3,  # 4-page PDF
    },
    '88-sw-7-st-1012': {
        'dom': 14,
        'last7_views': 224,
        'grand_views': '648',
        'emails_last7': '+8,655',
        'emails_grand': '19,593',
        'cities': [
            ('Miami', '35.7%'), ('Austin', '21.4%'), ('Los Angeles', '14.3%'),
            ('Tampa', '7.1%'), ('New York', '7.1%'), ('Bridgeport', '7.1%'),
            ('Albuquerque', '7.1%'),
        ],
        'pdf': '88 Southwest 7th Street,.pdf',
        'map_page': 3,  # 4-page PDF
    },
}

CACHE_TS = '20260518'


def extract_map(slug, pdf_name, map_page_idx):
    """Render the last page of the PDF as the visitor map PNG."""
    pdf_path = os.path.join(PDF_DIR, pdf_name)
    if not os.path.exists(pdf_path):
        print(f'  SKIP map extraction (PDF not found): {pdf_path}')
        return False

    doc = fitz.open(pdf_path)
    if map_page_idx >= len(doc):
        map_page_idx = len(doc) - 1
    
    page = doc[map_page_idx]
    mat = fitz.Matrix(3, 3)  # High resolution
    pix = page.get_pixmap(matrix=mat)

    out_root = os.path.join(BASE, slug, 'property_views_map_clean.png')
    out_agent = os.path.join(AGENT_BASE, slug, 'property_views_map_clean.png')
    os.makedirs(os.path.dirname(out_root), exist_ok=True)
    os.makedirs(os.path.dirname(out_agent), exist_ok=True)

    pix.save(out_root)
    pix.save(out_agent)
    print(f'  Map saved: {slug} (page {map_page_idx+1})')
    doc.close()
    return True


def build_city_stats_html(cities):
    """Build the city stats grid HTML."""
    if not cities:
        return ''
    html = '<div class="city-stats-grid" style="display: grid; grid-template-columns: 1fr 1fr; gap: 2rem; margin-top: 2rem; padding-top: 2rem; border-top: 1px solid var(--border);">'
    for city, pct in cities:
        html += f'<div style="display: flex; justify-content: space-between; padding: 0.5rem 0; border-bottom: 1px solid rgba(0,0,0,0.05);"><span style="font-weight: 600;">{city}</span><span style="color: var(--accent); font-weight: 700;">{pct}</span></div>'
    html += '</div>'
    return html


PENDING_BANNER = '''
                <!-- PENDING: Social Media Views and Feedback will be updated once data is provided -->
'''


def update_html(html, d):
    """Apply all updates to an HTML file."""

    # 1. Report period
    html = re.sub(
        r'Report Period:.*?(?=\s*</div>)',
        f'Report Period: {REPORT_PERIOD}',
        html
    )

    # 2. Days on Market card
    html = re.sub(
        r'(card-label[^>]*>Days on Market</div>\s*<div class="card-value"[^>]*>)\s*[\w/,]+\s*(\n)',
        lambda m: m.group(1) + f'\n                        {d["dom"]}\n',
        html
    )

    # 3. Last 7 Days Views card
    html = re.sub(
        r'(card-label[^>]*>Last 7 Days Views</div>\s*<div class="card-value"[^>]*>)\s*[\w/,]+',
        lambda m: m.group(1) + f'\n                        {d["last7_views"]}',
        html
    )

    # 4. Listing Views table row (last-7 and grand-total)
    html = re.sub(
        r'(metric-name[^>]*>Listing Views.*?</div>\s*<div class="last-7">)[^<]*(</div>\s*<div class="grand-total">)[^<]*(</div>)',
        lambda m: m.group(1) + str(d['last7_views']) + m.group(2) + d['grand_views'] + m.group(3),
        html, flags=re.DOTALL
    )

    # 5. Emails table row
    html = re.sub(
        r'(metric-name[^>]*>Emails Sent.*?</div>\s*<div class="last-7">)[^<]*(</div>\s*<div class="grand-total">)[^<]*(</div>)',
        lambda m: m.group(1) + d['emails_last7'] + m.group(2) + d['emails_grand'] + m.group(3),
        html, flags=re.DOTALL
    )

    # 6. Update map src with cache-busting timestamp
    html = re.sub(
        r'property_views_map_clean\.png(?:\?v=\d+)?',
        f'property_views_map_clean.png?v={CACHE_TS}',
        html
    )

    # 7. Update city stats grid
    city_html = build_city_stats_html(d['cities'])
    if city_html:
        # Replace existing city-stats-grid if present
        existing_pattern = r'<div class="city-stats-grid"[^>]*>.*?</div>\s*</div>'
        if re.search(existing_pattern, html, flags=re.DOTALL):
            html = re.sub(existing_pattern, city_html + '\n            </div>', html, flags=re.DOTALL)
        else:
            # Insert after the map img block
            html = re.sub(
                r'(property_views_map_clean\.png[^>]*>.*?</div>)',
                lambda m: m.group(1) + '\n                ' + city_html,
                html, flags=re.DOTALL
            )

    # 8. Footer date
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


def process_property(folder, d, location_base):
    html_path = os.path.join(location_base, folder, 'index.html')
    if not os.path.exists(html_path):
        print(f'  SKIP (no file): {html_path}')
        return
    with open(html_path, encoding='utf-8') as f:
        html = f.read()
    updated = update_html(html, d)
    write_file(html_path, updated)


# --- Main ---
print('=== May 11-17, 2026 Update for Joanna Jimenez properties ===\n')

for folder, data in PROPERTIES.items():
    print(f'\nProcessing: {folder}')
    
    # Extract visitor map from PDF
    extract_map(folder, data['pdf'], data['map_page'])
    
    # Update HTML in root level
    process_property(folder, data, BASE)
    
    # Update HTML in agent level
    process_property(folder, data, AGENT_BASE)

print('\n=== All done! ===')
print('NOTE: Social Media Views and Showing Feedback have NOT been updated yet.')
print('Please provide social media data and feedback to complete the update.')
