import os
import sys
import json
import time
import subprocess
import logging
import hashlib
from datetime import datetime, timedelta

# Import custom scripts
sys.path.append(os.path.join(os.getcwd(), 'seo-engine/SCRIPTS'))
from lock_manager import acquire_lock, release_lock
from strike_zone_detector import detect_opportunities
from surgical_reinforce import reinforce

# Config
STATE_PATH = "seo-engine/STATE.json"
REPORT_PATH = "seo-engine/ANALYTICS/STRIKE_REPORT.json"
LOG_PATH = "seo-engine/ANALYTICS/FACTORY_AUDIT.log"
MAX_MUTATIONS_PER_RUN = 2
COOLDOWN_DAYS = 14

# Logging Setup
logging.basicConfig(
    filename=LOG_PATH,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def is_cool(slug, state):
    """Checks if a page has been mutated recently."""
    history = state.get("mutation_history", {})
    last_mutation = history.get(slug)
    if not last_mutation:
        return True
    
    last_date = datetime.strptime(last_mutation, "%Y-%m-%d")
    if datetime.now() - last_date > timedelta(days=COOLDOWN_DAYS):
        return True
    return False

def run_factory():
    print("🚀 Starting SEO Factory Orchestrator...")
    
    # 1. Acquire Lock
    if not acquire_lock():
        return

    try:
        # 2. Sync GSC (Simulated or actual call)
        print("📥 Syncing GSC Data (Simulated)...")
        # subprocess.run(["python3", "seo-engine/INGEST/sync_gsc.py"], check=True)

        # 3. Detect Opportunities
        print("🔍 Detecting Strike Zone Opportunities...")
        detect_opportunities()
        
        if not os.path.exists(REPORT_PATH):
            print("⚠️ No Strike Report found. Exiting.")
            return

        with open(REPORT_PATH, 'r') as f:
            report = json.load(f)
        
        with open(STATE_PATH, 'r') as f:
            state = json.load(f)

        opportunities = report.get("opportunities", [])
        if not opportunities:
            print("✅ No reinforcement opportunities detected. System IDLE.")
            return

        # 4. Filter and Prioritize
        mutations_count = 0
        for opp in opportunities:
            if mutations_count >= MAX_MUTATIONS_PER_RUN:
                print(f"🛑 Mutation cap ({MAX_MUTATIONS_PER_RUN}) reached.")
                break
            
            slug = opp['slug'].strip('/')
            if is_cool(slug, state):
                # 5. Reinforce
                print(f"🎯 Reinforcing: {slug} (Reason: {opp['category']})")
                
                # Payload Mapping (Simulated AI output for phase 4 validation)
                payload_map = {
                    "STRIKE_ZONE": ("BODY", "seo-engine/ANALYTICS/TEST_PAYLOAD_BODY_INCREMENTAL.html"),
                    "LOW_CTR": ("HEAD", "seo-engine/ANALYTICS/TEST_PAYLOAD_HEAD_LOCAL.html")
                }
                
                region, payload_path = payload_map.get(opp['category'], ("FAQ", "seo-engine/ANALYTICS/TEST_PAYLOAD_FAQ_INCREMENTAL.html"))
                
                if reinforce(slug, region, payload_path):
                    # 6. Update State & Log
                    state["mutation_history"][slug] = datetime.now().strftime("%Y-%m-%d")
                    logging.info(f"MUTATION: {slug} | REGION: {region} | REASON: {opp['category']}")
                    print(f"✅ Mutated {slug} in {region}")
                    mutations_count += 1
                else:
                    logging.error(f"FAILED: {slug} | Integrity or Injection error.")
            else:
                print(f"⏳ Skipping {slug} (In Cooldown)")

        # Save state
        state["last_run"] = datetime.now().strftime("%Y-%m-%d")
        with open(STATE_PATH, 'w') as f:
            json.dump(state, f, indent=4)

    except Exception as e:
        print(f"🧨 CRITICAL ENGINE FAILURE: {e}")
        logging.error(f"CRITICAL: {e}")
    finally:
        # 7. Release Lock
        release_lock()

if __name__ == "__main__":
    run_factory()
