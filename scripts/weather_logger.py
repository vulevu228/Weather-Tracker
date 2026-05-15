import requests
import pandas as pd
import time
import os
from datetime import datetime
from dotenv import load_dotenv

# Load variables from .env
load_dotenv('.env')
# --- CONFIGURATION ---
API_KEY = os.getenv("OPENWEATHER_API_KEY")
CITIES = ["London", "Hamburg"]  # Added Hamburg here
INTERVAL = 300  # 5 minutes
FILE_NAME = "overnight_weather.csv"

def fetch_weather(city_name):
    # Safety check: make sure the key loaded
    if not API_KEY:
        print("Error: API Key not found. Check your .env file!")
        return None

    url = f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={API_KEY}&units=metric"
    
    try:
        response = requests.get(url)
        response.raise_for_status() 
        data = response.json()
        
        return {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "city": city_name,  # Added this so Excel can tell them apart
            "temp_c": data["main"]["temp"],
            "humidity_pct": data["main"]["humidity"],
            "pressure_hpa": data["main"]["pressure"],
            "wind_speed": data["wind"]["speed"],
            "description": data["weather"][0]["description"]
        }
    except Exception as e:
        print(f"Error fetching data for {city_name} at {datetime.now()}: {e}")
        return None

def run_once():
    print(f"Cloud logger started for {', '.join(CITIES)}. Updating {FILE_NAME}...")
    
    all_new_rows = []
    for city in CITIES:
        new_data = fetch_weather(city)
        if new_data:
            all_new_rows.append(new_data)
            print(f"Logged: {new_data['timestamp']} | {city}: {new_data['temp_c']}°C")
    
    if all_new_rows:
        df = pd.DataFrame(all_new_rows)
        # We use a path check to ensure it saves in the root directory properly
        df.to_csv(FILE_NAME, mode='a', index=False, header=not os.path.exists(FILE_NAME))
        print("Data saved. Script exiting successfully.")
    else:
        print("No data was fetched. Check API key/connection.")

if __name__ == "__main__":
    run_once()