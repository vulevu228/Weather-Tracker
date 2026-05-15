import os
import sys

# Force the log to show up immediately
print("--- PYTHON SANITY TEST START ---", flush=True)

try:
    print(f"Current Working Directory: {os.getcwd()}", flush=True)
    api_key = os.getenv("OPENWEATHER_API_KEY")
    print(f"API Key found: {bool(api_key)}", flush=True)
    
    # Try to write a test line to the CSV
    with open("overnight_weather.csv", "a") as f:
        f.write("test_run,success\n")
    print("Successfully wrote to CSV file.", flush=True)

except Exception as e:
    print(f"An error occurred: {e}", flush=True)

print("--- PYTHON SANITY TEST COMPLETE ---", flush=True)
sys.exit(0)