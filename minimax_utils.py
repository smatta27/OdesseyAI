import requests
import os

MINIMAX_API_KEY = os.environ.get("MINIMAX_API_KEY")

if not MINIMAX_API_KEY:
    raise ValueError("⚠️ MINIMAX_API_KEY not set in environment variables.")

def generate_hashtags_with_minimax(categories, location="San Francisco"):
    """
    Ask MiniMax to generate TikTok/Instagram hashtags 
    for the given categories and location.
    Returns a string with JSON-like content.
    """
    url = "https://api.minimax.chat/v1/text/chatcompletion"
    headers = {"Authorization": f"Bearer {MINIMAX_API_KEY}"}

    prompt = f"""
    You are an assistant that generates social media hashtags for event/activity discovery.
    Location: {location}
    Activity categories: {", ".join(categories)}
    Return 5 hashtags per category as a JSON object.
    """

    payload = {
        "model": "abab5.5-chat",   # model name may vary in your account
        "messages": [{"role": "user", "content": prompt}]
    }

    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()

    return response.json()["choices"][0]["message"]["content"]
