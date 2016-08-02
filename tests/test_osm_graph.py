import unittest

from osm_graph import OSMGraph, OSMWay, OSMNode


class TestOSMGraph(unittest.TestCase):

    def test_parse_simple_map(self):
        xml_string = """<?xml version="1.0" encoding="UTF-8"?>
            <osm version="0.6" generator="OpenStreetMap server" copyright="OpenStreetMap and contributors" attribution="http://www.openstreetmap.org/copyright" license="http://opendatacommons.org/licenses/odbl/1-0/">
              <bounds minlat="49.2756" minlon="-123.12518" maxlat="49.277574" maxlon="-123.122176"/>
              <node id="5900058" changeset="8212" timestamp="2011-02-03T00:45:17Z" version="1" visible="true" user="rus" uid="96" lat="49.2759" lon="-123.1242"/>
              <node id="5900341" changeset="8212" timestamp="2011-02-03T00:45:26Z" version="1" visible="true" user="rus" uid="96" lat="49.2766" lon="-123.1231"/>
              <way id="199838">
                <nd ref="5900058"/>
                <nd ref="5900341"/>
              </way>
            </osm>
            """

        graph = OSMGraph(xml_string)
        expected_ways = [OSMWay("199838-0", ["5900058", "5900341"])]
        expected_nodes = [OSMNode("5900058", -123.1242, 49.2759,), OSMNode("5900341", -123.1231, 49.2766)]

        self.assertEqual(sorted(list(graph.ways.values())), sorted(expected_ways))
        self.assertEqual(sorted(list(graph.nodes.values())), sorted(expected_nodes))

