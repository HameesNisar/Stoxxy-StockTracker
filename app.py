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
    
    url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}.BSE&apikey={API_KEY}"
    
    try:
        response = requests.get(url, timeout=10)
        data = response.json()
        
        if "Global Quote" in data and data["Global Quote"]:
            quote = data["Global Quote"]
            price = float(quote.get("05. price", 0))
            change = float(quote.get("09. change", 0))
            
            stock_info = {
                'symbol': symbol,
                'price': round(price, 2),
                'change': round(change, 2),
                'direction': 'up' if change >= 0 else 'down'
            }
            
            return jsonify(stock_info)
        else:
            return jsonify({'error': 'Stock not found'})
            
    except Exception as e:
        return jsonify({'error': 'API error'})

# Remove the /api/history route since we'll handle history client-side

if __name__ == '__main__':
    app.run(debug=True)
