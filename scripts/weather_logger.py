import os
import sys

print("--- HELLO FROM PYTHON ---", flush=True)
print(f"Current Directory: {os.getcwd()}", flush=True)
print(f"API Key exists: {bool(os.getenv('OPENWEATHER_API_KEY'))}", flush=True)
sys.exit(0)