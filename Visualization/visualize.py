from flask import Flask, Response, jsonify
import time
import json
from confluent_kafka import Consumer, KafkaException, KafkaError

app = Flask(__name__)

# Kafka Consumer Configuration
conf = {
    'bootstrap.servers': 'localhost:9092',
    'group.id': 'signal-group',
    'auto.offset.reset': 'earliest'
}
consumer = Consumer(conf)
consumer.subscribe(['buysell-topic'])

@app.route('/stream')
def stream():
    def generate():
        try:
            while True:
                msg = consumer.poll(0.5)
                if msg is None:
                    continue
                if msg.error():
                    if msg.error().code() == KafkaError._PARTITION_EOF:
                        continue
                    else:
                        raise KafkaException(msg.error())
                else:
                    # Decode Kafka message
                    data = json.loads(msg.value().decode('utf-8'))
                    formatted_data = {
                        "stock_symbol": data.get("stock_symbol"),
                        "MA": data.get("MA"),
                        "EMA": data.get("EMA"),
                        "RSI": data.get("RSI"),
                        "Buy_signal": data.get("Buy_signal"),
                        "Sell_signal": data.get("Sell_signal")
                    }
                    print(formatted_data)
                    yield f"{json.dumps(formatted_data)}\n"
        except KeyboardInterrupt:
            consumer.close()

    return Response(generate(), content_type='application/json')

if __name__ == "__main__":
    app.run(debug=True, port=8000)
