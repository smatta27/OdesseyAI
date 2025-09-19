**OdysseyAI**

- OdysseyAI is an AI-powered event and activity discovery agent. Unlike general-purpose chatbots, OdysseyAI specializes in curating local, personalized experiences — from thrift shops to hidden gems — by scraping real-world content (TikTok, Instagram) and turning it into actionable recommendations.

**Features**

- User Personalization: Tailored to your preferences (age, mood, budget, group type).
- Social Content Scraping: Uses Apify to collect fresh event/activity data from TikTok & Instagram.
- Smart Parsing: LlamaIndex extracts and structures activities from raw captions/posts.
- Chat Interface: Powered by MiniMax LLM for conversational recommendations.
- Optional Memory: Redis backend to store user preferences and past feedback.

**System Architecture**

- Survey → User Preferences
- Google Form/Typeform survey collects user context (age, mood, activity type, budget).
- Responses exported as CSV/JSON → used to generate scraping queries (hashtags, filters).
- Data Collection (Apify)
- Scrapes TikTok/IG posts with relevant hashtags (e.g., #thriftingSF, #bayareaevents).
- Normalizes JSON into a consistent format.
- Indexing (LlamaIndex)
- Loads captions/posts → converts into documents.
- Extracts structured activities (e.g., store name, type, location).
- Builds retriever index for fast semantic search.
- Chat Layer (MiniMax)
- Wraps MiniMax as the LLM inside LlamaIndex.
- ReAct Agent with tools:
- search_activities(query) → queries index.
- enrich_place(place) → (optional) cross-check via Maps/Yelp API.
- Frontend & API
- FastAPI backend serving /chat endpoint.
- Simple Next.js chat UI (input + streaming output + activity cards).

**Tech Stack**

- Apify → Scraping TikTok/Instagram content
- LlamaIndex → Document parsing, activity extraction, semantic search
- MiniMax → LLM powering chatbot & reasoning
- FastAPI → Backend API for chat interface
- Redis (optional) → Store embeddings, user prefs, feedback
