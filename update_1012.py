import re, os

BASE = r'C:\Users\Daniel Estrada\.gemini\antigravity\scratch\weekly-showing-reports'
AGENT_BASE = os.path.join(BASE, 'agents', 'joanna-jimenez')
slug = '88-sw-7-st-1012'

for base in [BASE, AGENT_BASE]:
    html_path = os.path.join(base, slug, 'index.html')
    if not os.path.exists(html_path):
        continue
    with open(html_path, 'r', encoding='utf-8') as f:
        html = f.read()

    # Update Social Media Views: +222 -> +10, 3,370 -> 3,158
    html = re.sub(
        r'(Social Media Views.*?last-7">\s*)\+222(\s*</div>\s*<div class="grand-total">\s*)3,370(\s*</div>)',
        lambda m: m.group(1) + '+10' + m.group(2) + '3,158' + m.group(3),
        html, flags=re.DOTALL
    )

    # Update Showings: 0 -> 2, 3 -> 5
    html = re.sub(
        r'(Physical Showings.*?last-7">\s*)0(\s*</div>\s*<div class="grand-total">\s*)3(\s*</div>)',
        lambda m: m.group(1) + '2' + m.group(2) + '5' + m.group(3),
        html, flags=re.DOTALL
    )

    # Update Feedback text
    feedback_text = "1. Really liked the unit comparing with units at Reach; The other client did not like the building."
    html = re.sub(
        r'(<div class="feedback-content">\s*<p>)[^<]*(</p>)',
        lambda m: m.group(1) + feedback_text + m.group(2),
        html, flags=re.DOTALL
    )

    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html)
        
    print(f"Updated {base}/{slug}")

