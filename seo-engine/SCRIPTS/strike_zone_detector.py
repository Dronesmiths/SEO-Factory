import json
import os

# Paths
ANALYTICS_DIR = "seo-engine/ANALYTICS"
GSC_PULL = os.path.join(ANALYTICS_DIR, "GSC_PULL.json")
THRESHOLDS = os.path.join(ANALYTICS_DIR, "thresholds.json")
OUTPUT_FILE = os.path.join(ANALYTICS_DIR, "STRIKE_REPORT.json")

def load_json(path):
    if not os.path.exists(path):
        return None
    with open(path, 'r') as f:
        return json.load(f)

def detect_opportunities():
    gsc_data = load_json(GSC_PULL)
    thresholds = load_json(THRESHOLDS)

    if not gsc_data or not thresholds:
        print("❌ Error: Missing GSC_PULL.json or thresholds.json")
        return False

    report = {
        "generated_at": gsc_data.get("generated_at"),
        "low_ctr_pages": [],
        "strike_zone_pages": [],
        "top_performers": [],
        "rising_queries": []
    }

    low_ctr_threshold = thresholds.get("low_ctr_threshold", 0.02)
    min_impressions = thresholds.get("min_impressions", 100)
    strike_min = thresholds["strike_zone"]["min_pos"]
    strike_max = thresholds["strike_zone"]["max_pos"]
    top_pos = thresholds.get("top_performer_threshold", 5.0)

    for row in gsc_data.get("rows", []):
        if row['impressions'] < min_impressions:
            continue

        page_data = {
            "page": row['page'],
            "query": row['query'],
            "position": row['position'],
            "ctr": row['ctr'],
            "impressions": row['impressions']
        }

        # 1. Low CTR (Focus on Title/Meta)
        if row['ctr'] < low_ctr_threshold and row['position'] <= 10:
            report["low_ctr_pages"].append(page_data)

        # 2. Strike Zone (Focus on Content Expansion)
        if strike_min <= row['position'] <= strike_max:
            report["strike_zone_pages"].append(page_data)

        # 3. Top Performers (Focus on Internal Link Protection)
        if row['position'] <= top_pos:
            report["top_performers"].append(page_data)

        # 4. Rising Queries (Potential for new clusters)
        if 11 <= row['position'] <= 30:
            report["rising_queries"].append(page_data)

    # Sort report for readability
    for key in report:
        if isinstance(report[key], list):
            report[key] = sorted(report[key], key=lambda x: x['impressions'], reverse=True)[:10]

    with open(OUTPUT_FILE, 'w') as f:
        json.dump(report, f, indent=2)

    print(f"✅ SUCCESS: {OUTPUT_FILE} generated.")
    return True

if __name__ == "__main__":
    detect_opportunities()
