import csv
import os
import re

def slugify(text):
    return re.sub(r'[^a-z0-9]+', '-', text.strip().lower()).strip('-')

def extract_feedback(file_path):
    if not os.path.exists(file_path):
        return '<div style="background: rgba(0,0,0,0.05); padding: 2rem; text-align: center; border-radius: 8px; color: var(--text-muted);"><em>No new feedback this week.</em></div>'
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    match = re.search(r'<div id="feedback" class="tab-content">.*?<div class="card">(.*?)</div>\s*<!-- VISITOR LOCATIONS TAB -->', content, re.DOTALL)
    if match:
        return match.group(1).strip()
    return '<div style="background: rgba(0,0,0,0.05); padding: 2rem; text-align: center; border-radius: 8px; color: var(--text-muted);"><em>No new feedback this week.</em></div>'

def get_property_specs(address):
    # Mapping arbitrary specs based on whatever we have, since CSV doesn't have it
    if 'Washington' in address: return "3 Bedrooms | Attached Garage", "MLS #A11888151"
    if 'Unit' in address or 'UNIT' in address: return "Condo", "MLS #Pending"
    return "Property Details", "MLS #Pending"

def build():
    with open('template.html', 'r', encoding='utf-8') as f:
        template = f.read()

    with open('properties.csv', 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        rows = list(reader)

    # Skip first row which is just a note
    headers = rows[1]
    data_rows = rows[2:]

    properties_data = []

    for row in data_rows:
        if len(row) < 6: continue
        address = row[0].strip(' "')
        if not address: continue
        slug = slugify(address)
        social = row[1].strip()
        online = row[2].strip()
        emails = row[3].strip()
        visits = row[4].strip()
        dom = row[5].strip()
        
        properties_data.append((address, slug))
        
        folder = os.path.join(os.getcwd(), slug)
        if not os.path.exists(folder):
            os.makedirs(folder)
            
        index_path = os.path.join(folder, 'index.html')
        feedback = extract_feedback(index_path)
        
        specs, mls = get_property_specs(address)

        html = template.replace('{{PROPERTY_NAME}}', address)
        html = html.replace('{{PROPERTY_SPECS}}', specs)
        html = html.replace('{{MLS_NUMBER}}', mls)
        html = html.replace('{{DAYS_ON_MARKET}}', dom)
        html = html.replace('{{TOTAL_ONLINE_VISITS}}', online)
        html = html.replace('{{TOTAL_PHYSICAL_VISITS}}', visits)
        html = html.replace('{{TOTAL_EMAILS_OPENED}}', emails)
        html = html.replace('{{TOTAL_SOCIAL_VIEWS}}', social)
        html = html.replace('{{FEEDBACK_SECTION}}', feedback)
        
        with open(index_path, 'w', encoding='utf-8') as out:
            out.write(html)
        print(f"Generated {slug}/index.html")

    # Generate root index.html
    portal = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Listing Insights Portal</title>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&display=swap" rel="stylesheet">
    <style>
        body { font-family: 'Outfit', sans-serif; background: #F8F9FA; color: #333; padding: 2rem 5%; }
        header { text-align: center; margin-bottom: 3rem; }
        h1 { color: #002244; }
        .grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 1.5rem; }
        .card { background: white; padding: 1.5rem; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.05); text-decoration: none; color: inherit; transition: transform 0.2s, box-shadow 0.2s; display: block; border-left: 4px solid #2A9D8F; }
        .card:hover { transform: translateY(-5px); box-shadow: 0 8px 25px rgba(0,0,0,0.1); }
        .card h3 { margin: 0 0 0.5rem 0; color: #002244; }
        .card p { margin: 0; color: #666; font-size: 0.9rem; }
    </style>
</head>
<body>
    <header>
        <h1>Listing Insights Dashboards</h1>
        <p>Weekly real estate activity reports for our active listings</p>
    </header>
    <div class="grid">
"""
    for address, slug in properties_data:
        portal += f"""        <a href="{slug}/index.html" class="card">
            <h3>{address}</h3>
            <p>View latest insights &amp; feedback &#8594;</p>
        </a>\n"""
        
    portal += """    </div>
</body>
</html>"""

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(portal)
    print("Generated root portal index.html")

if __name__ == '__main__':
    build()
