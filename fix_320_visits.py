import csv

csv_path = 'properties.csv'
with open(csv_path, 'r', encoding='utf-8') as f:
    rows = list(csv.reader(f))

def parse_num(val):
    return int(val.replace('"', '').replace(',', '').strip())

def format_num(val):
    return f"{val:,}"

for i in range(2, len(rows)):
    row = rows[i]
    if len(row) < 6: continue
    address = row[0].strip(' "')
    if '320' in address:
        current = parse_num(row[2])
        new_val = current + 150
        row[2] = format_num(new_val)
        print(f"Updated 320 85 ST online visits: {current} + 150 = {new_val}")
        break

with open(csv_path, 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerows(rows)
print("Done.")
