import csv

path = r'C:\Users\Daniel Estrada\.gemini\antigravity\brain\a3049b86-fe12-4807-a724-d40f2852e20b\.system_generated\steps\20\content.md'

with open(path, 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    for row in reader:
        if len(row) > 2 and 'joanna' in row[1].lower():
            print(row)
