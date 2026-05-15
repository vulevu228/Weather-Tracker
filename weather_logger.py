import os
import sys
import requests

# Use a custom log function that forces the console to refresh
def log(msg):
    print(msg, flush=True)
    sys.stdout.flush()

log("--- LOG START: HELLO FROM GITHUB ---")

API_KEY = os.getenv("OPENWEATHER_API_KEY")
log(f"Checking API Key: {'Found' if API_KEY else 'NOT FOUND'}")

try:
    log("Testing network by calling Google...")
    test_res = requests.get("https://www.google.com", timeout=5)
    log(f"Network Status: {test_res.status_code}")
except Exception as e:
    log(f"Network Error: {e}")

log("--- LOG END: SUCCESS ---")