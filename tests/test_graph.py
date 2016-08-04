import unittest

from graph import Graph


class TestOSMGraph(unittest.TestCase):

    def test_calculate_node_distance(self):
        coordinate1 = (-123.121905, 49.278653)
        coordinate2 = (-123.111949, 49.285309)
        self.assertAlmostEqual(Graph._calculate_distance_between_coordinates(coordinate1, coordinate2), 1.034, 3)