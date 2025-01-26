# Airflow Setup for Market Data Processing

## Directory Structure
```
airflow/
├── dags/
│   └── market_data_dag.py
├── logs/
├── plugins/
├── docker-compose.yaml
├── .env
└── README.md
```

## Initial Setup

1. Create required directories:
```bash
mkdir -p ./dags ./logs ./plugins
chmod -R 777 ./dags ./logs ./plugins
```

2. Initialize the database:
```bash
# Initialize Airflow database and create first user
docker-compose up airflow-init

# Wait for initialization to complete
# You should see "User created successfully" message
```

3. Start Airflow services:
```bash
# Start all services
docker-compose up -d

# Verify services are running
docker-compose ps
```

4. Access Airflow:
- Web UI: http://localhost:4040
- Default credentials:
  - Username: airflow
  - Password: airflow

## Accessing Airflow

- Web UI: http://localhost:8080
- Default credentials:
  - Username: airflow
  - Password: airflow

## Available DAGs

### Market Data Pipeline
- Runs every 5 minutes
- Processes equity and commodity data
- Uploads results to S3

## Monitoring

- Logs are available in ./logs directory
- Container logs: `docker-compose logs -f`

## Stopping Services

```bash
docker-compose down
```
````
