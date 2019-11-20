import time
import json
from iota import Iota, ProposedTransaction, Address, TryteString, Tag, Transaction
from apps.public_nodes import load_public_nodes
from apps.custom_nodes import load_custom_nodes
from apps.eval import sort_milestone_start_index, sort_duration_send_transfer
from apps.logging import update_log, read_log, append_log
from config.config_logging import LOG_DURATION_SEND, LOG_MILESTONE_START_INDEX, LOG_HISTORY_TXN

SEED = 'AMRWQP9BUMJALJHBXUCHOD9HFFD9LGTGEAWMJWWXSDVOF9PI9YGJAPBQLQUOMNYEQCZPGCTHGVNNAPGHA'

def milestone_start_index():
    while True:
        # Fetch all node from iota-nodes
        list_public_nodes = load_public_nodes()
        # Load custom node list
        list_custom_nodes = load_custom_nodes()

        list_public_nodes = list_public_nodes + list_custom_nodes

        # Sort by keys
        list_milestone_start_index = sort_milestone_start_index(list_public_nodes)

        # Log save
        update_log(list_milestone_start_index, LOG_MILESTONE_START_INDEX)

        # Sleeo
        time.sleep(43200)

    return 0

def duration_send_transfer():
    while True:
        # Fetch all node from iota-nodes
        list_public_nodes = load_public_nodes()
        # Load custom node list
        list_custom_nodes = load_custom_nodes()

        list_public_nodes = list_public_nodes + list_custom_nodes

        # Sort by keys
        list_duration_send = sort_duration_send_transfer(list_public_nodes)

        # Log save
        update_log(list_duration_send, LOG_DURATION_SEND)

    return 0

def add_txn_to_queue(request_data):
    request_command = json.loads(request_data)
    node_url = request_command['node_url']
    address = request_command['address']
    tag = request_command['tag']
    messages = request_command['messages']
    values = request_command['values']

    bundle_hash = ""
    prepared_transferes = []
    api = Iota(node_url, SEED)

    txn = \
        ProposedTransaction(
            address = Address(address),
            message = TryteString.from_string(messages),
            tag = Tag(tag),
            value = int(values),
    )
    prepared_transferes.append(txn)
    try:
        bundle_hash = api.send_transfer(
            depth = 7,
            transfers = prepared_transferes,
            min_weight_magnitude = 14
        )
    except Exception as e:
        print(e)
        return 0

    print(bundle_hash['bundle'].hash)
    append_log(bundle_hash['bundle'].hash, LOG_HISTORY_TXN)

    return 0
