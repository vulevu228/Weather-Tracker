import requests
import pandas as pd
import time
import os
from datetime import datetime
from dotenv import load_dotenv

# Load variables from .env
load_dotenv()

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

print(f"Secure logger started for {', '.join(CITIES)}. Appending to {FILE_NAME}...")

try:
    while True:
        # Loop through each city in our list
        for city in CITIES:
            new_data = fetch_weather(city)
            
            if new_data:
                df = pd.DataFrame([new_data])
                # Append mode 'a', write header only if file doesn't exist
                df.to_csv(FILE_NAME, mode='a', index=False, header=not os.path.exists(FILE_NAME))
                print(f"Logged: {new_data['timestamp']} | {city}: {new_data['temp_c']}°C")
        
        # Wait for the interval before checking all cities again
        print(f"Waiting {INTERVAL} seconds...")
        time.sleep(INTERVAL)

except KeyboardInterrupt:
    print("\nLogging stopped by user. CSV is saved and ready for analysis.")