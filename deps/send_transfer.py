import time
from iota import Iota, ProposedTransaction, Address, TryteString, Tag, Transaction
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
