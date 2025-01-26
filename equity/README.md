# Equity Data Generator and API Service

## Project Structure
```
equity/
├── equity_generator.py
├── equity_api.py
├── README.md
```

## Overview
Real-time equity data simulation system with REST API endpoints and automatic S3 storage integration.

## Components

### 1. Equity Generator (`equity_generator.py`)
- Generates synthetic market data
- Simulates price movements for major stocks
- Handles S3 uploads automatically
- Configurable volatility per stock
- Supports stocks: AAPL, GOOGL, MSFT, AMZN, META

### 2. API Service (`equity_api.py`)
- Real-time price streaming
- Historical data access
- Market statistics
- Swagger UI documentation

## API Endpoints

1. Current Prices
```
GET /api/equity/current
GET /api/equity/current?symbol=AAPL
```

2. Historical Data
```
GET /api/equity/historical
GET /api/equity/historical?symbol=AAPL&date=20230901
```

3. Market Statistics
```
GET /api/equity/statistics
```

## Setup

1. Environment Setup
```bash
# From project root
cd equity
python -m venv venv
source venv/bin/activate  # Unix
.\venv\Scripts\activate   # Windows
pip install -r ../requirements.txt
```

2. AWS Configuration
```bash
# ~/.aws/credentials
[default]
aws_access_key_id = your_access_key
aws_secret_access_key = your_secret_key
aws_region = your_region

# Or environment variables
export AWS_ACCESS_KEY_ID='your_access_key'
export AWS_SECRET_ACCESS_KEY='your_secret_key'
export AWS_DEFAULT_REGION='your_region'
```

3. Update Configuration
```python
# equity_generator.py
self.bucket_name = 'your-bucket-name'  # Update this
```

4. Create a `.env` file in the project root with the following content:
```properties
access_key = your_access_key
secret_key = your_secret_key
region = your_region
bucket = your_bucket_name
equity_prefix = equity-data/
commodity_prefix = commodity-data/
mutualfund_prefix = mutualfund-data/
```

## Usage

1. Start the Service
```bash
# From equity directory
python equity_api.py
```

2. Access Swagger UI
Open your browser and navigate to `http://localhost:9091/apidocs/` to view the API documentation.

3. Example API Calls
```bash
# Get all current prices
curl http://localhost:9091/api/equity/current

# Get specific stock
curl http://localhost:9091/api/equity/current?symbol=AAPL

# Get historical data
curl http://localhost:9091/api/equity/historical?symbol=AAPL&date=20230901

# Get market statistics
curl http://localhost:9091/api/equity/statistics
```

## Data Format

### Current Price Response
```json
{
    "symbol": "AAPL",
    "price": 150.25,
    "volume": 100000,
    "timestamp": "2023-09-01T10:00:00",
    "change_percent": 0.5,
    "market_cap": 2500000000
}
```

### Statistics Response
```json
{
    "total_stocks": 5,
    "total_volume": 500000,
    "total_market_cap": 10000000000,
    "highest_price": {"symbol": "GOOGL", "price": 2800.00},
    "lowest_price": {"symbol": "META", "price": 330.00},
    "timestamp": "2023-09-01T10:00:00"
}
```

## Available Stocks

### Technology Sector
- AAPL (Apple)
- GOOGL (Google)
- MSFT (Microsoft)
- META (Meta)

### Consumer Sector
- AMZN (Amazon)
- PG (Procter & Gamble)

### Automotive Sector
- TSLA (Tesla)

### Finance Sector
- JPM (JPMorgan)
- V (Visa)

### Retail Sector
- WMT (Walmart)

## Data Features
- Real-time price simulation
- Sector-based categorization
- Volume-based calculations
- Mean reversion in price movements
- Volatility tracking
- Market cap calculations

## Error Handling
- 404: Symbol not found
- 500: Server/S3 errors
- Automatic retry for data updates
- Thread-safe operations

## Monitoring
- Console logging for S3 uploads
- Error logging for failed operations
- Real-time data update status
