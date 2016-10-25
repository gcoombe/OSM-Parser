import xml.sax
import copy

"""
Convert xml map data returned from OSM and parse into a set of OSM nodes and ways.

Written with help from https://gist.github.com/aflaxman/287370

"""


class OSMGraph(object):
    def __init__(self, ways=None, nodes=None):
        if (ways is None):
            ways = {}
        if (nodes is None):
            nodes = {}
        self.ways = ways
        self.nodes = nodes

    @classmethod
    def from_xml_data(cls, xml_map_data):
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
                    self.currElem = OSMNode(attrs['id'], float(attrs['lat']), float(attrs['lon']))
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

        return cls._split_ways(ways.values(), nodes)

    @classmethod
    def from_overpy_result(cls, overpy_result):
        ways =  []
        nodes = {}
        for node in overpy_result.get_nodes():
            nodes[node.id] = OSMNode(node.id, node.lat, node.lon)
        for way in overpy_result.get_ways():
            ways.append(OSMWay(way.id, list(map(lambda node: node.id, way.get_nodes()))))
        return cls._split_ways(ways, nodes);


    @classmethod
    def _split_ways(cls, ways, nodes):
        degree_of_nodes = {}
        for way in ways:
            for node in way.nds:
                if(node not in degree_of_nodes):
                    degree_of_nodes[node] = 0
                degree_of_nodes[node] += 1

        # Ways now only have 2 nodes
        new_ways = {}
        for way in ways:
            split_ways = way.split(degree_of_nodes)
            for split_way in split_ways:
                new_ways[split_way.id] = split_way

        return cls(new_ways, nodes)

    # Populate node objects on ways
    def get_ways_with_nodes(self):
        ways_with_nodes = [];
        for id, way in self.ways.items():
            new_way = OSMWay(way.id, way.nds)
            new_way.nodes = [];
            for node_id in new_way.nds:
                new_way.nodes.append(self.nodes[node_id])
            ways_with_nodes.append(new_way)
        return ways_with_nodes



class OSMWay(object):
    def __init__(self, id, nds=None):
        self.id = id
        if (nds is None):
            self.nds = []
        else:
            self.nds = nds

    def __repr__(self):
        return "OSMWay({})".format(self.__dict__)

    def __str__(self):
        return str(self.__dict__)

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self.__eq__(other)

    def __lt__(self, other):
        return self.id < other.id

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
    def __init__(self, id, lat, lon):
        self.id = id
        self.lon = lon
        self.lat = lat

    def __repr__(self):
        return "OSMNode({})".format(self.__dict__)

    def __str__(self):
        return str(self.__dict__)

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self.__eq__(other)

    def __lt__(self, other):
        return self.id < other.id

    def get_coordinate(self):
        return (self.lon, self.lat)
