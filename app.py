from flask import Flask, render_template, jsonify, request
import requests
import os
from dotenv import load_dotenv
import logging

app = Flask(__name__)
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

API_KEY = os.getenv("API_KEY")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/stock')
def get_stock():
    symbol = request.args.get('symbol', '').upper()
    if not symbol:
        return jsonify({'error': 'No symbol provided'})
    
    # Check if API key is available
    if not API_KEY:
        logger.error("API_KEY not found in environment variables")
        return jsonify({'error': 'API configuration error. Please try again later.'})
    
    # Optimized approach: Try BSE first (since NSE is no longer supported)
    # Then try without exchange suffix as fallback
    urls = [
        f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}.BSE&apikey={API_KEY}",
        f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={API_KEY}"
    ]
    
    for i, url in enumerate(urls):
        try:
            logger.info(f"Trying URL {i+1}: {url}")
            
            # Reduced timeout for faster failure and retry
            response = requests.get(url, timeout=8)
            response.raise_for_status()  # Raise exception for bad status codes
            
            data = response.json()
            logger.info(f"API Response: {data}")
            
            # Check for API limit error
            if "Note" in data:
                logger.warning("API limit reached")
                return jsonify({'error': 'API limit reached. Please try again later.'})
            
            # Check for API error messages
            if "Error Message" in data:
                logger.warning(f"API Error: {data['Error Message']}")
                continue
            
            # Check for valid quote data
            if "Global Quote" in data and data["Global Quote"]:
                quote = data["Global Quote"]
                
                # Check if quote has meaningful data
                if not quote:
                    logger.warning("Empty quote data")
                    continue
                
                # Get price - handle different possible keys
                price_key = "05. price"
                change_key = "09. change"
                
                # Validate that required keys exist
                if price_key not in quote or change_key not in quote:
                    logger.warning(f"Missing price or change data in quote: {quote.keys()}")
                    continue
                
                try:
                    price = float(quote.get(price_key, 0))
                    change = float(quote.get(change_key, 0))
                except (ValueError, TypeError):
                    logger.warning("Invalid price or change data")
                    continue
                
                # Additional validation - price should be greater than 0
                if price <= 0:
                    logger.warning(f"Invalid price: {price}")
                    continue
                
                stock_info = {
                    'symbol': symbol,
                    'price': round(price, 2),
                    'change': round(change, 2),
                    'direction': 'up' if change >= 0 else 'down'
                }
                
                logger.info(f"Successfully found stock data: {stock_info}")
                return jsonify(stock_info)
            else:
                logger.warning("No Global Quote data found in response")
                continue
                
        except requests.exceptions.Timeout:
            logger.warning(f"Timeout for URL {i+1}")
            continue
        except requests.exceptions.RequestException as e:
            logger.error(f"Request error for URL {i+1}: {str(e)}")
            continue
        except Exception as e:
            logger.error(f"Unexpected error for URL {i+1}: {str(e)}")
            continue
    
    logger.error(f"No valid data found for symbol: {symbol}")
    return jsonify({'error': 'Stock not found. Please check the symbol and try again.'})

if __name__ == '__main__':
    app.run(debug=True)
