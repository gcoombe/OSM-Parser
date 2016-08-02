import xml.sax
import copy

"""
Convert xml map data returned from OSM and parse into a set of OSM nodes and ways.

Written with help from https://gist.github.com/aflaxman/287370

"""


class OSMGraph(object):
    """docstring for Graph"""
    def __init__(self, xml_map_data):
        ways = {}
        nodes = {}

        class OSMHandler(xml.sax.ContentHandler):
            @classmethod
            def setDocumentLocator(self, loc):
                pass

            @classmethod
            def startDocument(self):
                pass

            @classmethod
            def endDocument(self):
                pass

            @classmethod
            def startElement(self, name, attrs):
                if name == 'node':
                    self.currElem = OSMNode(attrs['id'], float(attrs['lon']), float(attrs['lat']))
                elif name == 'way':
                    self.currElem = OSMWay(attrs['id'])
                elif name == 'nd':
                    self.currElem.nds.append(attrs['ref'])

            @classmethod
            def endElement(self, name):
                if name == 'node':
                    nodes[self.currElem.id] = self.currElem
                elif name == 'way':
                    ways[self.currElem.id] = self.currElem

            @classmethod
            def characters(self, chars):
                pass

        xml.sax.parseString(xml_map_data, OSMHandler)

        self.ways = ways
        self.nodes = nodes

        degree_of_nodes = {}
        for way in ways.values():
            for node in way.nds:
                if(node not in degree_of_nodes):
                    degree_of_nodes[node] = 0
                degree_of_nodes[node] += 1

        # Ways now only have 2 nodes
        new_ways = {}
        for id, way in self.ways.items():
            split_ways = way.split(degree_of_nodes)
            for split_way in split_ways:
                new_ways[split_way.id] = split_way
        self.ways = new_ways

class OSMWay(object):
    def __init__(self, id, nds=[]):
        self.id = id
        self.nds = nds

    def __str__(self):
        return str(self.__dict__)

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self.__eq__(other)

    # Take a way (which can have >= 2 nodes) and create 1 or more edges from it
    def split(self, degree_of_nodes):
        def slice_edges(nodes, degree_of_nodes):
            for i in range(1, len(nodes)-1):
                if degree_of_nodes[nodes[i]] > 1:
                    left = nodes[:i+1]
                    right = nodes[i:]

                    rightsliced = slice_edges(right, degree_of_nodes)

                    return [left]+rightsliced
            return [nodes]

        slices = slice_edges(self.nds, degree_of_nodes)

        ret = []
        counter = 0
        for slice in slices:
            sliced_way = copy.copy(self)
            sliced_way.id += "-%d" % counter
            sliced_way.nds = slice
            ret.append(sliced_way)
            counter += 1

        return ret


class OSMNode(object):
    def __init__(self, id, lon, lat):
        self.id = id
        self.lon = lon
        self.lat = lat

    def __str__(self):
        return str(self.__dict__)

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self.__eq__(other)

    def __lt__(self, other):
        return self.id < other.id
