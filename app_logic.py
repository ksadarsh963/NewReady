import os
from supabase import create_client, Client
from dotenv import load_dotenv
from datetime import datetime, timedelta

load_dotenv()

# 1. Initialize Supabase
url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)

def subscribe_user(email, topic, interval):
    print(f"📡 Subscribing {email} to topic: {topic} every {interval} minutes.")
    
    # Step A: Save the subscription to the cloud
    data = {
        "user_email": email,
        "topic": topic,
        "interval_minutes": interval,
        "last_updated": datetime.now().isoformat()
    }
    supabase.table("user_subscriptions").insert(data).execute()
    
    # Step B: Immediate "Initial Load" (History for the day)
    print(f"📚 Fetching initial 24-hour history for {topic}...")
    # Here you would call your existing get_verified_update() function
    # result = get_verified_update(topic, timeframe="24h")
    # supabase.table("verified_news").insert({"topic": topic, "content": result}).execute()

def check_for_updates():
    # This runs in the background (every few minutes)
    now = datetime.now()
    subscriptions = supabase.table("user_subscriptions").select("*").execute()
    
    for sub in subscriptions.data:
        last_upd = datetime.fromisoformat(sub['last_updated'].replace('Z', '+00:00'))
        interval = timedelta(minutes=sub['interval_minutes'])
        
        # Check if the user's personal window has passed
        if now - last_upd >= interval:
            print(f"⏰ Time to update {sub['topic']} for {sub['user_email']}")
            # 1. Trigger AI Search & Verification
            # 2. Update 'last_updated' timestamp in DB
            # 3. Store new news in verified_news table