from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.types import StructType, StructField, StringType, DoubleType, TimestampType, IntegerType
import os

os.environ['PYSPARK_SUBMIT_ARGS'] = '--packages org.apache.spark:spark-streaming-kafka-0-10_2.12:3.2.0,org.apache.spark:spark-sql-kafka-0-10_2.12:3.2.0 pyspark-shell'

# Initialize SparkSession with Kafka support
spark = SparkSession.builder \
    .appName("TradingIndicators") \
    .getOrCreate()

spark.sparkContext.setLogLevel("WARN")

# Define the schema for Kafka data
schema = StructType([
    StructField("closing_price", DoubleType(), True),
    StructField("high", DoubleType(), True),
    StructField("low", DoubleType(), True),
    StructField("opening_price", DoubleType(), True),
    StructField("stock_symbol", StringType(), True),
    StructField("timestamp", DoubleType(), True),
    StructField("volume", IntegerType(), True)
])

# Read data from Kafka
kafka_stream = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "trading-topic") \
    .load()

# Parse Kafka data
parsed_stream = kafka_stream.selectExpr("CAST(value AS STRING)") \
    .withColumn("data", F.from_json(F.col("value"), schema)) \
    .withColumn("time", F.from_unixtime(F.col("data.timestamp"))) \
    .select("data.*", "time")

# Convert timestamp to timestamp type
parsed_stream = parsed_stream.withColumn("time", F.to_timestamp("time", "yyyy-MM-dd HH:mm:ss"))

# Define the windowing operation and calculated columns
output = parsed_stream \
    .withWatermark("time", "2 minutes") \
    .groupBy("stock_symbol", F.window("time", "1 minutes", "1 minutes")) \
    .agg(
        F.avg("closing_price").alias("MA"),
        ((F.avg("closing_price")+F.last("closing_price"))/2).alias("EMA"),
        (100-(100/((F.avg("high")/F.avg("low"))+1))).alias("RSI"),
        F.skewness("closing_price").alias("skewness"),
        F.stddev("closing_price").alias("stddev"),
        F.count("time").alias("count")
    ) \
    .withColumn("buy_signal", (F.col("RSI") < 50).cast("int")) \
    .withColumn("sell_signal", (F.col("RSI") > 50.2).cast("int"))

# Prepare the data to send to Kafka
kafka_output = output \
    .selectExpr(
        "CAST(stock_symbol AS STRING) AS key",  # Kafka key
        "to_json(struct(*)) AS value"  # Convert entire row to JSON string
    )

# Define checkpoint location (change the path as needed)
checkpoint_location_kafka = "/home/pooya/Desktop/distributed-systems-final-project/Processing/tmp"
checkpoint_location_console = "/home/pooya/Desktop/distributed-systems-final-project/Processing/tmp"

# Write the output to Kafka topic 'signals-topic'
kafka_query = kafka_output \
    .writeStream \
    .outputMode("complete") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("topic", "buysell-topic") \
    .option("checkpointLocation", checkpoint_location_kafka) \
    .format("kafka") \
    .start()
print("Kafka write stream started.")

# Write the output to the console in real-time with a 10-second trigger
console_query = output \
    .writeStream \
    .outputMode("complete") \
    .trigger(processingTime="10 seconds") \
    .option("checkpointLocation", checkpoint_location_console) \
    .format("console") \
    .start()

# Wait for the termination of both streams
kafka_query.awaitTermination()
console_query.awaitTermination()
