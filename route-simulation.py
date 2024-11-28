import osmnx as ox
import networkx as nx
import numpy as np
import time
from kafka import KafkaProducer, KafkaConsumer
import json


def interpolate_points(points, speed_kph, interval_sec):
    interpolated = []
    speed_mps = speed_kph * 1000 / 3600  # Convert speed to meters per second
    for i in range(len(points) - 1):
        start = np.array(points[i])
        end = np.array(points[i + 1])
        dist = np.linalg.norm(end - start)  # Distance between points
        steps = int(dist / (speed_mps * interval_sec)) + 1
        for step in range(steps):
            interpolated.append(list(start + step * (end - start) / steps))
    interpolated.append(points[-1])  # Include the final point
    return interpolated


# Define coordinates (latitude, longitude)
start = (-21.264061178844006, -44.99667868968854)
end = (-21.237633375707656, -45.02327994551246)

# Download road network for the area
graph = ox.graph_from_point(start, dist=5000, network_type='drive')

# Find the nearest nodes in the graph
orig_node = ox.distance.nearest_nodes(graph, X=start[1], Y=start[0])
dest_node = ox.distance.nearest_nodes(graph, X=end[1], Y=end[0])

# Calculate the shortest path
route = nx.shortest_path(graph, orig_node, dest_node, weight='length')

route_coords = [(graph.nodes[node]['y'], graph.nodes[node]['x'])
                for node in route]

interpolated_route = interpolate_points(
    route_coords, speed_kph=50, interval_sec=1)

config = {
  "acks": 0
}

producer = KafkaProducer(bootstrap_servers='localhost:9092',
                         #acks=0,
                         #linger_ms=0,
                         value_serializer=lambda v: json.dumps(v).encode('utf-8'))

for coord in interpolated_route:
    print(f"{coord[0]}, {coord[1]}")
    producer.send('rota', value={'latitude': coord[0], 'longitude': coord[1]})
    time.sleep(0.5)
