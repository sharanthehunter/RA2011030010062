from flask import Flask, request, jsonify
import requests
import threading
import time

app = Flask(__name__)

def fetch_numbers(url):
    try:
        response = requests.get(url, timeout=2)
        if response.status_code == 200:
            data = response.json()
            return data.get("numbers", [])
        return []
    except requests.Timeout:
        return []

def merge_sort(numbers_lists):
    merged_numbers = []
    for numbers in numbers_lists:
        merged_numbers.extend(numbers)
    merged_numbers = sorted(set(merged_numbers))
    return merged_numbers

@app.route('/numbers', methods=['GET'])
def get_merged_numbers():
    urls = request.args.getlist('url')
    start_time = time.time()

    threads = []
    numbers_lists = []

    for url in urls:
        thread = threading.Thread(target=lambda u: numbers_lists.append(fetch_numbers(u)), args=(url,))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    merged_numbers = merge_sort(numbers_lists)
    end_time = time.time()

    response = {
        "numbers": merged_numbers
    }

    if end_time - start_time > 0.5:
        return jsonify(response), 500
    else:
        return jsonify(response), 200

if __name__ == '__main__':
    app.run(host='localhost', port=8080)
