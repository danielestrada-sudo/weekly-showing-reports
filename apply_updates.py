import csv
import re
import os

# 1. Update properties.csv
csv_path = 'properties.csv'
with open(csv_path, 'r', encoding='utf-8') as f:
    rows = list(csv.reader(f))

# The first row is a note, second is header.
# properties.csv columns: Property Address,Total Social Views,Total Online Visits,Total Emails Opened,Total Physical Visits,Days On Market

def parse_num(val):
    return int(val.replace('"', '').replace(',', '').strip())

def format_num(val):
    return f"{val:,}"

for i in range(2, len(rows)):
    row = rows[i]
    if len(row) < 6: continue
    # "Total Social Views" => row[1]
    # "Total Emails Opened" => row[3]
    social = parse_num(row[1]) + 444
    emails = parse_num(row[3]) + 4618
    row[1] = format_num(social)
    row[3] = format_num(emails)
    
with open(csv_path, 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerows(rows)
print("Updated properties.csv")

# 2. Update Feedback in index.html for specific properties
feedbacks = {
    "6061-collins-avenue-unit-5f": "Friday 10:30 am: Loved the view and the spacious floorplan. Did not like the building nor amenities.<br><br>Friday 10:45: Loved the ocean view and the three balconies, they are ok with waiting on the building to renovate but did not like the value of the monthly HOA payments.<br><br>Friday 1 pm: Buyer took video of the views because he really loved the idea of having three balconies all facing the ocean. He sees a potential in the building, and it’s OK to wait until everything is done because the property is for himself.",
    "17301-biscayne-boulevard-unit-1401": "Realtor brought her client who flew in to see this unit. Client loved how spacious the balcony is and loved the building amenities. They had more options to see in the same building - agent wants to know more about the HOA reduction in the future.",
    "320-85-st-15": "One offer Received. Another said they were interested in submitting one but has not sent us anything.",
    "7334-harding-unit-6": "3 Private showings last week. 2 for rent and 1 for purchase. The rental showings went well but they want to see more options before making a decision. The showing for purchase also went well. The buyer is an older woman and is all cash. Her family is deciding if the property is a good fit due to laundry outside and the stairs in front and back. They liked the location at lot too.",
    "8000-harding-avenue-unit-2b": "Buyer liked it, but it worried it is too dark due to the unit being on the second floor. He is exploring his options further.",
    "763-pennsylvania-avenue-unit-116": "2 Showing request last week but could not accommodate the scheduled times."
}

def inject_feedback(slug, feedback_text):
    folder = os.path.join(os.getcwd(), slug)
    index_path = os.path.join(folder, 'index.html')
    if not os.path.exists(index_path):
        print(f"Skipping {slug}, no index.html found.")
        return

    with open(index_path, 'r', encoding='utf-8') as f:
        content = f.read()

    new_feedback_html = f'''<div class="feedback-item">
                    <div class="feedback-text">
                        "{feedback_text}"
                        <span class="agent-date" style="display: block; margin-top: 0.5rem; font-style: normal;">— Apr 13 - Apr 19, 2026</span>
                    </div>
                </div>'''

    # Find the feedback card where the items are listed
    # We want to insert the new feedback item at the top of the <div class="card"> inside <div id="feedback" ...>
    
    match = re.search(r'(<div id="feedback" class="tab-content">.*?<div class="card">)', content, re.DOTALL)
    if match:
        insertion_point = match.end()
        # insert right after <div class="card">
        # wait! need to check if the exact feedback was already inserted to avoid dupes!
        if 'Apr 13 - Apr 19, 2026' in content:
            print(f"Feedback already exists in {slug}")
        else:
            updated_content = content[:insertion_point] + '\n                ' + new_feedback_html + '\n' + content[insertion_point:]
            with open(index_path, 'w', encoding='utf-8') as f:
                f.write(updated_content)
            print(f"Added feedback to {slug}")
    else:
        print(f"Could not find feedback section in {slug}")

for slug, text in feedbacks.items():
    inject_feedback(slug, text)

