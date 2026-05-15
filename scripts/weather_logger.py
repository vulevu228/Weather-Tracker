import requests
import pandas as pd
import os
from datetime import datetime
from dotenv import load_dotenv

# 1. Load environment variables
# load_dotenv() will look for a .env file locally, 
# but GitHub Actions will provide the variables directly.
load_dotenv()

# --- CONFIGURATION ---
# This pathing ensures that if the script is in /scripts/, 
# the CSV is saved in the root folder /overnight_weather.csv
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
FILE_NAME = os.path.join(BASE_DIR, "overnight_weather.csv")

API_KEY = os.getenv("OPENWEATHER_API_KEY")
CITIES = ["London", "Hamburg"]

def fetch_weather(city_name):
    """Fetches weather data for a specific city from OpenWeatherMap."""
    if not API_KEY:
        print(f"CRITICAL ERROR: API Key is missing for {city_name}!")
        return None

    url = f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={API_KEY}&units=metric"
    
    try:
        print(f"Attempting to fetch data for {city_name}...")
        response = requests.get(url, timeout=10) # Added timeout to prevent hanging
        response.raise_for_status() 
        data = response.json()
        
        return {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "city": city_name,
            "temp_c": data["main"]["temp"],
            "humidity_pct": data["main"]["humidity"],
            "pressure_hpa": data["main"]["pressure"],
            "wind_speed": data["wind"]["speed"],
            "description": data["weather"][0]["description"]
        }
    except Exception as e:
        print(f"Error fetching data for {city_name}: {e}")
        return None

def run_once():
    """Main execution function to be called by GitHub Actions."""
    print("--- STARTING WEATHER LOGGER ---")
    print(f"Target file: {FILE_NAME}")
    
    all_new_rows = []
    for city in CITIES:
        new_data = fetch_weather(city)
        if new_data:
            all_new_rows.append(new_data)
            print(f"Successfully retrieved: {city} ({new_data['temp_c']}°C)")
    
    if all_new_rows:
        df = pd.DataFrame(all_new_rows)
        # Append to CSV; if file doesn't exist, write the header
        file_exists = os.path.isfile(FILE_NAME)
        df.to_csv(FILE_NAME, mode='a', index=False, header=not file_exists)
        print(f"Success: {len(all_new_rows)} rows appended to {FILE_NAME}")
    else:
        print("FAILED: No data was collected during this run.")
    
    print("--- SCRIPT FINISHED ---")

if __name__ == "__main__":
    run_once()