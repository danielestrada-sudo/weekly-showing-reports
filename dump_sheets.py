import urllib.request
import csv
import io

def print_sheet(url, name):
    print(f"--- {name} ---")
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req) as response:
            text = response.read().decode('utf-8')
            reader = csv.reader(io.StringIO(text))
            for row in reader:
                print(row)
    except Exception as e:
        print(f"Error fetching {name}: {e}")

print_sheet('https://docs.google.com/spreadsheets/d/1M_H4baCDptHnGrpwlZgy1PiKRnS22YsKfRCOD0KACq4/export?format=csv&gid=690319944', 'SHEET 1')
print_sheet('https://docs.google.com/spreadsheets/d/1RaUV9kDdBGAzwRPrlmqkcbKmdFXDFeMvMU1lAD3pCcQ/export?format=csv&gid=0', 'SHEET 2')
