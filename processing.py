import requests
from kafka import KafkaProducer
import json
import time
import socket
import threading
import json

# تنظیمات Kafka
KAFKA_BROKER = 'localhost:9092'
topic = 'trading-topic'

# ایجاد تولیدکننده (Producer)
producer = KafkaProducer(
    bootstrap_servers=KAFKA_BROKER,
    value_serializer=lambda v: json.dumps(v).encode('utf-8')  # تبدیل پیام به JSON
)

# URL = "http://localhost:5000/ingest"

try:
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(("127.0.0.1", 5555))
    print("Connected to the server.")
    while True:
        # response = requests.get(URL)
        client.send('data'.encode("utf-8"))
        try:
            response = client.recv(10240).decode("utf-8")
            if response:
                print(f"Received data: {response}")
                try:
                    json_data = json.loads(response)
                    producer.send(topic, value=json_data)
                    print("Data sent to Kafka")
                except json.JSONDecodeError:
                    print("Failed to decode response as JSON.")
        except ConnectionResetError:
            print("Connection was reset by the server.")
            break
        # finally:
        #     client.close()
        time.sleep(5)

except KeyboardInterrupt:
    client.send('finish'.encode("utf-8"))
    print("Stopped by user")
finally:
    producer.close()
    client.close()
