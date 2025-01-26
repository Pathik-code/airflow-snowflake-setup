import boto3
import pandas as pd
import numpy as np
from datetime import datetime
import time
import json

class MutualFundDataGenerator:
    def __init__(self):
        self.s3_client = boto3.client('s3')
        self.bucket_name = 'your-bucket-name'
        self.mutual_funds = {
            'Growth Fund': {'nav': 45.0, 'volatility': 0.01, 'category': 'Equity'},
            'Balanced Fund': {'nav': 30.0, 'volatility': 0.008, 'category': 'Hybrid'},
            'Debt Fund': {'nav': 25.0, 'volatility': 0.005, 'category': 'Debt'},
            'Index Fund': {'nav': 50.0, 'volatility': 0.012, 'category': 'Index'},
            'Small Cap Fund': {'nav': 35.0, 'volatility': 0.015, 'category': 'Equity'}
        }

    def generate_mf_data(self):
        current_time = datetime.now()
        mf_data = []


        for name, info in self.mutual_funds.items():
            # Generate NAV changes
            nav_change = np.random.normal(0, info['volatility'])
            new_nav = info['nav'] * (1 + nav_change)
            self.mutual_funds[name]['nav'] = new_nav

            # Calculate AUM (Assets Under Management)
            aum = np.random.normal(1000000000, 200000000)

            mf_data.append({
                'fund_name': name,
                'category': info['category'],
                'nav': round(new_nav, 4),
                'aum': round(aum, 2),
                'timestamp': current_time.isoformat(),
                'change_percent': round(nav_change * 100, 3),
                'expense_ratio': round(np.random.uniform(0.5, 2.0), 2)
            })

        return mf_data

    def upload_to_s3(self, data):
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'mutual_fund_data_{timestamp}.json'

        try:
            self.s3_client.put_object(
                Bucket=self.bucket_name,
                Key=f'mutual_funds/{filename}',
                Body=json.dumps(data)
            )
            print(f"Uploaded {filename} to S3")
        except Exception as e:
            print(f"Error uploading to S3: {str(e)}")

def main():
    generator = MutualFundDataGenerator()

    while True:
        try:
            # Generate and upload data
            data = generator.generate_mf_data()
            generator.upload_to_s3(data)

            # Wait for 1 minute before next update
            time.sleep(60)
        except Exception as e:
            print(f"Error: {str(e)}")
            time.sleep(60)  # Wait before retrying

if __name__ == "__main__":
    main()
