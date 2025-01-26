from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
import boto3
import snowflake.connector
from kafka import KafkaConsumer
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Snowflake connection parameters
SNOWFLAKE_CONN_PARAMS = {
    'user': os.getenv('SNOWFLAKE_USER'),
    'password': os.getenv('SNOWFLAKE_PASSWORD'),
    'account': os.getenv('SNOWFLAKE_ACCOUNT'),
    'warehouse': os.getenv('SNOWFLAKE_WAREHOUSE'),
    'database': os.getenv('SNOWFLAKE_DATABASE'),
    'schema': os.getenv('SNOWFLAKE_SCHEMA')
}

# S3 client
s3_client = boto3.client(
    's3',
    aws_access_key_id=os.getenv('access_key'),
    aws_secret_access_key=os.getenv('secret_key'),
    region_name=os.getenv('region')
)

# Kafka consumer
consumer = KafkaConsumer(
    'your_topic',
    bootstrap_servers=['your_kafka_server'],
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='your_group_id',
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'etl_pipeline',
    default_args=default_args,
    description='ETL pipeline for Snowflake',
    schedule_interval=timedelta(days=1),
)

def extract_from_s3():
    bucket_name = os.getenv('bucket')
    prefix = os.getenv('equity_prefix')
    response = s3_client.list_objects_v2(Bucket=bucket_name, Prefix=prefix)
    data = []
    for obj in response.get('Contents', []):
        file_obj = s3_client.get_object(Bucket=bucket_name, Key=obj['Key'])
        file_data = json.loads(file_obj['Body'].read().decode('utf-8'))
        data.extend(file_data['data'])
    return data

def extract_from_kafka():
    data = []
    for message in consumer:
        data.append(message.value)
    return data

def load_to_snowflake(data):
    conn = snowflake.connector.connect(**SNOWFLAKE_CONN_PARAMS)
    cursor = conn.cursor()
    for record in data:
        cursor.execute("""
            INSERT INTO your_table (symbol, sector, price, volume, timestamp, change_percent, market_cap, volatility)
            VALUES (%(symbol)s, %(sector)s, %(price)s, %(volume)s, %(timestamp)s, %(change_percent)s, %(market_cap)s, %(volatility)s)
        """, record)
    conn.commit()
    cursor.close()
    conn.close()

def etl_task():
    s3_data = extract_from_s3()
    kafka_data = extract_from_kafka()
    combined_data = s3_data + kafka_data
    load_to_snowflake(combined_data)

etl = PythonOperator(
    task_id='etl_task',
    python_callable=etl_task,
    dag=dag,
)
