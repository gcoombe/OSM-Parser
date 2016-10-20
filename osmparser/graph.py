from math import radians, cos, sin, asin, sqrt
from functools import reduce


class Graph(object):
    def __init__(self, osm_graph):
        self.edges = []
        self.nodes = {}
        for id, way in osm_graph.ways.items():
            for i in range(0, len(way.nds)-1):
                node_pairs = [(way.nds[i], way.nds[i + 1]) for i in range(0, len(way.nds) - 1)]
                way_length = reduce(
                    lambda total, node_pair: total + calculate_distance_between_coordinates(node_pair[0].get_coordinate(), node_pair[1].get_coordinate()),
                    node_pairs,
                    0
                )
                self.edges.append(Edge(way.nds[0].id, way.nds[-1].id, way_length))
        for id, osm_node in osm_graph.nodes.items():
            self.nodes[id] = Node(osm_node.lat, osm_node.lon)

    def edge_list(self):
        result = []
        for edge in self.edges:
            result.append((edge.head, edge.tail, edge.weight))
        return result

    def node_list(self):
        result = []
        for id, node in self.nodes.items():
            result.append((node.lat, node.lon))
        return result

def calculate_distance_between_coordinates(coordinate1, coordinate2):
        """
        Calculate the great circle distance between two points
        on the earth (specified in decimal degrees) using the haversince formula.
        :param coordinate1: tuple in form (lon, lat)
        :param coordinate2: tuple in form (lon, lat)
        :return: distance between points in km
        """

        # convert decimal degrees to radians
        lon1, lat1, lon2, lat2 = map(radians, [coordinate1[0], coordinate1[1], coordinate2[0], coordinate2[1]])

        # haversine formula
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * asin(sqrt(a))
        r = 6371 # Radius of earth in kilometers. Use 3956 for miles
        return c * r

class Edge(object):
    def __init__(self, head, tail, weight):
        self.head = head  # Start node
        self.tail = tail  # End node
        self.weight = weight  # Cost

class Node(object):
    def __init__(self, lat, lon):
        self.lat = lat
        self.lon = lon