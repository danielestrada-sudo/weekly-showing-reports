import re

with open('template.html', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace(
'''<div class="card">
                    <div class="card-label">Last 7 Days Views</div>
                    <div class="card-value">
                        N/A
                        <span class="card-change">+35.4%</span>
                    </div>
                </div>
                <div class="card">
                    <div class="card-label">Last 7 Days Showings</div>
                    <div class="card-value">
                        N/A
                        <span class="card-change">Trending Up</span>
                    </div>
                </div>''',
'''<div class="card">
                    <div class="card-label">Last 7 Days Views</div>
                    <div class="card-value">
                        {{LAST_7_ONLINE_TABLE}}
                        <span class="card-change">Updated</span>
                    </div>
                </div>
                <div class="card">
                    <div class="card-label">Last 7 Days Showings</div>
                    <div class="card-value">
                        {{LAST_7_SHOWINGS}}
                        <span class="card-change">This Week</span>
                    </div>
                </div>'''
)

content = content.replace(
'''<div class="table-row">
                    <div class="metric-name">Listing Views (Online)</div>
                    <div class="last-7">N/A</div>
                    <div class="grand-total">{{TOTAL_ONLINE_VISITS}}</div>
                </div>
                <div class="table-row">
                    <div class="metric-name">Physical Showings</div>
                    <div class="last-7">N/A</div>
                    <div class="grand-total">{{TOTAL_PHYSICAL_VISITS}}</div>
                </div>
                <div class="table-row">
                    <div class="metric-name">Emails Sent (Opened)</div>
                    <div class="last-7">N/A</div>
                    <div class="grand-total">{{TOTAL_EMAILS_OPENED}}</div>
                </div>
                <div class="table-row">
                    <div class="metric-name">Social Media Views</div>
                    <div class="last-7">N/A</div>
                    <div class="grand-total">{{TOTAL_SOCIAL_VIEWS}}</div>
                </div>''',
'''<div class="table-row">
                    <div class="metric-name">Listing Views (Online)</div>
                    <div class="last-7">{{LAST_7_ONLINE_TABLE}}</div>
                    <div class="grand-total">{{TOTAL_ONLINE_VISITS}}</div>
                </div>
                <div class="table-row">
                    <div class="metric-name">Physical Showings</div>
                    <div class="last-7">{{LAST_7_PHYSICAL_TABLE}}</div>
                    <div class="grand-total">{{TOTAL_PHYSICAL_VISITS}}</div>
                </div>
                <div class="table-row">
                    <div class="metric-name">Emails Sent (Opened)</div>
                    <div class="last-7">+{{LAST_7_EMAILS_TABLE}}</div>
                    <div class="grand-total">{{TOTAL_EMAILS_OPENED}}</div>
                </div>
                <div class="table-row">
                    <div class="metric-name">Social Media Views</div>
                    <div class="last-7">+{{LAST_7_SOCIAL_TABLE}}</div>
                    <div class="grand-total">{{TOTAL_SOCIAL_VIEWS}}</div>
                </div>'''
)

content = content.replace('Generated on April 7, 2026', 'Generated on April 20, 2026')

with open('template.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("template.html updated.")
