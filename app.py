from flask import Flask, render_template, jsonify, request
import requests
import os
from dotenv import load_dotenv

app = Flask(__name__)
load_dotenv()

API_KEY = os.getenv("API_KEY")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/stock')
def get_stock():
    symbol = request.args.get('symbol', '').upper()
    if not symbol:
        return jsonify({'error': 'No symbol provided'})
    
    # Try multiple API endpoints for better reliability
    urls = [
        f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}.BSE&apikey={API_KEY}",
        f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}.NSE&apikey={API_KEY}",
        f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={API_KEY}"
    ]
    
    for url in urls:
        try:
            response = requests.get(url, timeout=10)
            data = response.json()
            
            # Check for API limit error
            if "Note" in data:
                return jsonify({'error': 'API limit reached. Please try again later.'})
            
            if "Global Quote" in data and data["Global Quote"]:
                quote = data["Global Quote"]
                
                # Check if quote has data
                if not quote or quote.get("05. price") == "0.0000":
                    continue
                
                price = float(quote.get("05. price", 0))
                change = float(quote.get("09. change", 0))
                
                # Additional validation
                if price == 0:
                    continue
                
                stock_info = {
                    'symbol': symbol,
                    'price': round(price, 2),
                    'change': round(change, 2),
                    'direction': 'up' if change >= 0 else 'down'
                }
                
                return jsonify(stock_info)
                
        except Exception as e:
            continue
    
    return jsonify({'error': 'Stock not found. Please check the symbol and try again.'})

if __name__ == '__main__':
    app.run(debug=True)