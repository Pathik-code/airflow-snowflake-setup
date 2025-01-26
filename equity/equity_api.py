from flask import Flask, jsonify, request
from flasgger import Swagger
from datetime import datetime
import json
import threading
import time
import numpy as np
import logging
from typing import List, Dict, Any
import sys
import os

# Add the parent directory to the system path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import s3_client, S3_CONFIG

app = Flask(__name__)
swagger = Swagger(app)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Define stock parameters
stocks = {
    'AAPL': {'base_price': 150.0, 'volatility': 0.02, 'sector': 'Technology'},
    'GOOGL': {'base_price': 2800.0, 'volatility': 0.025, 'sector': 'Technology'},
    'MSFT': {'base_price': 300.0, 'volatility': 0.018, 'sector': 'Technology'},
    'AMZN': {'base_price': 3300.0, 'volatility': 0.03, 'sector': 'Consumer'},
    'META': {'base_price': 330.0, 'volatility': 0.028, 'sector': 'Technology'},
    'TSLA': {'base_price': 250.0, 'volatility': 0.035, 'sector': 'Automotive'},
    'JPM': {'base_price': 140.0, 'volatility': 0.015, 'sector': 'Finance'},
    'V': {'base_price': 200.0, 'volatility': 0.012, 'sector': 'Finance'},
    'WMT': {'base_price': 150.0, 'volatility': 0.010, 'sector': 'Retail'},
    'PG': {'base_price': 140.0, 'volatility': 0.008, 'sector': 'Consumer'}
}

current_equity_data = {}
data_lock = threading.Lock()

def generate_stock_data() -> List[Dict[str, Any]]:
    """Generate current stock data with price movements"""
    current_time = datetime.now()
    stock_data = []

    for symbol, info in stocks.items():
        try:
            # Generate random price movement
            price_change = np.random.normal(0, info['volatility'])
            new_price = info['base_price'] * (1 + price_change)

            # Update base price for next iteration (with mean reversion)
            stocks[symbol]['base_price'] = new_price * 0.9 + info['base_price'] * 0.1

            # Generate realistic volume based on price
            base_volume = int(1000000 / new_price)  # Higher for lower-priced stocks
            volume = int(np.random.normal(base_volume, base_volume * 0.2))

            stock_data.append({
                'symbol': symbol,
                'sector': info['sector'],
                'price': round(new_price, 2),
                'volume': max(0, volume),
                'timestamp': current_time.isoformat(),
                'change_percent': round(price_change * 100, 2),
                'market_cap': round(new_price * volume, 2),
                'volatility': round(info['volatility'] * 100, 2)
            })

        except Exception as e:
            logging.error(f"Error generating data for {symbol}: {str(e)}")

    return stock_data

def upload_to_s3(data: List[Dict[str, Any]]) -> bool:
    """Upload stock data to S3 with error handling"""
    try:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'equity_data_{timestamp}.json'

        # Add metadata
        payload = {
            'timestamp': datetime.now().isoformat(),
            'record_count': len(data),
            'data': data
        }

        s3_client.put_object(
            Bucket=S3_CONFIG['bucket_name'],
            Key=f'{S3_CONFIG['equity_prefix']}{filename}',
            Body=json.dumps(payload),
            ContentType='application/json'
        )

        logging.info(f"Successfully uploaded {filename} to S3 path: {S3_CONFIG['equity_prefix']}")
        return True

    except Exception as e:
        logging.error(f"Error uploading to S3: {str(e)}")
        return False

def update_equity_data():
    """Background task to continuously update equity data"""
    global current_equity_data
    while True:
        try:
            with data_lock:
                data = generate_stock_data()
                # Index data by symbol for quick lookup
                current_equity_data = {item['symbol']: item for item in data}

                # Upload to S3 as well
                upload_to_s3(data)
            time.sleep(1)  # Update every second
        except Exception as e:
            print(f"Error updating data: {str(e)}")
            time.sleep(1)

@app.route('/api/equity/current', methods=['GET'])
def get_current_prices():
    """
    Get current prices for all or specific equity
    ---
    parameters:
      - name: symbol
        in: query
        type: string
        required: false
        description: The symbol of the equity
    responses:
      200:
        description: A list of current equity prices
        schema:
          type: array
          items:
            type: object
            properties:
              symbol:
                type: string
              sector:
                type: string
              price:
                type: number
              volume:
                type: integer
              timestamp:
                type: string
              change_percent:
                type: number
              market_cap:
                type: number
              volatility:
                type: number
      404:
        description: Symbol not found
    """
    symbol = request.args.get('symbol', '').upper()

    with data_lock:
        if symbol:
            if symbol in current_equity_data:
                return jsonify(current_equity_data[symbol])
            return jsonify({"error": "Symbol not found"}), 404
        return jsonify(list(current_equity_data.values()))

@app.route('/api/equity/historical', methods=['GET'])
def get_historical_data():
    """
    Get historical data from S3
    ---
    parameters:
      - name: symbol
        in: query
        type: string
        required: false
        description: The symbol of the equity
      - name: date
        in: query
        type: string
        required: false
        description: The date of the historical data in YYYYMMDD format
    responses:
      200:
        description: A list of historical equity data
        schema:
          type: array
          items:
            type: object
            properties:
              symbol:
                type: string
              sector:
                type: string
              price:
                type: number
              volume:
                type: integer
              timestamp:
                type: string
              change_percent:
                type: number
              market_cap:
                type: number
              volatility:
                type: number
      404:
        description: No data found for symbol or date
    """
    symbol = request.args.get('symbol', '').upper()
    date = request.args.get('date', datetime.now().strftime('%Y%m%d'))

    try:
        response = s3_client.list_objects_v2(
            Bucket=S3_CONFIG['bucket_name'],
            Prefix=f"{S3_CONFIG['equity_prefix']}equity_data_{date}"
        )

        if 'Contents' in response:
            latest_file = sorted(response['Contents'], key=lambda x: x['LastModified'])[-1]
            obj = s3_client.get_object(
                Bucket=S3_CONFIG['bucket_name'],
                Key=latest_file['Key']
            )
            data = json.loads(obj['Body'].read())

            if symbol:
                data = [item for item in data if item['symbol'] == symbol]
                if not data:
                    return jsonify({"error": "No data found for symbol"}), 404

            return jsonify(data)

        return jsonify({"error": "No historical data found"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/equity/statistics', methods=['GET'])
def get_statistics():
    """
    Get statistical information about equities
    ---
    responses:
      200:
        description: Statistical information about equities
        schema:
          type: object
          properties:
            total_stocks:
              type: integer
            total_volume:
              type: integer
            total_market_cap:
                type: number
            highest_price:
              type: object
              properties:
                symbol:
                  type: string
                sector:
                  type: string
                price:
                  type: number
                volume:
                  type: integer
                timestamp:
                  type: string
                change_percent:
                  type: number
                market_cap:
                  type: number
                volatility:
                  type: number
            lowest_price:
              type: object
              properties:
                symbol:
                  type: string
                sector:
                  type: string
                price:
                  type: number
                volume:
                  type: integer
                timestamp:
                  type: string
                change_percent:
                  type: number
                market_cap:
                  type: number
                volatility:
                  type: number
            timestamp:
              type: string
      404:
        description: No data available
    """
    with data_lock:
        if not current_equity_data:
            return jsonify({"error": "No data available"}), 404

        stats = {
            "total_stocks": len(current_equity_data),
            "total_volume": sum(stock['volume'] for stock in current_equity_data.values()),
            "total_market_cap": sum(stock['market_cap'] for stock in current_equity_data.values()),
            "highest_price": max(current_equity_data.values(), key=lambda x: x['price']),
            "lowest_price": min(current_equity_data.values(), key=lambda x: x['price']),
            "timestamp": datetime.now().isoformat()
        }
        return jsonify(stats)

def main():
    # Start the background update task
    update_thread = threading.Thread(target=update_equity_data, daemon=True)
    update_thread.start()

    # Run the Flask app
    app.run(host='0.0.0.0', port=9091, debug=True)

if __name__ == '__main__':
    main()
