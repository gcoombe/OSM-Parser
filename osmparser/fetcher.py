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

OSM_BASE_URL = 'http://overpass_api06.dev.openstreetmap.org/'

OVERPASS_QUERY_TEMPLATE = """way[highway!=service][!building]({0})->.w;
    node({0})->.n;
    .w>->.nw;
    (
      .w;
      node.nw.n;
    );
    out meta;"""

overpass_api = overpy.Overpass()

def fetch_bounded_box_map(left, bottom, right, top):
    bounding_box = ','.join(map(str, (left, bottom, right, top)))
    return _request("GET", OSM_BASE_URL + '/overpass_api/0.6/map', params={'bbox': bounding_box})

def fetch_bounded_box_graph(left, bottom, right, top):
    fetch_reponse = fetch_bounded_box_map(left, bottom, right, top)
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

def _build_overpass_query(left, bottom, right, top):
    bounding_box = ','.join(map(str, (bottom, left, top, right)))
    return OVERPASS_QUERY_TEMPLATE.format(bounding_box)

def fetch_from_overpass(left, bottom, right, top):
    return overpass_api.query(_build_overpass_query(left, bottom, right, top))

def fetch_osm_graph_from_overpass(left, bottom, right, top):
    fetch_reponse = fetch_from_overpass(left, bottom, right, top)
    osm_graph = OSMGraph.from_overpy_result(fetch_reponse)
    return Graph.from_osm_graph(osm_graph)
