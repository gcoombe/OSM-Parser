from math import radians, cos, sin, asin, sqrt


class Graph(object):
    def __init__(self, osm_graph):
        self.edges = []
        # for way in osm_graph.ways:
        #     for i in range(0, len(nodes)-1):
        #         node_pairs = [(nodes[i], nodes[i + 1]) for i in len(nodes) - 1]
        #         way_length = reduce(lambda total, node_pair: total + _calculate_distance_between_coordinates(node_pair[0], node_pair[1]), node_pairs)
        #         self.edges.append(Edge(way.nds[0]))

    def _calculate_distance_between_coordinates(coordinate1, coordinate2):
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