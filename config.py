import boto3
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Initialize S3 client
s3_client = boto3.client(
    's3',
    aws_access_key_id=os.getenv('access_key'),
    aws_secret_access_key=os.getenv('secret_key'),
    region_name=os.getenv('region')
)

# S3 Configuration
S3_CONFIG = {
    'bucket_name': os.getenv('bucket'),
    'equity_prefix': os.getenv('equity_prefix'),
    'commodity_prefix': os.getenv('commodity_prefix'),
    'mutualfund_prefix': os.getenv('mutualfund_prefix')
}
