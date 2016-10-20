import unittest

from osmparser.osm_graph import OSMGraph, OSMWay, OSMNode


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

        graph = OSMGraph.from_xml_data(xml_string)
        expected_ways = [OSMWay("199838-0", ["5900058", "5900341"])]
        expected_nodes = [OSMNode("5900058", 49.2759, -123.1242), OSMNode("5900341", 49.2766, -123.1231)]

        self.assertEqual(sorted(list(graph.ways.values())), sorted(expected_ways))
        self.assertEqual(sorted(list(graph.nodes.values())), sorted(expected_nodes))

    def test_ways_with_multi_nodes_arent_split_if_no_interestctions(self):
        xml_string = """<?xml version="1.0" encoding="UTF-8"?>
            <osm version="0.6" generator="OpenStreetMap server" copyright="OpenStreetMap and contributors" attribution="http://www.openstreetmap.org/copyright" license="http://opendatacommons.org/licenses/odbl/1-0/">
              <bounds minlat="49.2756" minlon="-123.12518" maxlat="49.277574" maxlon="-123.122176"/>
              <node id="5902860" changeset="8212" timestamp="2011-02-03T00:45:17Z" version="1" visible="true" user="rus" uid="96" lat="49.2759" lon="-123.1242"/>
              <node id="5899705" changeset="8212" timestamp="2011-02-03T00:45:26Z" version="1" visible="true" user="rus" uid="96" lat="49.2766" lon="-123.1231"/>
              <node id="5902472" changeset="8212" timestamp="2011-02-03T00:46:00Z" version="1" visible="true" user="rus" uid="96" lat="49.2748" lon="-123.1258"/>
                <way id="201058" changeset="8212" timestamp="2011-02-03T00:48:37Z" version="1" visible="true" user="rus" uid="96">
                <nd ref="5902860"/>
                <nd ref="5899705"/>
                <nd ref="5902472"/>
              </way>
            </osm>
            """

        graph = OSMGraph.from_xml_data(xml_string)
        expected_ways = [OSMWay("201058-0", ["5902860", "5899705", "5902472"])]
        expected_nodes = [OSMNode("5902860", 49.2759, -123.1242), OSMNode("5899705", 49.2766, -123.1231), OSMNode("5902472", 49.2748, -123.1258)]

        self.assertEqual(sorted(list(graph.ways.values())), sorted(expected_ways))
        self.assertEqual(sorted(list(graph.nodes.values())), sorted(expected_nodes))

    def test_split_way_if_multi_node_through_intersection(self):
        xml_string = """<?xml version="1.0" encoding="UTF-8"?>
            <osm version="0.6" generator="OpenStreetMap server" copyright="OpenStreetMap and contributors" attribution="http://www.openstreetmap.org/copyright" license="http://opendatacommons.org/licenses/odbl/1-0/">
              <bounds minlat="49.2756" minlon="-123.12518" maxlat="49.277574" maxlon="-123.122176"/>
              <node id="5902860" changeset="8212" timestamp="2011-02-03T00:45:17Z" version="1" visible="true" user="rus" uid="96" lat="49.2759" lon="-123.1242"/>
              <node id="5899705" changeset="8212" timestamp="2011-02-03T00:45:26Z" version="1" visible="true" user="rus" uid="96" lat="49.2766" lon="-123.1231"/>
              <node id="5902472" changeset="8212" timestamp="2011-02-03T00:46:00Z" version="1" visible="true" user="rus" uid="96" lat="49.2748" lon="-123.1258"/>
              <node id="553185065" visible="true" version="4" changeset="22033242" timestamp="2014-04-29T22:53:06Z" uid="1355239" lat="49.2775075" lon="-123.1267388"/>
                <way id="201058" changeset="8212" timestamp="2011-02-03T00:48:37Z" version="1" visible="true" user="rus" uid="96">
                    <nd ref="5902860"/>
                    <nd ref="5899705"/>
                    <nd ref="5902472"/>
                </way>
                <way id="301878980" visible="true" version="2" changeset="33257926" timestamp="2015-08-11T05:08:00Z" user="fmarier" uid="24555">
                    <nd ref="5899705"/>
                    <nd ref="553185065"/>
                </way>
            </osm>
            """

        graph = OSMGraph.from_xml_data(xml_string)
        expected_ways = [OSMWay("201058-0", ["5902860", "5899705"]), OSMWay("201058-1", ["5899705", "5902472"]), OSMWay("301878980-0", ["5899705", "553185065"])]
        expected_nodes = [OSMNode("5902860", 49.2759, -123.1242), OSMNode("5899705", 49.2766, -123.1231), OSMNode("5902472", 49.2748, -123.1258), OSMNode("553185065", 49.2775075, -123.1267388)]

        self.assertEqual(sorted(list(graph.ways.values())), sorted(expected_ways))
        self.assertEqual(sorted(list(graph.nodes.values())), sorted(expected_nodes))

