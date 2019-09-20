from deps.node_info import get_milestoneStartIndex
from deps.send_transfer import transfer
import datetime

def sort_milestone_start_index(list_nodes):
    list_result = []

    for obj in list_nodes:
        try:
            new_dict = dict()

            # Get milestoneStartIndex
            milestone_start_index = get_milestoneStartIndex(obj.rstrip())
            if milestone_start_index == 0:
                continue

            new_dict['datetime'] = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M")
            new_dict['url'] = obj.rstrip()
            new_dict['start_index'] = milestone_start_index

            print("Append : " + str(new_dict))
            list_result.append(new_dict)

        except Exception as err:
            print("Skip node URL: " + str(obj.rstrip()) + " : " + str(err))

    list_result = sorted(list_result, key=lambda k: int(k['start_index']), reverse=False)
    
    return list_result

def sort_duration_send_transfer(list_nodes):
    list_result = []

    for obj in list_nodes:
        try:
            new_dict = dict()

            # Calculate duration of send transfer
            duration, hash_txn = transfer(obj.rstrip())

            if len(hash_txn) != 81:
                continue

            new_dict['datetime'] = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M")
            new_dict['url'] = obj.rstrip()
            new_dict['duration'] = str(duration)

            print("Append : " + str(new_dict))
            list_result.append(new_dict)

        except Exception as err:
            print("Skip node URL: " + str(obj.rstrip()) + " : " + str(err))

    list_result = sorted(list_result, key=lambda k: int(k['duration']), reverse=False)

    return list_result
