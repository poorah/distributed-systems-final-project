from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.types import StructType, StructField, StringType, DoubleType, TimestampType, IntegerType
from pyspark.sql.window import Window
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

# # Write the parsed data to the console
# query = parsed_stream \
#     .writeStream \
#     .outputMode("append") \
#     .format("console") \
#     .start()

parsed_stream = parsed_stream.withColumn("time", F.to_timestamp("time", "yyyy-MM-dd HH:mm:ss"))

output = parsed_stream \
    .withWatermark("time", "2 minutes") \
    .groupBy("stock_symbol", F.window("time", "1 minutes", "1 minutes")) \
    .agg(
        F.avg("closing_price").alias("MA"),
        ((F.avg("closing_price")+F.last("closing_price"))/2).alias("EMA"),
        (100/((F.avg("high")/F.avg("low"))+1)).alias("RSI"),
        F.skewness("closing_price").alias("skewness"),
        F.stddev("closing_price").alias("stddev"),
        F.count("time").alias("count")
    ) \
    .orderBy(F.col("window.start"), "stock_symbol")

# # Select the required columns
# output = parsed_stream.select(
#     "stock_symbol", "time", "closing_price", "ma", "ema", "rsi"
# )

# Write the output to the console in real-time with a 10-second trigger
query = output \
    .writeStream \
    .outputMode("complete") \
    .trigger(processingTime="10 seconds") \
    .format("console") \
    .start()

#Wait for the query to terminate (streaming continues)
query.awaitTermination()