import csv
import os
import shutil
import re

# === STEP 1: Update Online Visits in properties.csv ===

# Extracted from Progress Reports (13 Apr - 19 Apr 2026)
last_7_online_views = {
    "234": 224,
    "7334": 144,
    "320": None,       # No progress report for 320 85 ST
    "8000": 147,
    "1710": 326,
    "763": 236,
    "6061": 512,
    "17301": 356,
}

csv_path = 'properties.csv'
with open(csv_path, 'r', encoding='utf-8') as f:
    rows = list(csv.reader(f))

def parse_num(val):
    return int(val.replace('"', '').replace(',', '').strip())

def format_num(val):
    return f"{val:,}"

print("Updating properties.csv with Online Visits...")
for i in range(2, len(rows)):
    row = rows[i]
    if len(row) < 6: continue
    address = row[0].strip(' "')
    if not address: continue
    
    current_online = parse_num(row[2])
    
    for key, visits in last_7_online_views.items():
        if key in address and visits is not None:
            new_total = current_online + visits
            row[2] = format_num(new_total)
            print(f"  {address}: {current_online} + {visits} = {new_total}")
            break

with open(csv_path, 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerows(rows)

print("\nDone updating CSV.")

# === STEP 2: Copy visitor maps to property folders ===

map_src_dir = 'visitor_maps'

property_map_mapping = {
    "234-washington-ave": "234_washington_avenue__unit_a.png",
    "7334-harding-unit-6": "7334_harding_avenue__unit_6.png",
    "320-85-st-15": None,  # No report
    "8000-harding-avenue-unit-2b": "8000_harding_avenue__unit_2b.png",
    "1710-nw-106-terr": "1710_northwest_106th.png",
    "763-pennsylvania-avenue-unit-116": "763_pennsylvania.png",
    "6061-collins-avenue-unit-5f": "6061_collins_avenue__unit_5f.png",
    "17301-biscayne-boulevard-unit-1401": "17301_biscayne.png",
}

print("\nCopying visitor maps to property folders...")
for slug, map_file in property_map_mapping.items():
    if map_file is None:
        print(f"  {slug}: No map available (skipping)")
        continue
    
    src = os.path.join(map_src_dir, map_file)
    dest_dir = slug
    dest = os.path.join(dest_dir, 'property_views_map_clean.png')
    
    if os.path.exists(src) and os.path.exists(dest_dir):
        shutil.copy2(src, dest)
        print(f"  Copied map to {dest}")
    else:
        print(f"  MISSING: {src} or {dest_dir}")

print("\nAll done!")
