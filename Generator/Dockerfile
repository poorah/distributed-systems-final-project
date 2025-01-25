# Use the official Python image as the base image
FROM python:3.12.3-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir flask redis

# Expose the port the app runs on
EXPOSE 5000

# Run the application
CMD ["python", "app.py"]
