from flask import Flask, render_template, jsonify, request
import requests
import os
from dotenv import load_dotenv
import logging
import json

app = Flask(__name__)
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/stock')
def get_stock():
    symbol = request.args.get('symbol', '').upper()
    if not symbol:
        return jsonify({'error': 'No symbol provided'})
    
    # NSE India API (Free and works for Indian stocks)
    nse_url = f"https://www.nseindia.com/api/quote-equity?symbol={symbol}"
    
    # Headers to mimic browser request (NSE requires this)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.9',
        'Referer': 'https://www.nseindia.com/',
        'sec-ch-ua': '"Google Chrome";v="91", "Chromium";v="91", ";Not A Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
    }
    
    try:
        logger.info(f"Fetching data for symbol: {symbol}")
        
        # First get cookies by visiting NSE homepage
        session = requests.Session()
        session.get('https://www.nseindia.com', headers=headers, timeout=10)
        
        # Now get the stock data
        response = session.get(nse_url, headers=headers, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        logger.info(f"NSE API Response: {json.dumps(data, indent=2)}")
        
        # Extract stock information from NSE API response
        if 'priceInfo' in data:
            price_info = data['priceInfo']
            
            # Get current price
            current_price = price_info.get('lastPrice', 0)
            previous_close = price_info.get('previousClose', 0)
            
            if current_price and previous_close:
                change = current_price - previous_close
                
                stock_info = {
                    'symbol': symbol,
                    'price': round(float(current_price), 2),
                    'change': round(float(change), 2),
                    'direction': 'up' if change >= 0 else 'down'
                }
                
                logger.info(f"Successfully found stock data: {stock_info}")
                return jsonify(stock_info)
        
        # If NSE doesn't work, try Yahoo Finance as backup
        logger.info("NSE API didn't return expected data, trying Yahoo Finance backup...")
        return get_stock_yahoo_backup(symbol)
        
    except Exception as e:
        logger.error(f"NSE API error: {str(e)}")
        # Try Yahoo Finance backup
        return get_stock_yahoo_backup(symbol)

def get_stock_yahoo_backup(symbol):
    """Backup function using Yahoo Finance"""
    try:
        # Yahoo Finance API for Indian stocks
        yahoo_url = f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}.NS"
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        response = requests.get(yahoo_url, headers=headers, timeout=8)
        response.raise_for_status()
        
        data = response.json()
        
        if 'chart' in data and data['chart']['result']:
            result = data['chart']['result'][0]
            meta = result['meta']
            
            current_price = meta.get('regularMarketPrice', 0)
            previous_close = meta.get('previousClose', 0)
            
            if current_price and previous_close:
                change = current_price - previous_close
                
                stock_info = {
                    'symbol': symbol,
                    'price': round(float(current_price), 2),
                    'change': round(float(change), 2),
                    'direction': 'up' if change >= 0 else 'down'
                }
                
                logger.info(f"Yahoo Finance backup successful: {stock_info}")
                return jsonify(stock_info)
        
        # If both fail, try BSE suffix
        logger.info("Trying BSE suffix...")
        yahoo_bse_url = f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}.BO"
        response = requests.get(yahoo_bse_url, headers=headers, timeout=8)
        response.raise_for_status()
        
        data = response.json()
        
        if 'chart' in data and data['chart']['result']:
            result = data['chart']['result'][0]
            meta = result['meta']
            
            current_price = meta.get('regularMarketPrice', 0)
            previous_close = meta.get('previousClose', 0)
            
            if current_price and previous_close:
                change = current_price - previous_close
                
                stock_info = {
                    'symbol': symbol,
                    'price': round(float(current_price), 2),
                    'change': round(float(change), 2),
                    'direction': 'up' if change >= 0 else 'down'
                }
                
                logger.info(f"Yahoo Finance BSE backup successful: {stock_info}")
                return jsonify(stock_info)
        
    except Exception as e:
        logger.error(f"Yahoo Finance backup error: {str(e)}")
    
    return jsonify({'error': 'Stock not found. Please check the symbol and try again.'})

if __name__ == '__main__':
    app.run(debug=True)
