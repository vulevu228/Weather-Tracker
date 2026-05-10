import requests
import os
import ollama
import pandas as pd
from dotenv import load_dotenv
from datetime import datetime, timedelta

load_dotenv()
API_KEY = os.getenv("NEWS_API_KEY")

# 1. Set your date (Must be within the last 30 days for Free Tier)
# Let's try 25 days ago to be safe
start_date = (datetime.now() - timedelta(days=25)).strftime('%Y-%m-%d')

def fetch_political_news(query="politics", count=50):
    # Added pageSize=count and from={start_date}
    url = (
        f"https://newsapi.org/v2/everything?"
        f"q={query}&"
        f"from={start_date}&"
        f"pageSize={count}&"
        f"language=en&"
        f"apiKey={API_KEY}"
    )
    response = requests.get(url).json()
    return response.get('articles', [])

def analyze_and_save():
    articles = fetch_political_news("Election", count=50) # Increased to 50
    results = []

    print(f"Analyzing {len(articles)} headlines...")

    for art in articles:
        headline = art['title']
        
        # Local Llama 3 Analysis
        prompt = f"Analyze this political headline: '{headline}'. Is it Positive, Negative, or Neutral? Answer in one word."
        response = ollama.chat(model='llama3', messages=[{'role': 'user', 'content': prompt}])
        sentiment = response['message']['content'].strip().replace(".", "")

        results.append({
            "date": art['publishedAt'],
            "source": art['source']['name'],
            "headline": headline,
            "sentiment": sentiment
        })

    # Save to CSV for Excel manipulation tomorrow
    df = pd.DataFrame(results)
    df.to_csv("political_sentiment.csv", index=False)
    print("Done! Check 'political_sentiment.csv'")

analyze_and_save()