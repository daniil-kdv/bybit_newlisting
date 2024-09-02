import json
import requests

def get_bybit_token_info(symbol):
    url = f"https://api.bybit.com/v2/public/tickers?symbol={symbol}"
    response = requests.get(url)
    data = response.json()
    if data['ret_code'] == 0 and data['result']:
        return data['result'][0]
    return None

def read_new_listing_info(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        listings = json.load(file)
    return listings

def format_volume(value):
    value = float(value)
    if value >= 1_000_000_000:
        return f"{value / 1_000_000_000:.1f}b"
    elif value >= 1_000_000:
        return f"{value / 1_000_000:.1f}m"
    elif value >= 1_000:
        return f"{value / 1_000:.1f}k"
    else:
        return f"{value:.1f}"

