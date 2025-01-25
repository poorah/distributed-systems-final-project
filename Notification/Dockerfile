# Use official Python image as the base image
FROM python:3.10-slim

# Set environment variables for Spark (if needed)
ENV SPARK_HOME=/opt/spark
ENV PATH=$SPARK_HOME/bin:$PATH

# Install necessary dependencies
RUN apt-get update && apt-get install -y \
    openjdk-11-jdk \
    && rm -rf /var/lib/apt/lists/*

# Install PySpark and Twilio Python SDK
RUN pip install --no-cache-dir \
    pyspark \
    twilio \
    kafka-python

# Set the working directory inside the container
WORKDIR /app

# Copy the application code to the container
COPY . /app

# Set the entry point for the container
CMD ["python", "your_spark_app.py"]
