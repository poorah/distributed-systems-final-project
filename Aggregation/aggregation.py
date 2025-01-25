import json
from kafka import KafkaConsumer
import psycopg2
from psycopg2 import sql
import os

# Kafka Consumer Configuration
KAFKA_BROKER = 'localhost:9092'  # Kafka broker address
KAFKA_TOPIC = 'buysell-topic'    # Kafka topic name
GROUP_ID = 'my-consumer-group'   # Consumer group id

# PostgreSQL Configuration
PG_HOST = 'localhost'            # PostgreSQL host (localhost or IP)
PG_PORT = 5432                   # PostgreSQL port
PG_DBNAME = 'dsfinal'       # PostgreSQL database name
PG_USER = 'pooya'         # PostgreSQL user
PG_PASSWORD = '1234' # PostgreSQL password

# Setup Kafka Consumer
consumer = KafkaConsumer(
    KAFKA_TOPIC,
    bootstrap_servers=[KAFKA_BROKER],
    group_id=GROUP_ID,
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))  # Decode JSON message
)

# Setup PostgreSQL connection
def get_pg_connection():
    try:
        connection = psycopg2.connect(
            host=PG_HOST,
            port=PG_PORT,
            dbname=PG_DBNAME,
            user=PG_USER,
            password=PG_PASSWORD
        )
        return connection
    except Exception as e:
        print(f"Error connecting to PostgreSQL: {e}")
        return None

# Insert data into PostgreSQL
def insert_data_into_pg(data):
    conn = get_pg_connection()
    if conn:
        cursor = conn.cursor()
        try:
            # Adjust the table and column names as per your requirements
            insert_query = sql.SQL("""
                INSERT INTO signals (timestamp, signal_type, value)
                VALUES (%s, %s, %s)
            """)
            cursor.execute(insert_query, (data['timestamp'], data['signal_type'], data['value']))
            conn.commit()
            print(f"Data inserted: {data}")
        except Exception as e:
            print(f"Error inserting data into PostgreSQL: {e}")
        finally:
            cursor.close()
            conn.close()
    else:
        print("Failed to connect to PostgreSQL")

# Read and process Kafka messages
def process_kafka_messages():
    for message in consumer:
        data = message.value  # Assuming the message is a JSON object
        print(f"Received message: {data}")

        # Insert data into PostgreSQL
        insert_data_into_pg(data)

if __name__ == '__main__':
    process_kafka_messages()
