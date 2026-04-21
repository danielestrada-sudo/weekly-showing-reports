import re, os

properties = [
    "234-washington-ave",
    "7334-harding-unit-6",
    "320-85-st-15",
    "8000-harding-avenue-unit-2b",
    "1710-nw-106-terr",
    "763-pennsylvania-avenue-unit-116",
    "6061-collins-avenue-unit-5f",
    "17301-biscayne-boulevard-unit-1401"
]

for slug in properties:
    path = os.path.join(slug, "index.html")
    if not os.path.exists(path):
        print(f"{slug}: FILE NOT FOUND")
        continue
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    feedback_items = len(re.findall(r'<div class="feedback-item">', content))
    has_no_feedback = "No new feedback" in content
    # Find the img src for the map
    maps = re.findall(r'src="([^"]+\.png)"', content)
    print(f"{slug}:")
    print(f"  feedback-items: {feedback_items}, no-feedback-placeholder: {has_no_feedback}")
    print(f"  map srcs: {maps}")
    print()
