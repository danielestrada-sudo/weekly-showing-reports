import csv

def parse_num(val): return int(val.replace('"', '').replace(',', '').strip())
def format_num(val): return f"{val:,}"

csv_path = 'properties.csv'
with open(csv_path, 'r', encoding='utf-8') as f:
    rows = list(csv.reader(f))

for i in range(2, len(rows)):
    row = rows[i]
    if len(row) < 6: continue
    address = row[0].strip(' "')
    if not address: continue
    
    # 1. We incorrectly added 222 emails. We want to add 3267. Difference is +3045.
    row[3] = format_num(parse_num(row[3]) + 3045)
    
    # 2. For social, if it's NOT 6061 and NOT 17301, we added 3267 but we wanted 222.
    # Difference is -3045.
    if '6061' not in address and '17301' not in address:
        row[1] = format_num(parse_num(row[1]) - 3045)

with open(csv_path, 'w', newline='', encoding='utf-8') as f:
    csv.writer(f).writerows(rows)
print("CSV fixed")
