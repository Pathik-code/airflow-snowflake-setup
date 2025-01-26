# Mutual Fund Data Generator

Synthetic mutual fund data generator that simulates NAV changes and uploads data to S3.

## Components

- `mutual_fund_generator.py`: Generates mutual fund data

## Features

- NAV generation for different fund categories
- AUM calculation
- Expense ratio simulation
- Automatic S3 uploads
- Configurable update frequency

## Fund Categories

- Equity Funds
- Hybrid Funds
- Debt Funds
- Index Funds
- Small Cap Funds

## Configuration

1. Set AWS credentials:
```bash
export AWS_ACCESS_KEY_ID='your_access_key'
export AWS_SECRET_ACCESS_KEY='your_secret_key'
```

2. Update S3 bucket name in the generator script

## Data Format

```json
{
  "fund_name": "Growth Fund",
  "category": "Equity",
  "nav": 45.0,
  "aum": 1000000000,
  "timestamp": "2023-09-01T10:00:00",
  "change_percent": 0.5,
  "expense_ratio": 1.5
}
```

## Usage

```bash
# Start the generator
python mutual_fund_generator.py
```
