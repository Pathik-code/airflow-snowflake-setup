import boto3
import numpy as np
from datetime import datetime
import json
import logging
from typing import List, Dict, Any
from dotenv import load_dotenv
import os

class EquityDataGenerator:
    def __init__(self):
        """Initialize the equity data generator"""
        # Load environment variables
        load_dotenv()

        self.s3_client = boto3.client(
            's3',
            aws_access_key_id=os.getenv('access_key'),
            aws_secret_access_key=os.getenv('secret_key'),
            region_name=os.getenv('region')
        )
        self.bucket_name = os.getenv('bucket')
        self.prefix = os.getenv('equity_prefix')

        # Configure logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )

        # Define stock parameters
        self.stocks = {
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

    def generate_stock_data(self) -> List[Dict[str, Any]]:
        """Generate current stock data with price movements"""
        current_time = datetime.now()
        stock_data = []

        for symbol, info in self.stocks.items():
            try:
                # Generate random price movement
                price_change = np.random.normal(0, info['volatility'])
                new_price = info['base_price'] * (1 + price_change)

                # Update base price for next iteration (with mean reversion)
                self.stocks[symbol]['base_price'] = new_price * 0.9 + info['base_price'] * 0.1

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

    def upload_to_s3(self, data: List[Dict[str, Any]]) -> bool:
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

            self.s3_client.put_object(
                Bucket=self.bucket_name,
                Key=f'{self.prefix}{filename}',
                Body=json.dumps(payload),
                ContentType='application/json'
            )

            logging.info(f"Successfully uploaded {filename} to S3 path: {self.prefix}")
            return True

        except Exception as e:
            logging.error(f"Error uploading to S3: {str(e)}")
            return False

    def get_sector_summary(self) -> Dict[str, Any]:
        """Generate sector-wise summary of current stocks"""
        sectors = {}
        for symbol, info in self.stocks.items():
            sector = info['sector']
            if sector not in sectors:
                sectors[sector] = {
                    'count': 0,
                    'total_market_cap': 0,
                    'average_volatility': 0
                }
            sectors[sector]['count'] += 1
            sectors[sector]['average_volatility'] += info['volatility']

        # Calculate averages
        for sector in sectors.values():
            sector['average_volatility'] = round(
                (sector['average_volatility'] / sector['count']) * 100, 2
            )

        return sectors

def main():
    """Test the generator functionality"""
    generator = EquityDataGenerator()
    data = generator.generate_stock_data()
    print(json.dumps(data, indent=2))

    if generator.upload_to_s3(data):
        print("Test upload successful")

    print("\nSector Summary:")
    print(json.dumps(generator.get_sector_summary(), indent=2))

if __name__ == "__main__":
    main()
