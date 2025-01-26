# Stock API Service

Real-time stock market data API service with continuous price updates.

## Components

- `stock_api.py`: REST API service for stock data
- Background thread for price updates
- In-memory data storage with thread-safe operations

## Features

- Real-time price updates
- Multiple stock symbols support
- Automatic price variation
- Base price maintenance
- Thread-safe operations

## API Endpoints

1. GET `/stock`
   - Get current stock prices
   - Query params: `name` (stock symbol)

## Supported Stocks

- Base prices and volatility for:
  - GOLD
  - SILVER
  - OIL
  - COPPER
  - WHEAT

## Data Format

```json
{
  "stock_name": "GOLD",
  "base_price": 1800.0,
  "current_price": 1805.25,
  "timestamp": "2023-09-01T10:00:00"
}
```

## Usage

```bash
# Start the API service
python stock_api.py

# Access endpoint
curl http://localhost:5000/stock?name=GOLD
```
