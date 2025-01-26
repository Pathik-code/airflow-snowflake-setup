# Airflow Snowflake Setup

## Overview

This project provides a comprehensive setup for integrating Apache Airflow with Snowflake. It includes real-time data simulation, ETL pipelines, and REST API services for equity, commodity, and mutual fund data. The project leverages AWS S3 for data storage and Kafka for real-time data streaming.

## Project Structure
```

.
├── airflow/
│ ├── dags/
│ │ └──

etl_pipeline.py

│ ├──

docker-compose.yaml

│ ├── .env
│ └──

README.md

├── commodity/
│ ├──

commodity_api.py

│ └──

README.md

├── equity/
│ ├──

equity_api.py

│ ├──

equity_generator.py

│ └──

README.md

├── mutualfund/
│ ├──

mutual_fund_upload.py

│ └──

README.md

├──

config.py

├──

requirements.txt

└──

README.md

````

## Components

### 1. Airflow

- **DAGs**: Defines the ETL pipeline for processing and loading data into Snowflake.
- **Docker Compose**: Sets up the Airflow environment with PostgreSQL and Redis.

### 2. Equity

- **Equity Generator**: Simulates real-time stock data and uploads it to S3.
- **API Service**: Provides REST endpoints for accessing current and historical equity data.

### 3. Commodity

- **API Service**: Provides REST endpoints for accessing real-time commodity data.

### 4. Mutual Fund

- **Data Generator**: Simulates mutual fund data and uploads it to S3.

## Setup

### Prerequisites

- Docker
- Docker Compose
- Python 3.8+
- AWS Account
- Snowflake Account

### Installation

1. **Clone the repository**:
    ```sh
    git clone https://github.com/your-repo/airflow-snowflake-setup.git
    cd airflow-snowflake-setup
    ```

2. **Set up the virtual environment**:
    ```sh
    python -m venv myenv
    source myenv/bin/activate  # Unix
    .\myenv\Scripts\activate   # Windows
    ```

3. **Install dependencies**:
    ```sh
    pip install -r requirements.txt
    ```

4. **Configure environment variables**:
    - Update the

.env

 file with your AWS and Snowflake credentials.

5. **Initialize Airflow**:
    ```sh
    cd airflow
    docker-compose up airflow-init
    ```

6. **Start Airflow services**:
    ```sh
    docker-compose up -d
    ```

## Usage

### Accessing Airflow

- **Web UI**: [http://localhost:4040](http://localhost:4040)
- **Default credentials**:
  - Username:

airflow


  - Password:

airflow



### Running the API Services

1. **Equity API**:
    ```sh
    cd equity
    python equity_api.py
    ```

2. **Commodity API**:
    ```sh
    cd commodity
    python commodity_api.py
    ```

## API Endpoints

### Equity API

- **Current Prices**:
    ```
    GET /api/equity/current
    GET /api/equity/current?symbol=AAPL
    ```

- **Historical Data**:
    ```
    GET /api/equity/historical
    GET /api/equity/historical?symbol=AAPL&date=20230901
    ```

- **Market Statistics**:
    ```
    GET /api/equity/statistics
    ```

### Commodity API

- **Current Stock Data**:
    ```
    GET /current_stock
    GET /current_stock?name=GOLD
    ```

- **Update Stock Data**:
    ```
    POST /update_stock
    ```

## Data Format

### Equity API Response

```json
{
    "symbol": "AAPL",
    "price": 150.25,
    "volume": 100000,
    "timestamp": "2023-09-01T10:00:00",
    "change_percent": 0.5,
    "market_cap": 2500000000
}
````

### Commodity API Response

```json
{
  "stock_name": "GOLD",
  "base_price": 1800.0,
  "current_price": 1820.0,
  "timestamp": "2023-09-01T10:00:00"
}
```

## Monitoring

- **Logs**: Available in the `./logs` directory.
- **Container Logs**: Use `docker-compose logs -f` to view logs.

## Stopping Services

```sh
docker-compose down
```

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.
