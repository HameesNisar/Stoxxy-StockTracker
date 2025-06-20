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
    
    urls = [
        f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}.BSE&apikey={API_KEY}",
        f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}.NSE&apikey={API_KEY}",
        f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={API_KEY}"
    ]
    
    for url in urls:
        try:
            response = requests.get(url, timeout=10)
            data = response.json()
            
            if "Note" in data:
                return jsonify({'error': 'API limit reached. Please try again later.'})
            
            if "Global Quote" in data and data["Global Quote"]:
                quote = data["Global Quote"]
                
                # **Remove the price == "0.0000" check**
                if not quote or "05. price" not in quote:
                    continue
                
                price = float(quote["05. price"])
                change = float(quote.get("09. change", 0))
    
                return jsonify({
                    'symbol': symbol,
                    'price': round(price, 2),
                    'change': round(change, 2),
                    'direction': 'up' if change >= 0 else 'down'
                })
                
        except Exception:
            continue
    
    return jsonify({'error': 'Stock not found. Please check the symbol and try again.'})


if __name__ == '__main__':
    app.run(debug=True)
