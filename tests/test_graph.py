import unittest

from graph import Graph, Edge, calculate_distance_between_coordinates
from osm_graph import OSMGraph, OSMWay, OSMNode


class TestOSMGraph(unittest.TestCase):

    def test_calculate_node_distance(self):
        coordinate1 = (-123.121905, 49.278653)
        coordinate2 = (-123.111949, 49.285309)
        self.assertAlmostEqual(calculate_distance_between_coordinates(coordinate1, coordinate2), 1.034, 3)

    def test_calculates_simple_graph(self):
        nodes = [OSMNode(1, -123.121905, 49.278653), OSMNode(2, -123.111949, 49.285309)]
        o_graph = OSMGraph({3: OSMWay(3, nodes)}, {1: nodes[0], 2: nodes[1]})
        graph = Graph(o_graph)
        self.assertEqual(len(graph.edges), 1)
        self.assertEqual(graph.edges[0].head, 1)
        self.assertEqual(graph.edges[0].tail, 2)
        self.assertAlmostEqual(graph.edges[0].weight, 1.034, 3)

    def test_calculates_graph_with_many_node_ways(self):
        nodes = [OSMNode(1, -123.121905, 49.278653), OSMNode(2, -123.111949, 49.285309)]
        o_graph = OSMGraph({3: OSMWay(3, nodes)}, {1: nodes[0], 2: nodes[1]})
        graph = Graph(o_graph)
        self.assertEqual(len(graph.edges), 1)
        self.assertEqual(graph.edges[0].head, 1)
        self.assertEqual(graph.edges[0].tail, 2)
        self.assertAlmostEqual(graph.edges[0].weight, 1.034, 3)

    def test_to_list(self):
        nodes = [OSMNode(1, -123.121905, 49.278653), OSMNode(2, -123.111949, 49.285309)]
        o_graph = OSMGraph({3: OSMWay(3, nodes)}, {1: nodes[0], 2: nodes[1]})
        graph = Graph(o_graph)
        edges_list = graph.to_list()
        self.assertEqual(len(edges_list), 1)
        self.assertEqual(edges_list[0][0], 1)
        self.assertEqual(edges_list[0][1], 2)
        self.assertAlmostEqual(edges_list[0][2], 1.034, 3)