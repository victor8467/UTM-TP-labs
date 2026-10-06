# Laborator: functii, metode si importuri pe web
# Student: Buzdugan Victor

import sys
import argparse
import csv
import json
from datetime import datetime
from part5_webtools import get_title, security_headers, fetch, DEFAULT_HEADERS, site_report

BASE_URL = "https://cybercor.org"

# Daca main.py ar avea propria functie get_title, aceasta ar suprascrie functia importata.
# Numele definit local are intotdeauna prioritate in cod.
print("Titlu din webtools:", get_title(fetch(BASE_URL).text))
print("Constant User-Agent:", DEFAULT_HEADERS)

parser = argparse.ArgumentParser()
parser.add_argument("url", nargs="?", default=BASE_URL)
args = parser.parse_args()
target_url = args.url

with open("report.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["path", "status", "checked_at"])
    writer.writerow(["/", 200, datetime.now().isoformat()])

report = site_report(target_url)

print(f"=== Raport site: {report['url']} ===")
print(f"Cod de stare: {report['status_code']}")
print(f"Titlu: {report['title']}")
print(f"Adresa IP: {report['ip']}")
print(f"Redirectionari: {report['redirects']}")
print(f"Scor securitate: {report['security_score']}")
print(f"Certificat: {report['cert_days_left']} de zile ramase")
print(f"Legaturi: {report['internal_links']} interne, {report['external_links']} externe")
print(f"Cai interzise: {', '.join(report['disallowed_paths'])}")

with open("report.json", "w") as f:
    json.dump(report, f, indent=2)

print("\nSalvat in report.json si report.csv")
