# IOTA Full Node Provider

The IOTA Full Node Provider fetch full-nodes from [IOTA nodes](https://iota-nodes.net/) and
the customize list, and user can fetch a sorted node list from the REST API.

## Deploy
1. Add your custom IOTA Full-node in `input/input.txt`

   format:
   ```
   http://node1:14265
   http://node2:14265
   ```
2. python3 server.py

## Usage
1. Get sorted list
   
    - ```shell $curl <SERVER URL>/top_apis?api=<0:MilestoneStartIndex, 1:send_transfer duration>&counts=<response number> ```
    - Refer `example/request_nodes_by_milestoneindex.py` for detail. 

2. Send Transfer
    - Refer `example/send_transfer.py` for detail. 

## Demo site
- [http://node0.puyuma.org:5002](http://node0.puyuma.org:5002)

## IOTA Full-node reference
- [IOTA Nodes](https://iota-nodes.net/)
