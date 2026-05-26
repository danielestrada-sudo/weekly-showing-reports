"""
Feedback update for May 18-24, 2026 (Connor's May 26 submissions)
Updates: showings count (last-7 card + table row + grand total) and feedback section
"""
import re, os

BASE = r'C:\Users\Daniel Estrada\.gemini\antigravity\scratch\weekly-showing-reports'
AGENT_BASE = os.path.join(BASE, 'agents', 'joanna-jimenez')

WEEK_LABEL = 'May 18 - May 24, 2026'

# May 18-24 data from Connor's May 26 submissions
# showings = actual physical showings this week
# feedback = cleaned-up text for the report
FEEDBACK_DATA = {
    '6061-collins-avenue-unit-5f': {
        'showings': 0,
        'old_grand_showings': 8,
        'feedback': 'No showings this week.'
    },
    '1376-sw-4th-st-7': {
        'showings': 1,
        'old_grand_showings': 7,
        'feedback': (
            'The renters went back for a second showing, but unfortunately their car '
            'did not fit inside the garage, so they will not be moving forward.'
        )
    },
    '7334-harding-unit-6': {
        'showings': 4,
        'old_grand_showings': 22,
        'feedback': (
            '4 private showings — 3 for sale and 1 for rent. One buyer requested the building '
            'financials and HOA information; their agent is currently reviewing the details. '
            'The rental showing noted there was a smell throughout the unit and did not feel it '
            'was the right fit. The remaining two sale showings are still exploring their options '
            'before making a decision.'
        )
    },
    '8000-harding-avenue-unit-2b': {
        'showings': 0,
        'old_grand_showings': 3,
        'feedback': (
            'We had four private showing requests this week — three for sale and one for rent. '
            'Unfortunately, we were unable to accommodate any of them as the tenants were out of '
            'town and in the process of moving.'
        )
    },
    '17301-biscayne-boulevard-unit-1401': {
        'showings': 2,
        'old_grand_showings': 6,
        'feedback': (
            'The first showing was with a family who currently lives in the building and rents '
            'another unit. They really liked the views — their current unit is on a different '
            'line — but are still unsure about moving forward since they are currently in a '
            'three-bedroom unit.<br><br>'
            'The second showing was with a buyer who liked both the building and the unit '
            'overall, but is continuing to tour other properties before making a decision.'
        )
    },
    '763-pennsylvania-avenue-unit-116': {
        'showings': 1,
        'old_grand_showings': 19,
        'feedback': (
            'The agent mentioned the showing went well overall and that the clients thought '
            'the unit was nice, but they are primarily looking for something closer to the '
            'beach on Collins.'
        )
    },
    '1945-s-ocean-dr-unit-m2': {
        'showings': 0,
        'old_grand_showings': 3,
        'feedback': 'No showing requests this week. One showing is scheduled for next week.'
    },
    '244-biscayne-3702': {
        'showings': 1,
        'old_grand_showings': 3,
        'feedback': (
            'We had one showing this week. The agent mentioned the showing went well overall, '
            'but ultimately the unit was too small for the clients\' needs.'
        )
    },
    '88-sw-7-st-1012': {
        'showings': 1,
        'old_grand_showings': 2,
        'feedback': (
            'We had one private showing scheduled this week; it was cancelled last minute. '
            'Working on rescheduling.'
        )
    },
    # No May 26 entries from Connor for these — 0 showings, no new feedback
    '234-washington-ave': {
        'showings': 0,
        'old_grand_showings': 60,
        'feedback': None  # No new feedback this week
    },
    '320-85-st-15': {
        'showings': 0,
        'old_grand_showings': 27,
        'feedback': None
    },
    '10449-sw-78th-st': {
        'showings': 0,
        'old_grand_showings': 12,
        'feedback': None
    },
}


def build_feedback_html(text, week_label):
    return f'''<div class="feedback-item">
                    <div class="feedback-text">
                        "{text}"
                        <span class="agent-date" style="display: block; margin-top: 0.5rem; font-style: normal;">— {week_label}</span>
                    </div>
                </div>'''


def update_showings_and_feedback(html, d, week_label):
    showings = d['showings']
    new_grand = d['old_grand_showings'] + showings
    showings_display = f'+{showings}' if showings > 0 else '0'

    # 1. Last 7 Days Showings card
    html = re.sub(
        r'(<div class="card-label">Last 7 Days Showings</div>\s*<div class="card-value">\s*)[^\n<]+(\s*<span)',
        lambda m: m.group(1) + showings_display + '\n                        ' + m.group(2),
        html
    )

    # 2. Physical Showings table row — last-7 and grand-total
    html = re.sub(
        r'(metric-name[^>]*>Physical Showings.*?</div>\s*<div class="last-7">)[^<]*(</div>\s*<div class="grand-total">)[^<]*(</div>)',
        lambda m: m.group(1) + showings_display + m.group(2) + str(new_grand) + m.group(3),
        html, flags=re.DOTALL
    )

    # 3. Prepend new feedback entry (if we have feedback)
    feedback_text = d.get('feedback')
    if feedback_text:
        new_fb_html = build_feedback_html(feedback_text, week_label)
        # Find the feedback card div and insert after it
        html = re.sub(
            r'(<div class="card">\s*\n\s*<div class="feedback-item">)',
            lambda m: '<div class="card">\n                ' + new_fb_html + '\n                \n                ' + '<div class="feedback-item">',
            html, count=1
        )

    return html


def write_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f'  Written: {path}')


def process(slug, d):
    print(f'\nProcessing: {slug}')
    print(f'  Showings: {d["showings"]} | Grand: {d["old_grand_showings"]} -> {d["old_grand_showings"] + d["showings"]}')

    for location_base in [AGENT_BASE, BASE]:
        path = os.path.join(location_base, slug, 'index.html')
        if not os.path.exists(path):
            print(f'  SKIP: {path}')
            continue
        with open(path, encoding='utf-8') as f:
            html = f.read()
        updated = update_showings_and_feedback(html, d, WEEK_LABEL)
        write_file(path, updated)


print('=== Updating feedback and showings for May 18-24, 2026 ===\n')
for slug, data in FEEDBACK_DATA.items():
    process(slug, data)

print('\n=== All feedback updates complete! ===')
