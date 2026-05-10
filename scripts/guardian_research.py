import requests
import os
import ollama
import pandas as pd
from dotenv import load_dotenv

# Load keys from .env
load_dotenv()
API_KEY = os.getenv("GUARDIAN_API_KEY")

def run_guardian_analysis():
    # 1. Setup the request
    url = "https://content.guardianapis.com/search"
    params = {
        "q": "politics",           # You can change this to "election" or "economy"
        "from-date": "2026-01-01", # Starting from the beginning of the year
        "api-key": API_KEY,
        "page-size": 50            # How many articles to grab
    }

    print("Checking The Guardian archives for 2026...")
    
    # 2. Get the data
    response = requests.get(url, params=params)
    data = response.json()
    articles = data.get('response', {}).get('results', [])

    if not articles:
        print("No articles found. Check your API key or query!")
        return

    results = []
    print(f"Analyzing {len(articles)} headlines with Llama 3...")

    # 3. The "Bridge" to Llama 3
    for art in articles:
        headline = art['webTitle']
        date = art['webPublicationDate']
        
        # Ask local AI for sentiment
        prompt = f"Analyze the tone of this headline: '{headline}'. Reply with only one word: Positive, Negative, or Neutral."
        
        try:
            ai_msg = ollama.chat(model='llama3', messages=[{'role': 'user', 'content': prompt}])
            sentiment = ai_msg['message']['content'].strip().replace(".", "")
            
            results.append({
                "Date": date,
                "Section": art['sectionName'],
                "Headline": headline,
                "Sentiment": sentiment
            })
            print(f"Processed: {headline[:50]}... -> {sentiment}")
        except Exception as e:
            print(f"AI Error on headline: {e}")

    # 4. Save for Excel
    df = pd.DataFrame(results)
    df.to_csv("guardian_2026_data.csv", index=False, encoding='utf-8-sig')
    print("\n--- SUCCESS ---")
    print("Open 'guardian_2026_data.csv' in Excel to see the results.")

# Run the function
if __name__ == "__main__":
    run_guardian_analysis()