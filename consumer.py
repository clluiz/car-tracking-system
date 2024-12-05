from kafka import KafkaConsumer
import json

consumer = KafkaConsumer(
    'rota',
    bootstrap_servers='localhost:9092',
    group_id="teste-2",
    auto_offset_reset='earliest',
    value_deserializer=lambda v: json.loads(v.decode('utf-8'))
)
for message in consumer:
    print(message.value)