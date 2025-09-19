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


def run_apify_scraper(actor_id, payload):
    """
    Run an Apify scraper actor with the given payload.
    Payload may differ by platform (hashtags, query, queries).
    """
    url = f"https://api.apify.com/v2/acts/{actor_id}/run-sync-get-dataset-items?token={APIFY_TOKEN}"
    response = requests.post(url, json=payload)
    response.raise_for_status()
    return response.json()


# Define platform configurations
PLATFORM_CONFIGS = {
    "tiktok": {
        "actor": "apify~tiktok-scraper",
        "payload_key": "hashtags"
    },
    "instagram": {
        "actor": "apify~instagram-scraper",
        "payload_key": "hashtags"
    },
    "maps": {
        "actor": "apify~google-maps-scraper",
        "payload_key": "queries"
    },
    "eventbrite": {
        "actor": "apify~eventbrite-scraper",
        "payload_key": "query"
    }
}

def scrape_all_platforms(user_id, hashtags, platforms=None):
    """
    Run scrapers across multiple platforms for a single user.
    Saves ONE merged JSON file with a 'platform' field.
    """
    if platforms is None:
        platforms = ["tiktok", "instagram", "maps", "eventbrite"]

    all_results = []  # collect everything here

    for platform in platforms:
        if platform not in PLATFORM_CONFIGS:
            print(f"⚠️ Unknown platform: {platform}")
            continue

        config = PLATFORM_CONFIGS[platform]
        actor_id = config["actor"]
        key = config["payload_key"]

        # Prepare payload differently depending on input type
        if key == "hashtags":
            payload = {key: hashtags}
        elif key == "queries":
            payload = {key: [", ".join(hashtags)]}  # Maps expects list of queries
        elif key == "query":
            payload = {key: ", ".join(hashtags)}    # Eventbrite expects a single string
        else:
            print(f"⚠️ Unsupported payload type for {platform}")
            continue

        try:
            print(f"🔎 Scraping {platform} for user {user_id} with {len(hashtags)} tags/queries")
            results = run_apify_scraper(actor_id, payload)

            # Attach platform label to each result item
            for item in results:
                item["platform"] = platform
            all_results.extend(results)

            print(f"✅ Collected {len(results)} {platform} results for user {user_id}")

        except Exception as e:
            print(f"⚠️ Error scraping {platform} for user {user_id}: {e}")

    # Save ONE merged file per user
    merged_filename = f"user_{user_id}_results.json"
    with open(merged_filename, "w") as f:
        json.dump(all_results, f, indent=2)

    print(f"📂 Saved merged results file: {merged_filename} with {len(all_results)} total items")

# -------------------------
# Step 3: Use MiniMax → Scrape All Platforms
# -------------------------
for i, profile in enumerate(user_profiles):
    if profile["activity_categories"]:
        print(f"🤖 Generating hashtags for user {i+1} with MiniMax...")

        hashtags_json = generate_hashtags_with_minimax(
            profile["activity_categories"], 
            profile["location"]
        )
        print("MiniMax output:", hashtags_json)

        try:
            hashtags_dict = json.loads(hashtags_json)
            all_hashtags = [h for lst in hashtags_dict.values() for h in lst]
        except Exception:
            print("⚠️ Could not parse MiniMax output, skipping user.")
            all_hashtags = []

        if all_hashtags:
            scrape_all_platforms(i+1, all_hashtags)
