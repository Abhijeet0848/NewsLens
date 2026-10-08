"""
NewsSense Project Launcher
Starts the FastAPI application with Uvicorn and opens the web interface in the default browser.
"""

import os
import sys
import webbrowser
import threading
import time
import uvicorn

# Add project root to Python module path
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from src.data_loader import ensure_dataset_exists
from src.classifier import inference_service

def open_browser():
    time.sleep(1.5)
    url = "http://127.0.0.1:8000"
    print(f"\n[NewsSense] Opening interactive dashboard at: {url}")
    webbrowser.open(url)

def main():
    print("=" * 70)
    print("  NewsSense – News Article Category Classifier (MCA Academic Project)")
    print("=" * 70)
    print("1. Checking dataset integrity...")
    ensure_dataset_exists()
    
    print("2. Verifying trained model artifacts...")
    if not inference_service.loaded:
        inference_service.load_artifacts()

    print("3. Starting FastAPI server on http://127.0.0.1:8000 ...")
    threading.Thread(target=open_browser, daemon=True).start()
    
    uvicorn.run("src.api:app", host="127.0.0.1", port=8000, reload=False, log_level="info")

if __name__ == "__main__":
    main()
