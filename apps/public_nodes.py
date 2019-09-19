import json
import requests
from config.config_public_node import IOTA_NODES_API

def load_public_nodes():
    list_nodes = []
    response = ""

    try:
        response = requests.get(IOTA_NODES_API)
    except:
        return []

    if response.status_code == requests.codes.ok:
        list_response = json.loads(response.text)

        for obj in list_response:
            host_url = ""

            if obj["isSSL"]:
                host_url = "https://"
            else:
                host_url = "http://"

            list_nodes.append(host_url + obj["hostname"] + ":" + str(obj["port"]))

        return list_nodes

    return []
