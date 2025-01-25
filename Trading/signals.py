from confluent_kafka import Consumer, KafkaException, KafkaError
import json

conf = {
    'bootstrap.servers': 'localhost:9092', 
    'group.id': 'signal-group',
    'auto.offset.reset': 'earliest'
}

consumer = Consumer(conf)

consumer.subscribe(['signals-topic'])

try:
    while True:
        msg = consumer.poll(1.0) 

        if msg is None:
            continue
        if msg.error():
            if msg.error().code() == KafkaError._PARTITION_EOF:
                print(f"End of partition {msg.partition} reached {msg.offset}")
            else:
                raise KafkaException(msg.error())
        else:
            # get data from kafka
            data = json.loads(msg.value().decode('utf-8'))

            # print(data)

            stock_symbol = data['stock_symbol']
            ma = data['MA']
            ema = data['EMA']
            rsi = data['RSI']
            buy_signal = data['buy_signal']
            sell_signal = data['sell_signal']

            print(f"Stock: {stock_symbol}, MA: {ma}, EMA: {ema}, RSI: {rsi}, Buy Signal: {buy_signal}, Sell Signal: {sell_signal}")

except KeyboardInterrupt:
    pass
finally:
    consumer.close()
