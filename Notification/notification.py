from pyspark.sql import SparkSession
from pyspark.sql.functions import col
from twilio.rest import Client
import json
import os
os.environ['PYSPARK_SUBMIT_ARGS'] = '--packages org.apache.spark:spark-streaming-kafka-0-10_2.12:3.2.0,org.apache.spark:spark-sql-kafka-0-10_2.12:3.2.0 pyspark-shell'
# Step 1: Initialize Spark session for reading from Kafka
spark = SparkSession.builder \
    .appName("KafkaToSMS") \
    .getOrCreate()

# Set the Kafka server and topic
kafka_server = "localhost:9092"  # Update with your Kafka server address
topic = "buysell-topic"  # The Kafka topic you want to read from

# Read data from Kafka
kafka_stream = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", kafka_server) \
    .option("subscribe", topic) \
    .load()

# Decode the value column from Kafka as string (assuming JSON format)
messages = kafka_stream.selectExpr("CAST(value AS STRING) as message")

# Step 2: Define function to send SMS
def send_sms(message):
    # Twilio credentials
    account_sid = "your_account_sid"
    auth_token = "your_auth_token"
    from_phone = "your_twilio_phone_number"
    to_phone = "recipient_phone_number"  # The phone number to receive the SMS

    # Initialize Twilio client
    client = Client(account_sid, auth_token)
    
    # Send SMS
    message = client.messages.create(
        body=message,
        from_=from_phone,
        to=to_phone
    )
    print(f"Message sent: {message.sid}")

# Step 3: Process and send SMS for each incoming message
def process_message(message):
    print(f"Received message: {message}")
    
    # Send SMS with the message content
    send_sms(message)

# Step 4: Write a foreachBatch to process each microbatch of data
def process_batch(df, epoch_id):
    # Collect the messages in this batch and process them
    for row in df.collect():
        message = row["message"]
        process_message(message)

# Step 5: Start the streaming query
query = messages.writeStream \
    .foreachBatch(process_batch) \
    .outputMode("append") \
    .start()

# Wait for the termination of the query (it will continue indefinitely)
query.awaitTermination()
