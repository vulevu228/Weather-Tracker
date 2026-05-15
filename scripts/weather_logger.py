import requests
import pandas as pd
import os
import sys
from datetime import datetime
from dotenv import load_dotenv

# Try to load .env for local work, but don't fail if it's missing
load_dotenv()

# --- CONFIGURATION ---
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
FILE_NAME = os.path.join(BASE_DIR, "overnight_weather.csv")
API_KEY = os.getenv("OPENWEATHER_API_KEY")
CITIES = ["London", "Hamburg"]

def fetch_weather(city_name):
    if not API_KEY:
        print(f"CRITICAL: No API Key found for {city_name}", flush=True)
        return None

    # We use a 10-second timeout. If it takes longer, the script will error out
    # rather than hanging for hours.
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={API_KEY}&units=metric"
    
    try:
        print(f"Fetching {city_name}...", end=" ", flush=True)
        response = requests.get(url, timeout=10) 
        response.raise_for_status() 
        data = response.json()
        print("Done.", flush=True)
        
        return {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "city": city_name,
            "temp_c": data["main"]["temp"],
            "humidity_pct": data["main"]["humidity"],
            "pressure_hpa": data["main"]["pressure"],
            "wind_speed": data["wind"]["speed"],
            "description": data["weather"][0]["description"]
        }
    except requests.exceptions.Timeout:
        print(f"FAILED: Connection to OpenWeather timed out for {city_name}", flush=True)
    except Exception as e:
        print(f"FAILED: {e}", flush=True)
    return None

def run_once():
    print("--- Process Started ---", flush=True)
    
    all_new_rows = []
    for city in CITIES:
        new_data = fetch_weather(city)
        if new_data:
            all_new_rows.append(new_data)
    
    if all_new_rows:
        df = pd.DataFrame(all_new_rows)
        file_exists = os.path.isfile(FILE_NAME)
        
        print(f"Saving data to {FILE_NAME}...", end=" ", flush=True)
        df.to_csv(FILE_NAME, mode='a', index=False, header=not file_exists)
        print("Saved.", flush=True)
    else:
        print("No data collected. Exiting.", flush=True)
        sys.exit(1) # Tell GitHub Actions something went wrong

    print("--- Process Completed Successfully ---", flush=True)

if __name__ == "__main__":
    run_once()