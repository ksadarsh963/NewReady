import os
import json
from google import genai
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

# 1. Setup the Client using the 2026 SDK
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# 2. Define our "Production Schema"
# This ensures the AI always gives us exactly what we need
class NewsObject(BaseModel):
    headline: str
    sentiment: str # Positive, Negative, or Neutral
    impact_score: int # 1 to 10
    key_entities: list[str]
    one_sentence_summary: str

def extract_news_data(text):
    print("🚀 Processing news article...")
    
    # We use 'gemini-2.0-flash' or 'gemini-1.5-flash' for speed and cost
    response = client.models.generate_content(
        model="gemini-2.0-flash", 
        contents=text,
        config={
            'response_mime_type': 'application/json',
            'response_schema': NewsObject,
        }
    )
    
    # The SDK automatically parses the JSON into our NewsObject
    return response.parsed

# --- TEST IT ---
raw_news = """
Apple announced a major partnership with a Kerala-based tech hub 
to improve Malayalam voice recognition in the next iOS update. 
Investors responded positively, and stocks rose by 2% today.
"""

result = extract_news_data(raw_news)

print(f"\n--- AI EXTRACTED DATA ---")
print(f"Headline: {result.headline}")
print(f"Sentiment: {result.sentiment} (Impact: {result.impact_score}/10)")
print(f"Entities: {', '.join(result.key_entities)}")
print(f"Summary: {result.one_sentence_summary}")