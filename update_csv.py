import csv
import os
import re

def parse_num(val):
    if not val or val == 'N/A' or val == 'NA': return 0
    return int(val.replace('"', '').replace(',', '').strip())

def format_num(val):
    return f"{val:,}"

updates = {
    "234": {"social": 3267, "online": 171, "emails": 222, "showings": 0, "dom_add": 7},
    "7334": {"social": 3267, "online": 134, "emails": 222, "showings": 2, "dom_add": 7},
    "320": {"social": 3267, "online": 153, "emails": 222, "showings": 4, "dom_add": 7},
    "8000": {"social": 3267, "online": 83, "emails": 222, "showings": 0, "dom_add": 7},
    "1710": {"social": 3267, "online": 69, "emails": 222, "showings": 0, "dom_add": 7},
    "763": {"social": 3267, "online": 169, "emails": 222, "showings": 1, "dom_add": 7},
    "6061": {"social": 5223, "online": 337, "emails": 222, "showings": 2, "dom_add": 7},
    "17301": {"social": 3219, "online": 147, "emails": 222, "showings": 2, "dom_add": 7},
}

csv_path = 'properties.csv'
with open(csv_path, 'r', encoding='utf-8') as f:
    rows = list(csv.reader(f))

for i in range(2, len(rows)):
    row = rows[i]
    if len(row) < 6: continue
    address = row[0].strip(' "')
    if not address: continue
    
    key = None
    for k in updates:
        if k in address:
            key = k
            break
            
    if key:
        row[1] = format_num(parse_num(row[1]) + updates[key]["social"])
        row[2] = format_num(parse_num(row[2]) + updates[key]["online"])
        row[3] = format_num(parse_num(row[3]) + updates[key]["emails"])
        row[4] = str(parse_num(row[4]) + updates[key]["showings"])
        row[5] = str(parse_num(row[5]) + updates[key]["dom_add"])

with open(csv_path, 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerows(rows)
    
print("Updated properties.csv")
