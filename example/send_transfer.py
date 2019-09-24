import requests 
import json
import ast

r = requests.get("http://node0.puyuma.org:5002/top_apis?api=1&counts=1")
obj = ast.literal_eval(json.loads(r.text)[0])

data = {'node_url':obj['url'],'address':'ILXW9VMJQVFQVKVE9GUZSODEMIMGOJIJNFAX9PPJHYQPUHZLTWCJZKZKCZYKKJJRAKFCCNJN9EWOW9N9YDGZDDQDDC','tag':'TESTKIIDJHEG','messages':'good guy','values':0}
headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
r = requests.post("http://node0.puyuma.org:5002/send_transfer", data=json.dumps(data), headers=headers)

print(r.text)
