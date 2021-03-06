"""
Functions to fetch data from OSM overpass_api

"""

import requests
import os
import json
from .graph import Graph
from .osm_graph import OSMGraph
import overpy

from requests.auth import HTTPBasicAuth

OSM_BASE_URL = 'http://api06.dev.openstreetmap.org/'

OVERPASS_QUERY_TEMPLATE = """way[highway][highway!=service][!building][!junction]({0})->.w;
    node({0})->.n;
    .w>->.nw;
    (
      .w;
      node.nw.n;
    );
    out;"""

overpass_api = overpy.Overpass()

"""
Fetch a graph representation of the map specified by the bounded box.

provider can be "overpass" or "osm".  overpass is suggested its api is designed for querying an superior than the base osm api.

"""
def fetch_bounded_box_graph(left, bottom, right, top, provider="overpass"):
    if provider == "osm":
        return _fetch_bounded_box_graph_from_osm(left, bottom, right, top)
    return _fetch_graph_from_overpass(left, bottom, right, top);

def _fetch_bounded_box_graph_from_osm(left, bottom, right, top):
    bounding_box = ','.join(map(str, (left, bottom, right, top)))
    fetch_reponse = _request("GET", OSM_BASE_URL + '/api/0.6/map', params={'bbox': bounding_box})
    osm_graph = OSMGraph.from_xml_data(fetch_reponse.text)
    return Graph.from_osm_graph(osm_graph)

def _request(method, url, params=None, data=None, timeout=60):
    """
    :param method: String, 'get', 'post', etc.
    :param url: String, url which will be hit
    :param params: Dict, parameters to be passed with the request
    :param data: Dictionary, bytes, or file-like object to send in the body of the Request
    :return: response object
    """

    auth = HTTPBasicAuth(os.getenv('OSM_USER_NAME', ''), os.getenv('OSM_PASSWORD', ''))

    try:
        if data:
            data = json.dumps(data)
            return requests.request(method, url, auth=auth, data=data, timeout=timeout)
        else:
            return requests.request(method, url, auth=auth, params=params, timeout=timeout)
    except requests.RequestException as e:
        print('Failure to fetch {}, {}'.format(url, e))
        raise e

def _fetch_graph_from_overpass(left, bottom, right, top):
    fetch_reponse = _fetch_from_overpass(left, bottom, right, top)
    osm_graph = OSMGraph.from_overpy_result(fetch_reponse)
    return Graph.from_osm_graph(osm_graph)

def _fetch_from_overpass(left, bottom, right, top):
    bounding_box = ','.join(map(str, (bottom, left, top, right)))
    print(OVERPASS_QUERY_TEMPLATE.format(bounding_box))
    return overpass_api.query(OVERPASS_QUERY_TEMPLATE.format(bounding_box))
