from flask import Flask, render_template, request
from apps.public_nodes import load_public_nodes
from apps.custom_nodes import load_custom_nodes
from apps.eval import sort_milestone_start_index, sort_duration_send_transfer
from apps.logging import update_log, read_log
from config.config_logging import LOG_DURATION_SEND, LOG_MILESTONE_START_INDEX

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/milestone_start_index')
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

    # Ready to publish
    return render_template('milestone_start_index.html', list_milestone_start_index = list_milestone_start_index)

@app.route('/duration_send_transfer')
def duration_send_transfer():
    # Fetch all node from iota-nodes
    list_public_nodes = load_public_nodes()
    # Load custom node list
    list_custom_nodes = load_custom_nodes()

    list_public_nodes = list_public_nodes + list_custom_nodes

    # Sort by keys
    list_duration_send = sort_duration_send_transfer(list_public_nodes)

    # Log save
    print("Hello start to log" + str(list_duration_send))
    update_log(list_duration_send, LOG_DURATION_SEND)

    # Ready to publish
    return render_template('duration_send.html', list_duration_send = list_duration_send)


@app.route('/top_apis', methods=['GET'])
def top_apis():
    api = request.args.get('api', 0)
    counts = request.args.get('counts', 0)
    log_path = ""

    if int(api) == 0:
        log_path = LOG_MILESTONE_START_INDEX
    else:
        log_path = LOG_DURATION_SEND

    list_logs = read_log(log_path, int(counts))

    return str(list_logs)

app.run(threaded=True, host = '0.0.0.0', port = 5002)
