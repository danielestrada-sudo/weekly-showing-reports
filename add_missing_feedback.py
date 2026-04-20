import os
import re

feedbacks = {
    "234-washington-ave": "Client looking for second home in Miami - the wife lived here for 10+ years but they now live in Hawaii. He thinks the home is great but has concerns over the split levels. He thinks they are a little too much for their 2 year old and 7 week old. He think the most they could do is two levels.",
    "1710-nw-106-terr": "No showings this week."
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

    match = re.search(r'(<div id="feedback" class="tab-content">.*?<div class="card">)', content, re.DOTALL)
    if match:
        insertion_point = match.end()
        # insert right after <div class="card">
        # wait! need to check if the exact feedback was already inserted to avoid dupes!
        if feedback_text[:20] in content:
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
