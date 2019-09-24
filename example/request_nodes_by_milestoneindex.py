import requests
import json

r = requests.get("http://localhost:5002/top_apis?api=0&counts=3")
list_nodes = json.loads(r.text)

for obj in list_nodes:
    print(obj)
