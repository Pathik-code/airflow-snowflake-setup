from flask import Flask, jsonify, request
import random
import time
import threading
from datetime import datetime
import sys
import os

# Add the parent directory to the system path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import s3_client, S3_CONFIG

app = Flask(__name__)

# Base prices for different commodity stocks
base_prices = {
    "GOLD": 1800.0,  # Base price for Gold
    "SILVER": 22.0,  # Base price for Silver
    "OIL": 75.0,     # Base price for Oil
    "COPPER": 3.5,   # Base price for Copper
    "WHEAT": 8.0     # Base price for Wheat
}

# Storage for current stock data
current_stock_data = {}
data_lock = threading.Lock()

def update_stock_prices():
    """Background task to update stock prices every second"""
    while True:
        with data_lock:
            for stock_name, base_price in base_prices.items():
                price_variation = random.uniform(-0.10, 0.10)
                current_price = base_price * (1 + price_variation)

                current_stock_data[stock_name] = {
                    "stock_name": stock_name,
                    "base_price": base_price,
                    "current_price": round(current_price, 2),
                    "timestamp": datetime.now().isoformat()
                }
        time.sleep(1)  # Update every second

@app.route('/update_stock', methods=['POST'])
def update_stock():
    """Endpoint to manually update stock data"""
    data = request.get_json()
    stock_name = data.get('stock_name', '').upper()

    if stock_name not in base_prices:
        return jsonify({"error": "Invalid stock name"}), 400

    with data_lock:
        price_variation = random.uniform(-0.10, 0.10)
        current_price = base_prices[stock_name] * (1 + price_variation)

        current_stock_data[stock_name] = {
            "stock_name": stock_name,
            "base_price": base_prices[stock_name],
            "current_price": round(current_price, 2),
            "timestamp": datetime.now().isoformat()
        }

        return jsonify(current_stock_data[stock_name])

@app.route('/current_stock', methods=['GET'])
def get_current_stock():
    """Endpoint to fetch current stock data"""
    stock_name = request.args.get('name', '').upper()

    if not stock_name:
        return jsonify(current_stock_data)  # Return all stocks

    if stock_name not in base_prices:
        return jsonify({"error": "Invalid stock name"}), 400

    with data_lock:
        if stock_name in current_stock_data:
            return jsonify(current_stock_data[stock_name])
        return jsonify({"error": "Stock data not available"}), 404

if __name__ == '__main__':
    # Start the background update task
    update_thread = threading.Thread(target=update_stock_prices, daemon=True)
    update_thread.start()

    app.run(debug=True)
