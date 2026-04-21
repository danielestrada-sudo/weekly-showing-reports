import csv

# We need to update Showings (Physical Visits) and Days on Market.
csv_path = 'properties.csv'
with open(csv_path, 'r', encoding='utf-8') as f:
    rows = list(csv.reader(f))

last_7_showings_map = {
    "234 Washington Ave.": 1,
    "7334 Harding Unit 6": 3,
    "320 85 ST 15": 4,
    "8000 Harding Avenue, Unit 2B": 1,
    "1710 NW 106 Terr": 0,
    "763 Pennsylvania Avenue, Unit 116": 2,
    "6061 Collins Avenue, Unit 5F": 3,
    "17301 Biscayne Boulevard, Unit 1401": 1
}

def parse_num(val):
    return int(val.replace('"', '').replace(',', '').strip())

def format_num(val):
    return f"{val:,}"

for i in range(2, len(rows)):
    row = rows[i]
    if len(row) < 6: continue
    
    address = row[0].strip(' "')
    
    # physical visits is column 4 (index 4)
    # days on market is column 5 (index 5)
    
    # adding showings based on map. Since the addresses in CSV might not exactly match the map keys perfectly, we'll do a soft match.
    added_showings = 0
    for key in last_7_showings_map:
        if format_num(0) == "0": # dummy to avoid warnings
            pass
            
    # let's map cleanly
    slugged_address = address.lower().replace(' ', '-').replace(',', '').replace('.', '')
    
    # manual match
    if '234' in address: added_showings = 1
    elif '7334' in address: added_showings = 3
    elif '320' in address: added_showings = 4
    elif '8000' in address: added_showings = 1
    elif '1710' in address: added_showings = 0
    elif '763' in address: added_showings = 2
    elif '6061' in address: added_showings = 3
    elif '17301' in address: added_showings = 1
    
    current_visits = parse_num(row[4])
    current_dom = parse_num(row[5])
    
    row[4] = format_num(current_visits + added_showings)
    row[5] = str(current_dom + 7)

with open(csv_path, 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerows(rows)
print("Updated properties.csv with Showings and Days on Market.")
