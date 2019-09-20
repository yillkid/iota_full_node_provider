from apps.public_nodes import load_public_nodes
from apps.custom_nodes import load_custom_nodes
from apps.eval import sort_milestone_start_index, sort_duration_send_transfer
from apps.logging import update_log, read_log
from config.config_logging import LOG_DURATION_SEND, LOG_MILESTONE_START_INDEX

def milestone_start_index():
    # Fetch all node from iota-nodes
    list_public_nodes = load_public_nodes()
    # Load custom node list
    list_custom_nodes = load_custom_nodes()

    list_public_nodes = list_public_nodes + list_custom_nodes

    # Sort by keys
    list_milestone_start_index = sort_milestone_start_index(list_public_nodes)

    # Log save
    update_log(list_milestone_start_index, LOG_MILESTONE_START_INDEX)

    return 0

def duration_send_transfer():
    # Fetch all node from iota-nodes
    list_public_nodes = load_public_nodes()
    # Load custom node list
    list_custom_nodes = load_custom_nodes()

    list_public_nodes = list_public_nodes + list_custom_nodes

    # Sort by keys
    list_duration_send = sort_duration_send_transfer(list_public_nodes)

    # Log save
    update_log(list_duration_send, LOG_DURATION_SEND)

    # Ready to publish
    return 0

