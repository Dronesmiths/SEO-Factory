import os
import json
import datetime
from google.oauth2 import service_account
from googleapiclient.discovery import build

# Configuration
ANALYTICS_DIR = "seo-engine/ANALYTICS"
OUTPUT_FILE = os.path.join(ANALYTICS_DIR, "GSC_PULL.json")
COMPANY_FILE = "seo-engine/COMPANY.json"
RANGE_DAYS = 28

def get_site_url():
    if not os.path.exists(COMPANY_FILE):
        return None
    with open(COMPANY_FILE, 'r') as f:
        data = json.load(f)
        return data.get("domain")

def sync_gsc():
    # 1. Load Auth
    auth_json = os.environ.get("GSC_SERVICE_ACCOUNT_JSON")
    key_file = "GOOGLE KEYS/endless-terra-488018-c4-2f632c3b19ef.json"
    
    if auth_json:
        try:
            creds_content = json.loads(auth_json)
            creds = service_account.Credentials.from_service_account_info(creds_content)
        except Exception as e:
            print(f"❌ ERROR: Failed to parse credentials from ENV: {e}")
            return False
    elif os.path.exists(key_file):
        try:
            creds = service_account.Credentials.from_service_account_file(key_file)
        except Exception as e:
            print(f"❌ ERROR: Failed to load credentials from {key_file}: {e}")
            return False
    else:
        print("❌ ERROR: No GSC credentials found (ENV or File).")
        return False

    # 2. Identify Site
    site_url = get_site_url()
    if not site_url:
        print(f"❌ ERROR: Could not find domain in {COMPANY_FILE}")
        return False

    # 3. Build Service
    service = build('searchconsole', 'v1', credentials=creds)

    # 4. Calculate Dates
    end_date = datetime.date.today() - datetime.timedelta(days=3) # GSC latency
    start_date = end_date - datetime.timedelta(days=RANGE_DAYS)

    # 5. Fetch Data
    request = {
        'startDate': start_date.strftime('%Y-%m-%d'),
        'endDate': end_date.strftime('%Y-%m-%d'),
        'dimensions': ['query', 'page'],
        'rowLimit': 5000
    }

    try:
        response = service.searchanalytics().query(siteUrl=site_url, body=request).execute()
    except Exception as e:
        print(f"❌ ERROR: GSC API call failed: {e}")
        return False

    # 6. Format Output
    output = {
        "generated_at": datetime.date.today().strftime('%Y-%m-%d'),
        "range_days": RANGE_DAYS,
        "rows": []
    }

    if 'rows' in response:
        for row in response['rows']:
            output["rows"].append({
                "query": row['keys'][0],
                "page": row['keys'][1].replace(site_url, ""), # Store relative paths
                "clicks": row['clicks'],
                "impressions": row['impressions'],
                "ctr": row['ctr'],
                "position": row['position']
            })

    # 7. Write to Analytics
    os.makedirs(ANALYTICS_DIR, exist_ok=True)
    with open(OUTPUT_FILE, 'w') as f:
        json.dump(output, f, indent=2)

    print(f"✅ SUCCESS: Ingested {len(output['rows'])} rows into {OUTPUT_FILE}")
    return True

if __name__ == "__main__":
    sync_gsc()
