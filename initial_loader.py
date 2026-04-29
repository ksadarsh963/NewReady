import os
from dotenv import load_dotenv
from supabase import create_client, Client
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
import datetime
import time
import re

load_dotenv()

# 1. Setup Clients
supabase: Client = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))

# UPDATED MODELS FOR APRIL 2026
# Primary: Llama 3.3 (Faster and current on Groq)
primary_llm = ChatGroq(
    model_name="llama-3.3-70b-versatile", 
    groq_api_key=os.getenv("GROQ_API_KEY")
)

# Backup: Gemini 1.5 Flash (Most stable free-tier fallback)
backup_llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash"
)

embed_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

def run_initial_load(email, topic, interval):
    print(f"🚀 Starting Initial Load for: {topic}")

    # --- STEP A: Register Subscription ---
    sub_data = {
        "user_email": email,
        "topic": topic,
        "interval_minutes": interval,
        "last_updated": datetime.datetime.now().isoformat()
    }
    supabase.table("user_subscriptions").insert(sub_data).execute()
    print("✅ User subscription saved to cloud.")

    # --- STEP B: Search & Verify ---
    search_results = f"Latest verified reports on {topic} for April 2026..." 
    
    print("⚖️ Verifying news integrity...")
    
    prompt = ChatPromptTemplate.from_template("""
        Verify the following news about {topic}. 
        Return ONLY valid JSON with keys: is_verified (bool), headline (str), summary (str).
        DATA: {results}
    """)
    
    # We define the chain with a fallback. 
    # If Groq is decommissioned or fails, it hits Gemini.
    chain = (prompt | primary_llm.with_fallbacks([backup_llm]) | JsonOutputParser())
    
    verified_json = None
    for attempt in range(3):
        try:
            # We add a 1-second delay to prevent hitting 429 immediately
            time.sleep(1)
            verified_json = chain.invoke({"topic": topic, "results": search_results})
            if verified_json:
                break 
        except Exception as e:
            err = str(e)
            if "429" in err:
                wait = 35 # Default wait for quota
                print(f"🛑 Rate Limit. Waiting {wait}s...")
                time.sleep(wait)
            elif "400" in err or "decommissioned" in err:
                print("🔄 Model outdated! Attempting fallback model...")
                # If both fail, we might need a 2nd backup or local model
                continue
            else:
                print(f"⚠️ Attempt {attempt+1} failed: {err}")
                time.sleep(5)

    if not verified_json:
        print("❌ All providers (Groq & Gemini) are currently unavailable.")
        return

    # --- STEP C: Embedding & Push ---
    print("🧬 Generating semantic embedding...")
    vector = embed_model.embed_query(verified_json['summary'])

    news_entry = {
        "topic": topic,
        "content": verified_json,
        "embedding": vector 
    }
    supabase.table("verified_news").insert(news_entry).execute()
    print(f"☁️ Verified news pushed to Supabase for {topic}.")

if __name__ == "__main__":
    run_initial_load("adarsh@example.com", "AI in Kerala Healthcare", 120)