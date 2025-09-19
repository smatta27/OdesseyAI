import pandas as pd
import json
import requests
import os
from minimax_utils import generate_hashtags_with_minimax

# -------------------------
# Step 1: Parse Google Form CSV
# -------------------------
df = pd.read_csv("Event Finder Form.csv")

user_profiles = []

for _, row in df.iterrows():
    profile = {
        "location": str(row.get("Where is your desired location? (city, state, country)", "")).strip(),
        "age_range": str(row.get("Age Range", "")).strip(),
        "budget": str(row.get("Budget", "")).strip(),
        "group_type": str(row.get("Group Type", "")).strip(),
        "mood": str(row.get("What mood or vibe best fits your ideal activity?", "")).strip(),
        "time_of_day": str(row.get("Time of day", "")).strip(),
        "activity_categories": [
            c.strip().lower()
            for c in str(row.get("Activity Categories", "")).split(";")
            if isinstance(c, str) and c.strip()
        ],
        "duration": str(row.get("Duration", "")).strip(),
        "preference": str(row.get("Do you prefer:", "")).strip(),
        "goal": [
            c.strip().lower()
            for c in str(row.get("What's your primary goal when looking for new activities or experiences?", "")).split(";")
            if isinstance(c, str) and c.strip()
        ]
    }
    user_profiles.append(profile)

with open("survey_profiles.json", "w") as f:
    json.dump(user_profiles, f, indent=2)

print("✅ Exported profiles to survey_profiles.json")

# -------------------------
# Step 2: Apify Scraper Function
# -------------------------
APIFY_TOKEN = os.environ.get("APIFY_API_TOKEN")
if not APIFY_TOKEN:
    raise ValueError("⚠️ APIFY_API_TOKEN not set in environment variables.")

def run_apify_scraper(actor_id, hashtags):
    """Run an Apify scraper actor with hashtags as input"""
    url = f"https://api.apify.com/v2/acts/{actor_id}/run-sync-get-dataset-items?token={APIFY_TOKEN}"
    payload = {"hashtags": hashtags}
    response = requests.post(url, json=payload)
    response.raise_for_status()
    return response.json()

# -------------------------
# Step 3: Use MiniMax → Apify per User
# -------------------------
for i, profile in enumerate(user_profiles):
    if profile["activity_categories"]:
        print(f"🤖 Generating hashtags for user {i+1} with MiniMax...")

        hashtags_json = generate_hashtags_with_minimax(profile["activity_categories"], profile["location"])
        print("MiniMax output:", hashtags_json)

        # Try to parse MiniMax JSON output into Python dict
        try:
            hashtags_dict = json.loads(hashtags_json)
            all_hashtags = [h for lst in hashtags_dict.values() for h in lst]
        except Exception:
            print("⚠️ Could not parse MiniMax output, skipping user.")
            all_hashtags = []

        if all_hashtags:
            try:
                results = run_apify_scraper("apify~tiktok-scraper", all_hashtags)
                with open(f"user_{i+1}_results.json", "w") as f:
                    json.dump(results, f, indent=2)
                print(f"✅ Saved {len(results)} TikToks for user {i+1}")
            except Exception as e:
                print(f"⚠️ Error scraping for user {i+1}: {e}")
