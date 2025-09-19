# 🚀 OdysseyAI

**OdysseyAI** is an AI-powered event and activity discovery agent.  
Unlike general-purpose chatbots, OdysseyAI focuses on curating **local, personalized experiences** — from thrift shops to hidden gems — by scraping real-world content (TikTok, Instagram) and transforming it into **actionable recommendations**.

---

## ✨ Features
- **Personalized Recommendations** → Tailored to user context (age, mood, budget, group type).  
- **Social Content Scraping** → Uses [Apify](https://apify.com) to collect fresh activity/event data from TikTok & Instagram.  
- **Smart Parsing** → [LlamaIndex](https://docs.llamaindex.ai) extracts and structures activities from raw captions/posts.  
- **Conversational Chat** → Powered by [MiniMax](https://agent.minimax.io/) for natural, context-aware dialogue.  
- **Optional Memory Layer** → [Redis](https://redis.io/) backend for user preferences, embeddings, and feedback.  

---

## 🏗 System Architecture


### 1. Survey → User Preferences
- Google Form/Typeform collects user context (age, mood, activity type, budget).  
- Responses exported as CSV/JSON and converted into scraping queries (hashtags, filters).  

### 2. Data Collection (Apify)
- Scrapes TikTok/IG posts using relevant hashtags (e.g., `#thriftingSF`, `#bayareaevents`).  
- Normalizes raw JSON into a consistent schema.  

### 3. Indexing (LlamaIndex)
- Loads captions/posts → `Document` objects.  
- Extracts structured activities (e.g., *Community Thrift SF*, type: thrift store, location: San Francisco).  
- Builds retriever index for fast semantic search.  

### 4. Chat Layer (MiniMax)
- MiniMax serves as the LLM inside LlamaIndex.  
- Deployed as a **ReAct Agent** with tools:
  - `search_activities(query)` → queries the semantic index.  
  - `enrich_place(place)` *(optional)* → cross-check with Maps/Yelp API.  

### 5. API & Frontend
- **Backend:** [FastAPI](https://fastapi.tiangolo.com/) serving `/chat` endpoint.  
- **Frontend:** [Next.js](https://nextjs.org/) chat UI with:
  - Input box (user query)  
  - Streaming AI responses  
  - Activity cards (name, type, location, trending score)  

---

## ⚙️ Tech Stack
- **Apify** → Social content scraping (TikTok, Instagram)  
- **LlamaIndex** → Document parsing, activity extraction, semantic search  
- **MiniMax** → LLM powering the chatbot & reasoning  
- **FastAPI** → Backend API  
- **Redis (optional)** → Store embeddings, user preferences, and feedback  

---

## 🔮 Roadmap
- [ ] Integrate Google Maps/Yelp for verified addresses & reviews  
- [ ] Add group mode (combine multiple user profiles for shared recs)  
- [ ] Launch voice interface (Gladia for STT/TTS)  
- [ ] Push notifications for trending events nearby  

---
