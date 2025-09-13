from flask import Flask
import requests
import threading
import os
from concurrent.futures import ThreadPoolExecutor

app = Flask(__name__)

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
    # Using a ThreadPoolExecutor to send requests in parallel for better performance.
    with ThreadPoolExecutor(max_workers=10) as executor:
        for _ in range(count):
            # Submits the make_single_request function to be executed 'count' times.
            executor.submit(make_single_request, url, timeout)
    print(f"Finished sending {count} background requests to {url}.")

@app.route('/')
def index():
    """
    Main route that reads environment variables, triggers the background task,
    and immediately returns "OK".
    """
    # Read configuration from environment variables, with defaults.
    target_url = os.environ.get('TARGET_URL', 'https://www.google.com')

    # Read and validate REQUEST_COUNT, defaulting to 1.
    try:
        request_count = int(os.environ.get('REQUEST_COUNT', '1'))
    except ValueError:
        print("Invalid REQUEST_COUNT. Defaulting to 1.")
        request_count = 1

    # Read and validate TIMEOUT, defaulting to 10.
    try:
        timeout = int(os.environ.get('TIMEOUT', '10'))
    except ValueError:
        print("Invalid TIMEOUT. Defaulting to 10.")
        timeout = 10

    # A new thread is created for the background task so the response is immediate.
    background_thread = threading.Thread(
        target=visit_webpage_multiple_times,
        args=(target_url, request_count, timeout)
    )
    background_thread.daemon = True
    background_thread.start()

    return "OK"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
