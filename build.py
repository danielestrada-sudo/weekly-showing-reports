import csv
import os
import re

def slugify(text):
    return re.sub(r'[^a-z0-9]+', '-', text.strip().lower()).strip('-')

def extract_feedback(file_path):
    pass  # Replaced by build_feedback_html()

def get_property_specs(address):
    # Mapping arbitrary specs based on whatever we have, since CSV doesn't have it
    if 'Washington' in address: return "3 Bedrooms | Attached Garage", "MLS #A11888151"
    if 'Unit' in address or 'UNIT' in address: return "Condo", "MLS #Pending"
    return "Property Details", "MLS #Pending"

# Feedback entries per property, newest first
PROPERTY_FEEDBACK = {
    "234-washington-ave": [
        ("Apr 13 - Apr 19, 2026", "Client looking for second home in Miami - the wife lived here for 10+ years but they now live in Hawaii. He thinks the home is great but has concerns over the split levels. He thinks they are a little too much for their 2 year old and 7 week old. He think the most they could do is two levels."),
        ("Apr 6 - Apr 12, 2026", "10 People attended the Open House this past weekend. Overall, the feedback was very positive\u2014most described the property as beautiful, well-designed, and well-maintained. The entrance was a major highlight, along with the two parking spaces. One agent followed up afterward and mentioned that while they liked the property and are interested in bringing their client, they did notice a slight odor in the bedroom area. Despite that, they are still considering showing it to their client. I will follow up to see if they move forward. Working to schedule a showing with a family who previously showed strong interest, along with their parents, who will be funding the purchase."),
        ("Mar 30 - Apr 3, 2026", "There were two showing requests last week; however, both were declined as no showings were permitted at that time. I am currently coordinating with the agents to reschedule."),
        ("Mar 9, 2026", "No showings last week. Will plan third showing for family that saw it last week for a time next week. We received one inquiry from a client who lives in NYC and is interested in scheduling a FaceTime."),
        ("Mar 16, 2026", "Two showings took place last week. One private showing occurred on Friday with a client who lives in the area and walks by the property frequently. He liked the home a lot but wanted to discuss it with his business partner and family before making a decision. The other private showing took place on Monday. Their agent inquired about the 'odor' in the home. He said his clients liked it, but overall felt as though it was too small for their family."),
    ],
    "7334-harding-unit-6": [
        ("Apr 13 - Apr 19, 2026", "3 Private showings last week. 2 for rent and 1 for purchase. The rental showings went well but they want to see more options before making a decision. The showing for purchase also went well. The buyer is an older woman and is all cash. Her family is deciding if the property is a good fit due to laundry outside and the stairs in front and back. They liked the location a lot too."),
    ],
    "320-85-st-15": [
        ("Apr 13 - Apr 19, 2026", "One offer Received. Another said they were interested in submitting one but has not sent us anything."),
    ],
    "8000-harding-avenue-unit-2b": [
        ("Apr 13 - Apr 19, 2026", "Buyer liked it, but it worried it is too dark due to the unit being on the second floor. He is exploring his options further."),
    ],
    "1710-nw-106-terr": [
        ("Apr 13 - Apr 19, 2026", "No showings this week."),
    ],
    "763-pennsylvania-avenue-unit-116": [
        ("Apr 13 - Apr 19, 2026", "2 Showing request last week but could not accommodate the scheduled times."),
    ],
    "6061-collins-avenue-unit-5f": [
        ("Apr 13 - Apr 19, 2026", "Friday 10:30 am: Loved the view and the spacious floorplan. Did not like the building nor amenities.<br><br>Friday 10:45: Loved the ocean view and the three balconies, they are ok with waiting on the building to renovate but did not like the value of the monthly HOA payments.<br><br>Friday 1 pm: Buyer took video of the views because he really loved the idea of having three balconies all facing the ocean. He sees a potential in the building, and it's OK to wait until everything is done because the property is for himself."),
    ],
    "17301-biscayne-boulevard-unit-1401": [
        ("Apr 13 - Apr 19, 2026", "Realtor brought her client who flew in to see this unit. Client loved how spacious the balcony is and loved the building amenities. They had more options to see in the same building - agent wants to know more about the HOA reduction in the future."),
    ],
}

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

last_7_showings_map = {
    "234-washington-ave": "1",
    "7334-harding-unit-6": "3",
    "320-85-st-15": "4",
    "8000-harding-avenue-unit-2b": "1",
    "1710-nw-106-terr": "0",
    "763-pennsylvania-avenue-unit-116": "2",
    "6061-collins-avenue-unit-5f": "3",
    "17301-biscayne-boulevard-unit-1401": "1"
}

# Online views extracted from Progress Report PDFs (Apr 13-19, 2026)
last_7_online_map = {
    "234-washington-ave": "224",
    "7334-harding-unit-6": "144",
    "320-85-st-15": "150",
    "8000-harding-avenue-unit-2b": "147",
    "1710-nw-106-terr": "326",
    "763-pennsylvania-avenue-unit-116": "236",
    "6061-collins-avenue-unit-5f": "512",
    "17301-biscayne-boulevard-unit-1401": "356"
}

def build():
    with open('template.html', 'r', encoding='utf-8') as f:
        template = f.read()

    with open('properties.csv', 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        rows = list(reader)

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
        feedback = build_feedback_html(slug)
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
        
        # New Last 7 Days metrics
        showings = last_7_showings_map.get(slug, "0")
        if showings == "0":
            showings_display = "0"
        else:
            showings_display = "+" + showings
        
        online_7 = last_7_online_map.get(slug, None)
        online_7_display = online_7 if online_7 else 'N/A'
            
        html = html.replace('{{LAST_7_ONLINE_TABLE}}', online_7_display)
        html = html.replace('{{LAST_7_SHOWINGS}}', showings_display)
        html = html.replace('{{LAST_7_PHYSICAL_TABLE}}', showings_display)
        html = html.replace('{{LAST_7_EMAILS_TABLE}}', '4,618')
        html = html.replace('{{LAST_7_SOCIAL_TABLE}}', '444')
        html = html.replace('{{PROPERTY_SLUG}}', slug)
        html = html.replace('{{MAP_SRC}}', 'property_views_map_clean.png')

        with open(index_path, 'w', encoding='utf-8') as out:
            out.write(html)
        print(f"Generated {slug}/index.html")

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
