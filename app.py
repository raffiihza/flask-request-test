from flask import Flask
import requests
import threading
import os
from concurrent.futures import ThreadPoolExecutor

app = Flask(__name__)

# ... (rest of the code is the same as the previous version)
def make_single_request(url, timeout):
    """
    Function to make a single HTTP GET request with a specific timeout.
    It includes basic error handling.
    """
    try:
        response = requests.get(url, timeout=timeout)
        print(f"Visited {url} with status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while visiting {url}: {e}")

def visit_webpage_multiple_times(url, count, timeout):
    """
    Uses a ThreadPoolExecutor to concurrently send a specified number of requests.
    """
    with ThreadPoolExecutor(max_workers=10) as executor:
        for _ in range(count):
            executor.submit(make_single_request, url, timeout)
    print(f"Finished sending {count} background requests to {url}.")

@app.route('/')
def index():
    """
    Main route that reads environment variables, triggers the background task,
    and immediately returns "OK".
    """
    target_url = os.environ.get('TARGET_URL', 'https://www.google.com')
    try:
        request_count = int(os.environ.get('REQUEST_COUNT', '1'))
    except ValueError:
        print("Invalid REQUEST_COUNT. Defaulting to 1.")
        request_count = 1
    try:
        timeout = int(os.environ.get('TIMEOUT', '10'))
    except ValueError:
        print("Invalid TIMEOUT. Defaulting to 10.")
        timeout = 10
    
    background_thread = threading.Thread(
        target=visit_webpage_multiple_times,
        args=(target_url, request_count, timeout)
    )
    background_thread.daemon = True
    background_thread.start()

    return "OK"

if __name__ == '__main__':
    # This part is mainly for local development, not for production with Gunicorn
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
