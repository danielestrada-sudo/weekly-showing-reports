import re, os

path = r'C:\Users\Daniel Estrada\.gemini\antigravity\scratch\weekly-showing-reports\agents\natalia-figueroa\1650-coral-way-unit-607\index.html'
with open(path, encoding='utf-8') as f:
    html = f.read()

# Update Last 7 Days Views card
html = re.sub(
    r'(card-label[^>]*>Last 7 Days Views</div>\s*<div class="card-value[^>]*>\s*)0',
    r'\1 91\n                        <span class="card-change">Updated</span>',
    html
)

# Update Listing Views table
html = re.sub(
    r'(metric-name[^>]*>Listing Views \(Online\).*?</div>\s*<div class="last-7">)0(</div>\s*<div class="grand-total">)0(</div>)',
    r'\g<1>91\g<2>91\g<3>',
    html
)

# Update Emails table
html = re.sub(
    r'(metric-name[^>]*>Emails Sent.*?</div>\s*<div class="last-7">)0(</div>\s*<div class="grand-total">)0(</div>)',
    r'\g<1>+8,049\g<2>8,049\g<3>',
    html
)

# Update map section
map_html = '''<img src="property_views_map_clean.png?v=20260526" alt="Visitor Locations Map" style="width:100%; border-radius: 8px;">
                <div class="city-stats-grid" style="display: grid; grid-template-columns: 1fr 1fr; gap: 2rem; margin-top: 2rem; padding-top: 2rem; border-top: 1px solid var(--border);">
                    <div style="display: flex; justify-content: space-between; padding: 0.5rem 0; border-bottom: 1px solid rgba(0,0,0,0.05);"><span style="font-weight: 600;">Miami</span><span style="color: var(--accent); font-weight: 700;">50%</span></div>
                    <div style="display: flex; justify-content: space-between; padding: 0.5rem 0; border-bottom: 1px solid rgba(0,0,0,0.05);"><span style="font-weight: 600;">Miami Beach</span><span style="color: var(--accent); font-weight: 700;">12.5%</span></div>
                    <div style="display: flex; justify-content: space-between; padding: 0.5rem 0; border-bottom: 1px solid rgba(0,0,0,0.05);"><span style="font-weight: 600;">Detroit</span><span style="color: var(--accent); font-weight: 700;">11.3%</span></div>
                    <div style="display: flex; justify-content: space-between; padding: 0.5rem 0; border-bottom: 1px solid rgba(0,0,0,0.05);"><span style="font-weight: 600;">Los Angeles</span><span style="color: var(--accent); font-weight: 700;">3.8%</span></div>
                    <div style="display: flex; justify-content: space-between; padding: 0.5rem 0; border-bottom: 1px solid rgba(0,0,0,0.05);"><span style="font-weight: 600;">Fort Lauderdale</span><span style="color: var(--accent); font-weight: 700;">3.8%</span></div>
                    <div style="display: flex; justify-content: space-between; padding: 0.5rem 0; border-bottom: 1px solid rgba(0,0,0,0.05);"><span style="font-weight: 600;">Pompano Beach</span><span style="color: var(--accent); font-weight: 700;">2.5%</span></div>
                    <div style="display: flex; justify-content: space-between; padding: 0.5rem 0; border-bottom: 1px solid rgba(0,0,0,0.05);"><span style="font-weight: 600;">Chicago</span><span style="color: var(--accent); font-weight: 700;">2.5%</span></div>
                </div>'''

html = re.sub(
    r'<div class="empty-map">[\s\S]*?Location Data Unavailable[\s\S]*?</div>',
    map_html,
    html
)

with open(path, 'w', encoding='utf-8') as f:
    f.write(html)
print('Updated 1650 Coral Way HTML.')
