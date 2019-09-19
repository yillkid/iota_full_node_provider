import os
import time
import shutil
from deps.send import transfer
from deps.node_info import get_milestoneStartIndex

list_nodes = []
list_result = []

# Read input file
file_i = open("input.txt","r")
list_nodes = file_i.readlines() 
file_i.close()

print("Start to IOTA full-node checking ...")
for obj in list_nodes:
    try:
        new_dict = dict()

        # milestoneStartIndex
        milestone_start_index = get_milestoneStartIndex(obj.rstrip())
        if milestone_start_index == 0:
            continue

        # Send transfer
        start_send = time.time()
        txn_hash = transfer(obj.rstrip())
        if len(txn_hash) != 81:
            continue
        done_send = time.time()
        elapsed_send = int(done_send - start_send)

        new_dict['url'] = obj.rstrip()
        new_dict['send'] = str(elapsed_send)
        new_dict['start_index'] = milestone_start_index

        print("Node URL: " + str(new_dict['url']) +  \
                ", milestoneStartIndex: " + str(new_dict['start_index']) + \
                ", send duration: " + str(new_dict['send']))

        list_result.append(new_dict)
        
    except Exception as err:
        print("Skip node URL: " + str(obj.rstrip()) + " : " + err)


# Clear outpur folder
shutil.rmtree('output')
os.mkdir('output')

# Sort of send and save to csv
list_result = sorted(list_result, key=lambda k: int(k['send']), reverse=False)
f = open("output/duration_send.csv", "a")
for obj in list_result:
    f.write(obj['url'] + "," + str(obj['send']) + "\n")
f.close()

# Sort of milestoneStartIndex: and save to csv
list_result = sorted(list_result, key=lambda k: int(k['start_index']), reverse=False)
f = open("output/index_milestone_start.csv", "a")
for obj in list_result:
    f.write(obj['url'] + "," + str(obj['start_index']) + "\n")
f.close()
