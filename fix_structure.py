import re

# 1. Fix template.html
with open('template.html', 'r', encoding='utf-8') as f:
    template = f.read()

# Replace the broken comment line with a properly structured one
template = template.replace(
    '{{FEEDBACK_SECTION}}<!-- VISITOR LOCATIONS TAB -->',
    '{{FEEDBACK_SECTION}}\n            </div>\n        </div>\n        <!-- VISITOR LOCATIONS TAB -->'
)

with open('template.html', 'w', encoding='utf-8') as f:
    f.write(template)

# 2. Fix build.py so extract_feedback gets ONLY the inside of the card.
with open('build.py', 'r', encoding='utf-8') as f:
    build_py = f.read()

# Replace the extract_feedback function
new_extract_func = '''def extract_feedback(file_path):
    if not os.path.exists(file_path):
        return '<div style="background: rgba(0,0,0,0.05); padding: 2rem; text-align: center; border-radius: 8px; color: var(--text-muted);"><em>No new feedback this week.</em></div>'
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    # The new robust regex targets what is INSIDE the <div class="card"> in the feedback tab.
    # It stops before the very first </div> corresponding to the card end, or whatever text is there.
    # Actually, a simpler way is finding all feedback items or the "No new feedback" message.
    if '<div class="feedback-item">' in content:
        # Extract all feedback items. They are between <div class="card"> and </div></div>
        match = re.search(r\'<div id="feedback" class="tab-content">.*?<div class="card">(.*?)</div>\\s*</div>\\s*<!-- VISITOR LOCATIONS TAB -->\', content, re.DOTALL)
        if match:
            return match.group(1).strip()
        # Fallback if the file is broken (no closing divs)
        match = re.search(r\'<div id="feedback" class="tab-content">.*?<div class="card">(.*?)(?:<!-- VISITOR LOCATIONS TAB -->|</div>\\s*</div>)\', content, re.DOTALL)
        if match:
            return match.group(1).strip()
    return '<div style="background: rgba(0,0,0,0.05); padding: 2rem; text-align: center; border-radius: 8px; color: var(--text-muted);"><em>No new feedback this week.</em></div>'
'''

# Use regex to replace the function in build.py
build_py = re.sub(
    r'def extract_feedback\(file_path\):.*?def get_property_specs',
    new_extract_func + '\ndef get_property_specs',
    build_py,
    flags=re.DOTALL
)

with open('build.py', 'w', encoding='utf-8') as f:
    f.write(build_py)

print("Fixed template.html and build.py")
