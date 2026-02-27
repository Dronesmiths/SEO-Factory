import json
import csv
import os

INPUT_FILE = "seo-engine/ANALYTICS/GSC_PULL.json"
OUTPUT_FILE = "seo-engine/ANALYTICS/GSC_REPORT.csv"

def export_to_csv():
    if not os.path.exists(INPUT_FILE):
        print(f"❌ ERROR: {INPUT_FILE} not found. Run sync_gsc.py first.")
        return

    with open(INPUT_FILE, 'r') as f:
        data = json.load(f)

    rows = data.get("rows", [])
    if not rows:
        print("ℹ️ No data rows found to export.")
        return

    # Extract headers from the first row
    headers = ["query", "page", "clicks", "impressions", "ctr", "position"]

    with open(OUTPUT_FILE, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        for row in rows:
            # Filter only the headers we want
            filtered_row = {k: row.get(k, "") for k in headers}
            writer.writerow(filtered_row)

    print(f"✅ SUCCESS: Exported {len(rows)} rows to {OUTPUT_FILE}")

if __name__ == "__main__":
    export_to_csv()
