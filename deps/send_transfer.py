import time
from iota import Iota, ProposedTransaction, Address, TryteString, Tag, Transaction, ProposedBundle, Hash
from iota.trits import trits_from_int
import time
import requests
import json
from config.config_iota import SEED, DEPTH, MIN_WEIGHT_MAGNITUDE

def transfer(node):
    start_send = time.time()

    address = "ILXW9VMJQVFQVKVE9GUZSODEMIMGOJIJNFAX9PPJHYQPUHZLTWCJZKZKCZYKKJJRAKFCCNJN9EWOW9N9YDGZDDQDDC"
    tag = "TAG"
    message = "MSG"
    value = 0
    node_url = node

    recipient_address = address
    sender_message = message
    sender_tag = tag

    bundle_hash = ""
    prepared_transferes = []
    api = Iota(node_url, SEED)

    sender_tag = sender_tag
    transfer_value = int(value)

    txn = \
        ProposedTransaction(
            address = Address(
                recipient_address
        ),

        message = TryteString.from_string(sender_message),
        tag = Tag(sender_tag),
        value = transfer_value,
    )

    prepared_transferes.append(txn)
    try:
        bundle_hash = api.send_transfer(
            depth=DEPTH,
            transfers=prepared_transferes,
            min_weight_magnitude=MIN_WEIGHT_MAGNITUDE
        )
    except Exception as e:
        print("Error" + str(e))
        return "0, 0"

    done_send = time.time()
    elapsed_send = int(done_send - start_send)

    return elapsed_send, bundle_hash['bundle'].hash

def gtta(node_url):
    command = {
        "command": "getTransactionsToApprove",
        "depth": DEPTH
    }

    url = node_url
    data = command
    headers = {'Content-type': 'application/json', 'X-IOTA-API-Version': '1'}
    r = requests.post(url, data=str(data), headers=headers)

    if r.status_code == 200:
        obj_nonce = json.loads(r.text)
        return obj_nonce['trunkTransaction'], obj_nonce['branchTransaction']
    else:
        return Hash(''), Hash('')

def attach_to_tangle(node_url, trunk_hash, branch_hash, tx_tryte):
    command = {
        "command": "attachToTangle",
        "trunkTransaction": str(trunk_hash),
        "branchTransaction": str(branch_hash),
        "minWeightMagnitude": MIN_WEIGHT_MAGNITUDE,
        "trytes": [str(tx_tryte)]
    }

    url = node_url
    data = command
    headers = {'Content-type': 'application/json', 'X-IOTA-API-Version': '1'}
    r = requests.post(url, data=str(data), headers=headers)

    obj_nonce = json.loads(r.text)

    return obj_nonce["trytes"]

def insert_to_trytes(index_start, index_end, str_insert, trytes):
    trytes = trytes[:index_start] + str_insert + trytes[index_end:]

    return trytes

# Save to queue and broadcast
def send_transaction(node_url, address, tag, messages, values):
    propose_bundle = ProposedBundle()

    # Setting output transaction ...
    txn_output = ProposedTransaction(
        address = Address(address),
        value = values,
        tag = Tag(tag),
        message = TryteString.from_string(messages)
    )

    propose_bundle.add_transaction(txn_output)
    propose_bundle.finalize()
    trytes = propose_bundle.as_tryte_strings()

    api = Iota(node_url)

    # Tips
    trunk_hash, branch_hash = gtta(node_url)

    for tx_tryte in trytes:
        # Attachment timestamp insert
        timestamp = TryteString.from_trits(
            trits_from_int(int(time.time() * 1000), pad=27))
        tx_tryte = insert_to_trytes(2619, 2628, str(timestamp), tx_tryte)

        # timestamp_lower_bound = MIN_VALUE
        # timestamp_upper_bound = MAX_VALUE
        tx_tryte = insert_to_trytes(2637, 2646, str("MMMMMMMMM"), tx_tryte)

        # Tips insert - trunk
        tx_tryte = insert_to_trytes(2430, 2511, str(trunk_hash), tx_tryte)
        # Tips insert - branch
        tx_tryte = insert_to_trytes(2511, 2592, str(branch_hash), tx_tryte)

        # Do PoW for this transaction
        tx_tryte = attach_to_tangle(node_url, trunk_hash, branch_hash, tx_tryte)

        # Prepare to store and broadcast ...
        try:
            api.broadcast_and_store(tx_tryte)
        except Exception as e:
            return str("Error: %s" % (str(e)))

        return str(propose_bundle.hash)
