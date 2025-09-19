import pandas as pd
import json

df = pd.read_csv("Event Finder Form.csv")

user_profiles = []

for _, row in df.iterrows():
    profile = {
        "location": row["Where is your desired location? (city, state, country)"],
        "age_range": row["Age Range"],
        "budget": row["Budget"],
        "group_type": row["Group Type"],
        "mood": row["What mood or vibe best fits your ideal activity?"],
        "time_of_day": row["Time of day"],
        "activity_categories": [c.strip().lower() for c in str(row["Activity Categories"]).split(";")],
        "duration": row["Duration"],
        "preference": row["Do you prefer:"],
        "goal": [c.strip().lower() for c in str(row["What's your primary goal when looking for new activities or experiences?"]).split(";")]
    }
    user_profiles.append(profile)

with open("survey_profiles.json", "w") as f:
    json.dump(user_profiles, f, indent=2)

print("Exported profiles to survey_profiles.json")
