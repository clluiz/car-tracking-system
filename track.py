import osmnx as ox
import networkx as nx
import numpy as np


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


class Track:

    def __init__(self, car, start_coord, end_coord):
        self.car = car
        self.start_coord = start_coord
        self.end_coord = end_coord
        self.route = []

    def build_route(self):
        graph = ox.graph_from_point(self.start_coord, dist=5000, network_type='drive')
        orig_node = ox.distance.nearest_nodes(
            graph, X=self.start_coord[1], Y=self.start_coord[0])
        dest_node = ox.distance.nearest_nodes(
            graph, X=self.end_coord[1], Y=self.end_coord[0])
        route = nx.shortest_path(graph, orig_node, dest_node, weight='length')
        route_coords = [(graph.nodes[node]['y'], graph.nodes[node]['x'])
                        for node in route]
        self.route = interpolate_points(
            route_coords, speed_kph=self.car.speed_kph, interval_sec=1)
