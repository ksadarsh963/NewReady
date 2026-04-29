import datetime
from integrity_verify import get_verified_update

def process_user_request(topic, is_new_user=False):
    # 1. Determine the timeframe
    if is_new_user:
        # Initial Load: Get everything from today
        search_query = f"{topic} news since yesterday"
    else:
        # Regular Update: Just the last 2 hours
        search_query = f"{topic} news in the last 2 hours"
    
    # 2. Get the Verified Data (Using your existing script)
    # results = search_engine.run(search_query)
    # verified_data = get_verified_update(topic, results)
    
    # 3. Push to Supabase (Cloud)
    # supabase.table('news_articles').insert(verified_data).execute()
    
    print(f"✅ Database updated for {topic} at {datetime.datetime.now()}")