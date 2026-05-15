import os
import sys
import requests
from datetime import datetime

# Direct logging to bypass buffering
def log(msg):
    print(msg, flush=True)

log("--- STARTING WEATHER LOGGER ---")

API_KEY = os.getenv("OPENWEATHER_API_KEY")
FILE_NAME = "overnight_weather.csv"

if not API_KEY:
    log("❌ ERROR: API Key not found in environment!")
    sys.exit(1)

try:
    log("📡 Calling OpenWeather API...")
    # Using London as a test
    url = f"https://api.openweathermap.org/data/2.5/weather?q=London&appid={API_KEY}&units=metric"
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    log("✅ API Success!")
    
    # Save a simple line to the CSV
    with open(FILE_NAME, "a") as f:
        f.write(f"{datetime.now()},London,Success\n")
    log(f"💾 Data saved to {FILE_NAME}")

except Exception as e:
    log(f"❌ ERROR: {e}")

log("--- PROCESS COMPLETE ---")