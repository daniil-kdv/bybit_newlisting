import json
import re
from django.shortcuts import render
from .utils import get_bybit_token_info, read_new_listing_info
import yfinance as yf
import os
from bs4 import BeautifulSoup
import requests


def load_symbols_from_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        listings = json.load(file)
    return listings

def get_yfinance_symbol(listing):
    return listing.get('yfinance', '')

def index(request):
    return render(request, 'main/index.html')

def new_listing(request):
    file_path = "/home/rook1e/project/bybit/kirby/new_listing.json"
    listings = read_new_listing_info(file_path)

    for listing in listings:
        try:
            token_info = get_bybit_token_info(listing['symbol'])
            if token_info:
                listing.update({
                    'last_price': token_info.get('last_price', 'N/A'),
                    'volume_24h': token_info.get('volume_24h', 'N/A'),
                    'high_price_24h': token_info.get('high_price_24h', 'N/A'),
                    'low_price_24h': token_info.get('low_price_24h', 'N/A')
                })
            else:
                set_listing_na(listing)
        except Exception as e:
            set_listing_na(listing)
            log_error(f"Error fetching data for {listing['symbol']}: {e}")

    return render(request, 'main/new_listing.html', {'listings': listings})

def set_listing_na(listing):
    listing.update({
        'last_price': 'N/A',
        'volume_24h': 'N/A',
        'high_price_24h': 'N/A',
        'low_price_24h': 'N/A'
    })

def log_error(message):
    # 여기에 에러를 로그 파일에 기록하는 코드를 추가하세요.
    print(message)

def calculate_rsi(data, window=14):
    delta = data['Close'].diff(1)
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)

    avg_gain = gain.rolling(window=window, min_periods=1).mean()
    avg_loss = loss.rolling(window=window, min_periods=1).mean()

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))

    return rsi

def get_crypto_data(symbols, interval='1d'):
    crypto_data = []
    for symbol in symbols:
        try:
            data = yf.download(symbol, period='max', interval=interval)
            if not data.empty:
                data['RSI'] = calculate_rsi(data)
                latest_data = data.iloc[-1]
                crypto_data.append(format_crypto_data(symbol, latest_data))
            else:
                log_error(f"No data found for symbol: {symbol}")
        except Exception as e:
            log_error(f"Failed to download data for symbol: {symbol}. Error: {e}")
            crypto_data.append({
                'symbol': symbol,
                'rsi': 'Error',
                'price': 'Error'
            })
    return crypto_data

def format_crypto_data(symbol, data):
    if data['RSI'] >= 20:
        return {
            'symbol': symbol,
            'rsi': data['RSI'],
            'price': data['Close']
        }
    return {
        'symbol': symbol,
        'rsi': 'N/A',
        'price': 'N/A'
    }

def rsi_heatmap(request):
    intervals = ['1d', '1wk', '1mo']
    file_path = "/home/rook1e/project/bybit/kirby/new_listing.json"
    
    listings = load_symbols_from_json(file_path)
    crypto_symbols = [get_yfinance_symbol(listing) for listing in listings]

    heatmaps = {interval: get_crypto_data(crypto_symbols, interval) for interval in intervals}

    return render(request, 'main/rsi_heatmap.html', {'heatmaps': heatmaps})

def load_notices():
    notices_dir = "/home/rook1e/project/bybit/kirby/notices"
    notices = []
    for filename in os.listdir(notices_dir):
        if filename.endswith(".md"):
            with open(os.path.join(notices_dir, filename), "r", encoding="utf-8") as file:
                content = file.read()
                notices.append({"title": filename[:-3], "content": content})
    return notices

def notice(request):
    notices = load_notices()
    return render(request, 'main/notice.html', {'notices': notices})

def get_latest_news(link):
    try:
        response = requests.get(link)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')
        news_items = []

        # 뉴스 아이템을 선택하는 CSS 선택자를 웹사이트 구조에 맞게 수정해야 합니다.
        for item in soup.select('.sc-16r8icm-0.escjiH')[:10]:  # 예시 CSS 선택자
            title = item.select_one('.sc-16r8icm-0.escjiH .sc-1eb5slv-0 .link').text.strip()  # 예시 CSS 선택자
            date = item.select_one('.sc-16r8icm-0.escjiH .sc-1eb5slv-0 .date').text.strip()  # 예시 CSS 선택자
            news_items.append({'title': title, 'date': date})

        return news_items
    except Exception as e:
        print(f"Error fetching news: {e}")
        return []

def news_feed(request):
    file_path = "/home/rook1e/project/bybit/kirby/new_listing.json"  # 실제 파일 경로로 변경하세요
    with open(file_path, 'r', encoding='utf-8') as f:
        coins = json.load(f)

    for coin in coins:
        coin['news'] = get_latest_news(coin['link'])

    return render(request, 'main/news_feed.html', {'coins': coins})
