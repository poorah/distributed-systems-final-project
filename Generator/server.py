from flask import Flask, request, jsonify
import redis
import json

app = Flask(__name__)

# Configure Redis connection
redis_client = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)

# Redis key to store data
REDIS_KEY = "ingested_data"

@app.route('/ingest', methods=['POST'])
def ingest_data():
    """Handle POST request to ingest data."""
    try:
        # Extract JSON data from the request
        data = request.get_json()
        if data:
            # Store data in Redis
            redis_client.set(REDIS_KEY, json.dumps(data))
            return jsonify({"message": "Data ingested successfully"}), 200
        else:
            return jsonify({"error": "Invalid data"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/ingest', methods=['GET'])
def fetch_data():
    """Handle GET request to retrieve data."""
    try:
        # Fetch data from Redis
        data = redis_client.get(REDIS_KEY)
        if data:
            return jsonify(json.loads(data)), 200
        else:
            return jsonify({"message": "No data found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
