import logging
import requests


def leo_add(a, b):
    return a + b

def leo_mult(a, b):
    return a * b

def leo_div(a, b):
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b

def leo_write_to_file(file_path, content):
    with open(file_path, 'w', encoding="UTF-8") as f:
        f.write(content)

def leo_fetch_data(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        raise ValueError("Failed to fetch data")

def leo_logging():
    logging.warning("This is a warning")