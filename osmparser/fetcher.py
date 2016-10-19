"""
Functions to fetch data from OSM api

"""

import requests
import os
import json
from .graph import Graph
from .osm_graph import OSMGraph

from requests.auth import HTTPBasicAuth

OSM_BASE_URL = 'http://api06.dev.openstreetmap.org/'


def fetch_bounded_box_map(left, bottom, right, top):
    bounding_box = ','.join(map(str, (left, bottom, right, top)))
    return _request("GET", OSM_BASE_URL + '/api/0.6/map', params={'bbox': bounding_box})

def fetch_bounded_box_graph(left, bottom, right, top):
    osm_graph = osm_graph.from_xml_data(fetch_bounded_box_map(lefy, bottom, right, top))
    return Graph(osm_graph)

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
