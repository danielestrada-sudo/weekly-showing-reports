import csv
import os
import re
import json

def slugify(text):
    return re.sub(r'[^a-z0-9]+', '-', text.strip().lower()).strip('-')

# Load weekly data from central JSON file
with open('weekly_data.json', 'r', encoding='utf-8') as f:
    DATA = json.load(f)

PROPERTY_FEEDBACK = DATA['PROPERTY_FEEDBACK']
last_7_showings_map = DATA['last_7_showings_map']
last_7_online_map = DATA['last_7_online_map']
last_7_social_map = DATA['last_7_social_map']
last_7_emails_map = DATA['last_7_emails_map']
PROPERTY_CITY_STATS = DATA['PROPERTY_CITY_STATS']

def get_property_specs(address):
    # Mapping arbitrary specs based on whatever we have
    if 'Washington' in address: return "3 Bedrooms | Attached Garage", "MLS #A11888151"
    if 'Unit' in address or 'UNIT' in address: return "Condo", "MLS #Pending"
    return "Property Details", "MLS #Pending"

def build_feedback_html(slug):
    entries = PROPERTY_FEEDBACK.get(slug, [])
    if not entries:
        return '<div style="background: rgba(0,0,0,0.05); padding: 2rem; text-align: center; border-radius: 8px; color: var(--text-muted);"><em>No new feedback this week.</em></div>'
    html = ''
    for date, text in entries:
        html += f'''<div class="feedback-item">
                    <div class="feedback-text">
                        "{text}"
                        <span class="agent-date" style="display: block; margin-top: 0.5rem; font-style: normal;">\u2014 {date}</span>
                    </div>
                </div>\n\n                '''
    return html.rstrip()

def build_city_stats_html(slug):
    stats = PROPERTY_CITY_STATS.get(slug, [])
    if not stats: return ""
    
    html = '<div class="city-stats-grid" style="display: grid; grid-template-columns: 1fr 1fr; gap: 2rem; margin-top: 2rem; padding-top: 2rem; border-top: 1px solid var(--border);">'
    for city, val in stats:
        html += f'''<div style="display: flex; justify-content: space-between; padding: 0.5rem 0; border-bottom: 1px solid rgba(0,0,0,0.05);">
                    <span style="font-weight: 600;">{city}</span>
                    <span style="color: var(--accent); font-weight: 700;">{val}</span>
                </div>'''
    html += "</div>"
    return html

AGENTS_INFO = {
    "Joanna Jimenez": {"phone": "(305) 302-6384", "email": "joanna.jimenez@compass.com"},
    "Adriana Briceno": {"phone": "(346) 332-3869", "email": "adriana.briceno@compass.com"},
    "Sheree Saint Victor": {"phone": "(754) 971-7771", "email": "danica.noynay@compass.com"},
    "Anna Jimenez": {"phone": "(305) 322-3223", "email": "anna.jimenez@compass.com"},
    "Lilibeth Villanueva": {"phone": "(786) 395-0502", "email": "lilibeth.basagoitia@compass.com"},
    "Rafael Beltran": {"phone": "(954) 544-6816", "email": "rafael.beltran@compass.com"},
    "Carlos Rospigliosi": {"phone": "(305) 904-8048", "email": "carlos.rospigliosi@compass.com"},
    "Karina Reyes": {"phone": "(786) 554-0814", "email": "connor.weiss@compass.com"}
}

def build():
    with open('template.html', 'r', encoding='utf-8') as f:
        template = f.read()

    with open('properties.csv', 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        rows = list(reader)

    # Find the Agent column index
    agent_col_idx = -1
    if len(rows) > 1:
        headers = rows[1]
        for idx, h in enumerate(headers):
            if 'Agent' in h:
                agent_col_idx = idx
                break

    data_rows = rows[2:]
    agents_properties = {} # agent -> [(address, slug, data)]

    for row in data_rows:
        if len(row) < 6: continue
        address = row[0].strip(' "')
        if not address: continue
        
        agent_name = row[agent_col_idx].strip() if agent_col_idx != -1 and len(row) > agent_col_idx else "Joanna Jimenez"
        agent_slug = slugify(agent_name)
        
        slug = slugify(address)
        social = row[1].strip()
        online = row[2].strip()
        emails = row[3].strip()
        visits = row[4].strip()
        dom = row[5].strip()
        
        if agent_name not in agents_properties:
            agents_properties[agent_name] = []
        agents_properties[agent_name].append({
            "address": address,
            "slug": slug,
            "social": social,
            "online": online,
            "emails": emails,
            "visits": visits,
            "dom": dom,
            "agent_slug": agent_slug
        })

    # Generate Property Reports
    for agent_name, props in agents_properties.items():
        agent_info = AGENTS_INFO.get(agent_name, {"phone": "N/A", "email": "N/A"})
        agent_slug = slugify(agent_name)
        
        agent_dir = os.path.join(os.getcwd(), 'agents', agent_slug)
        if not os.path.exists(agent_dir):
            os.makedirs(agent_dir)

        for p in props:
            prop_dir = os.path.join(agent_dir, p['slug'])
            if not os.path.exists(prop_dir):
                os.makedirs(prop_dir)
            
            # Map handling
            legacy_map = os.path.join(os.getcwd(), p['slug'], 'property_views_map_clean.png')
            dest_map = os.path.join(prop_dir, 'property_views_map_clean.png')
            if os.path.exists(legacy_map) and not os.path.exists(dest_map):
                import shutil
                shutil.copy(legacy_map, dest_map)

            feedback = build_feedback_html(p['slug'])
            specs, mls = get_property_specs(p['address'])

            html = template.replace('{{PROPERTY_NAME}}', p['address'])
            html = html.replace('{{PROPERTY_SPECS}}', specs)
            html = html.replace('{{MLS_NUMBER}}', mls)
            html = html.replace('{{DAYS_ON_MARKET}}', p['dom'])
            html = html.replace('{{TOTAL_ONLINE_VISITS}}', p['online'])
            html = html.replace('{{TOTAL_PHYSICAL_VISITS}}', p['visits'])
            html = html.replace('{{TOTAL_EMAILS_OPENED}}', p['emails'])
            html = html.replace('{{TOTAL_SOCIAL_VIEWS}}', p['social'])
            html = html.replace('{{FEEDBACK_SECTION}}', feedback)
            
            # Agent Info
            html = html.replace('{{AGENT_NAME}}', agent_name)
            html = html.replace('{{AGENT_PHONE}}', agent_info['phone'])
            html = html.replace('{{AGENT_EMAIL}}', agent_info['email'])
            
            # New Last 7 Days metrics
            showings = last_7_showings_map.get(p['slug'], "0")
            showings_display = "+" + showings if showings != "0" else "0"
            
            online_7 = last_7_online_map.get(p['slug'], 'N/A')
                
            html = html.replace('{{LAST_7_ONLINE_TABLE}}', online_7)
            html = html.replace('{{LAST_7_SHOWINGS}}', showings_display)
            html = html.replace('{{LAST_7_PHYSICAL_TABLE}}', showings_display)
            html = html.replace('{{LAST_7_EMAILS_TABLE}}', last_7_emails_map.get(p['slug'], '3,267'))
            html = html.replace('{{LAST_7_SOCIAL_TABLE}}', last_7_social_map.get(p['slug'], '222'))
            html = html.replace('{{PROPERTY_SLUG}}', p['slug'])
            html = html.replace('{{MAP_SRC}}', 'property_views_map_clean.png')
            html = html.replace('{{CITY_STATS_TABLE}}', build_city_stats_html(p['slug']))

            with open(os.path.join(prop_dir, 'index.html'), 'w', encoding='utf-8') as out:
                out.write(html)
            print(f"Generated {agent_slug}/{p['slug']}/index.html")

    # Generate Agent Portals
    for agent_name in AGENTS_INFO.keys():
        agent_slug = slugify(agent_name)
        props = agents_properties.get(agent_name, [])
        
        agent_dir = os.path.join(os.getcwd(), 'agents', agent_slug)
        if not os.path.exists(agent_dir):
            os.makedirs(agent_dir)

        portal_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{agent_name} | Listing Insights</title>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&display=swap" rel="stylesheet">
    <style>
        body {{ font-family: 'Outfit', sans-serif; background: #F8F9FA; color: #333; padding: 2rem 5%; }}
        header {{ text-align: center; margin-bottom: 3rem; }}
        h1 {{ color: #002244; }}
        .grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 1.5rem; }}
        .card {{ background: white; padding: 1.5rem; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.05); text-decoration: none; color: inherit; transition: transform 0.2s, box-shadow 0.2s; display: block; border-left: 4px solid #2A9D8F; }}
        .card:hover {{ transform: translateY(-5px); box-shadow: 0 8px 25px rgba(0,0,0,0.1); }}
        .card h3 {{ margin: 0 0 0.5rem 0; color: #002244; }}
        .card p {{ margin: 0; color: #666; font-size: 0.9rem; }}
        .back-link {{ display: inline-block; margin-bottom: 2rem; color: #002244; text-decoration: none; font-weight: 600; }}
    </style>
</head>
<body>
    <a href="../../index.html" class="back-link">&#8592; Main Portal</a>
    <header>
        <h1>{agent_name}</h1>
        <p>Active Listing Dashboards</p>
    </header>
    <div class="grid">
"""
        for p in props:
            portal_html += f"""        <a href="{p['slug']}/index.html" class="card">
            <h3>{p['address']}</h3>
            <p>View latest insights &amp; feedback &#8594;</p>
        </a>\n"""
        
        portal_html += """    </div>
</body>
</html>"""
        with open(os.path.join(os.getcwd(), 'agents', agent_slug, 'index.html'), 'w', encoding='utf-8') as f:
            f.write(portal_html)

    # Generate Root Portal
    root_portal = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Compass One | Listing Insights Portal</title>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&display=swap" rel="stylesheet">
    <style>
        body { font-family: 'Outfit', sans-serif; background: #002244; color: white; padding: 4rem 5%; min-height: 100vh; display: flex; flex-direction: column; align-items: center; justify-content: center; }
        header { text-align: center; margin-bottom: 4rem; }
        h1 { font-size: 3rem; margin-bottom: 1rem; }
        .grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 2rem; width: 100%; max-width: 1000px; }
        .card { background: rgba(255,255,255,0.1); backdrop-filter: blur(10px); padding: 2.5rem; border-radius: 20px; text-decoration: none; color: white; transition: all 0.3s ease; text-align: center; border: 1px solid rgba(255,255,255,0.1); }
        .card:hover { background: white; color: #002244; transform: translateY(-10px); }
        .card h3 { font-size: 1.5rem; margin-bottom: 0.5rem; }
        .card p { opacity: 0.8; }
    </style>
</head>
<body>
    <header>
        <h1>Agent Portals</h1>
        <p>Select an agent to view their property performance dashboards</p>
    </header>
    <div class="grid">
"""
    for agent_name in sorted(AGENTS_INFO.keys()):
        agent_slug = slugify(agent_name)
        props = agents_properties.get(agent_name, [])
        count = len(props)
        root_portal += f"""        <a href="agents/{agent_slug}/index.html" class="card">
            <h3>{agent_name}</h3>
            <p>{count} Active Listings &#8594;</p>
        </a>\n"""
        
    root_portal += """    </div>
</body>
</html>"""
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(root_portal)
    print("Generated Multi-Agent Portal system")

if __name__ == '__main__':
    build()
