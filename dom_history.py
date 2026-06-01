import subprocess, re

BASE = r'C:\Users\Daniel Estrada\.gemini\antigravity\scratch\weekly-showing-reports'

# Check commits to trace back DOM history for suspect properties
slugs_to_check = [
    '244-biscayne-3702',
    '6061-collins-avenue-unit-5f',
    '17301-biscayne-boulevard-unit-1401',
    '1945-s-ocean-dr-unit-m2',
    '88-sw-7-st-1012',
    '1710-nw-106-terr',
    '10449-sw-78th-st',
    '1376-sw-4th-st-7',
    '8000-harding-avenue-unit-2b',
]

# Get last 10 commits
result = subprocess.run(['git', 'log', '--oneline', '-12'], cwd=BASE, capture_output=True, text=True)
commits = [line.split(' ', 1) for line in result.stdout.strip().split('\n')]

print("DOM history per property across last 12 commits:\n")
for slug in slugs_to_check:
    print(f"--- {slug} ---")
    for sha, msg in commits:
        for path in [f'{slug}/index.html', f'agents/joanna-jimenez/{slug}/index.html']:
            r = subprocess.run(['git', 'show', f'{sha}:{path}'], cwd=BASE, capture_output=True, text=True, encoding='utf-8')
            if r.returncode == 0 and r.stdout:
                m = re.search(r'Days on Market</div>\s*<div class="card-value[^"]*">\s*([\d,]+)', r.stdout)
                if m:
                    print(f"  {sha} ({msg[:40]}): DOM={m.group(1).strip()}")
                    break
    print()
