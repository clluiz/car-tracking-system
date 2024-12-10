import time
from kafka import KafkaProducer, KafkaConsumer
import json

from car import Car
from track import Track

# Define coordinates (latitude, longitude)
start = (-21.264061178844006, -44.99667868968854)
end = (-21.237633375707656, -45.02327994551246)

car = Car(1, 50)
track = Track(car, start, end)
track.build_route()

producer = KafkaProducer(bootstrap_servers='localhost:9092',
                         value_serializer=lambda v: json.dumps(v).encode('utf-8'))

for coord in track.route:
    print(f"{coord[0]}, {coord[1]}")
    producer.send('rota', value={'latitude': coord[0], 'longitude': coord[1]})
    producer.flush()
    time.sleep(0.5)
