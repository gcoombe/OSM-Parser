import unittest

from osmparser.graph import Graph, Edge, Node, calculate_distance_between_coordinates
from osmparser.osm_graph import OSMGraph, OSMWay, OSMNode


class TestOSMGraph(unittest.TestCase):

    def test_calculate_node_distance(self):
        coordinate1 = (-123.121905, 49.278653)
        coordinate2 = (-123.111949, 49.285309)
        self.assertAlmostEqual(calculate_distance_between_coordinates(coordinate1, coordinate2), 1.034, 3)

    def test_calculates_simple_graph(self):
        nodes = [OSMNode(1, 49.278653, -123.121905), OSMNode(2, 49.285309, -123.111949)]
        o_graph = OSMGraph({3: OSMWay(3, [nodes[0].id, nodes[1].id])}, {1: nodes[0], 2: nodes[1]})
        graph = Graph.from_osm_graph(o_graph)
        self.assertEqual(len(graph.edges), 1)
        self.assertEqual(graph.edges[0].head, 1)
        self.assertEqual(graph.edges[0].tail, 2)
        self.assertAlmostEqual(graph.edges[0].weight, 1.034, 3)

    def test_calculates_graph_with_many_node_ways(self):
        nodes = [OSMNode(1, 49.278653, -123.121905), OSMNode(2, 49.285309, -123.111949)]
        o_graph = OSMGraph({3: OSMWay(3, [nodes[0].id, nodes[1].id])}, {1: nodes[0], 2: nodes[1]})
        graph = Graph.from_osm_graph(o_graph)
        self.assertEqual(len(graph.edges), 1)
        self.assertEqual(graph.edges[0].head, 1)
        self.assertEqual(graph.edges[0].tail, 2)
        self.assertAlmostEqual(graph.edges[0].weight, 1.034, 3)

    def test_edge_list(self):
        nodes = [OSMNode(1, 49.278653, -123.121905), OSMNode(2, 49.285309, -123.111949)]
        o_graph = OSMGraph({3: OSMWay(3, [nodes[0].id, nodes[1].id])}, {1: nodes[0], 2: nodes[1]})
        graph = Graph.from_osm_graph(o_graph)
        edges_list = graph.edge_list()
        self.assertEqual(len(edges_list), 1)
        self.assertEqual(edges_list[0][0], 1)
        self.assertEqual(edges_list[0][1], 2)
        self.assertAlmostEqual(edges_list[0][2], 1.034, 3)

    def test_node_list(self):
        nodes = [OSMNode(1, 49.278653, -123.121905), OSMNode(2, 49.285309, -123.111949)]
        o_graph = OSMGraph({3: OSMWay(3, [nodes[0].id, nodes[1].id])}, {1: nodes[0], 2: nodes[1]})
        graph = Graph.from_osm_graph(o_graph)
        nodes_list = graph.node_list()
        self.assertEqual(len(nodes_list), 2)
        self.assertEqual(nodes_list[0][1], -123.121905)
        self.assertEqual(nodes_list[0][0], 49.278653)
        self.assertEqual(nodes_list[1][1], -123.111949)
        self.assertEqual(nodes_list[1][0], 49.285309)

    def test_edge_contains_lat_lng(self):
        nodes = [Node(1, 49.278653, -123.121905), Node(2, 49.285309, -123.111949)]
        edge =  Edge(1, nodes, 1)
        self.assertTrue(edge.contains_lat_long(49.278653, -123.121905))

    def test_edge_not_contains_lat_lng(self):
        nodes = [Node(1, 49.278653, -123.121905), Node(2, 49.285309, -123.111949)]
        edge =  Edge(1, nodes, 1)
        self.assertFalse(edge.contains_lat_long(60, -121))

    def test_edge_has_segment(self):
        nodes = [Node(1, 49.278653, -123.121905), Node(2, 49.285309, -123.111949)]
        edge =  Edge(1, nodes, 1)
        self.assertTrue(edge.contains_segment({"lat": nodes[0].lat, "lon": nodes[0].lon}, {"lat": nodes[1].lat, "lon": nodes[1].lon}))

    def test_edge_has_segment_undirected(self):
        nodes = [Node(1, 49.278653, -123.121905), Node(2, 49.285309, -123.111949)]
        edge =  Edge(1, nodes, 1)
        self.assertTrue(edge.contains_segment({"lat": nodes[1].lat, "lon": nodes[1].lon}, {"lat": nodes[0].lat, "lon": nodes[0].lon}))

    def test_edge_doesnt_have_segment(self):
        nodes = [Node(1, 49.278653, -123.121905), Node(2, 49.285309, -123.111949)]
        edge =  Edge(1, nodes, 1)
        self.assertFalse(edge.contains_segment({"lat": 50, "lon": -100}, {"lat": nodes[1].lat, "lon": nodes[1].lon}))

    def test_edge_coords_not_adjacent(self):
        nodes = [Node(1, 49.278653, -123.121905), Node(2, 49.285309, -123.111949), Node(3, 50.1, -124.1)]
        edge =  Edge(1, nodes, 1)
        self.assertFalse(edge.contains_segment({"lat": nodes[0].lat, "lon": nodes[0].lon}, {"lat": nodes[2].lat, "lon": nodes[2].lon}))

    def test_edge_coords_head_tail(self):
        nodes = [Node(1, 49.278653, -123.121905), Node(2, 49.285309, -123.111949), Node(3, 50.1, -124.1)]
        edge =  Edge(1, nodes, 1)
        self.assertTrue(edge.contains_segment({"lat": nodes[0].lat, "lon": nodes[0].lon}, {"lat": nodes[2].lat, "lon": nodes[2].lon}, head_to_tail=True))