import threading
import json
from flask import Flask, render_template, request
from apps.jobs import milestone_start_index, duration_send_transfer, add_txn_to_queue
from config.config_logging import LOG_MILESTONE_START_INDEX, LOG_DURATION_SEND
from deps.send_transfer import send_transaction
from apps.logging import read_log

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

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

@app.route('/send_transfer' ,methods=['POST'])
def send_transfer():
    if request.method == 'POST':
        request_data = request.get_data()
        request_command = json.loads(request_data)
        node_url = request_command['node_url']
        address = request_command['address']
        tag = request_command['tag']
        messages = request_command['messages']
        values = request_command['values']
        hash_boundle = send_transaction(node_url, address, tag, messages, values)
    
        return hash_boundle

@app.route('/send_message' ,methods=['POST'])
def send_message():
    if request.method == 'POST':
        request_data = request.get_data()

        # Job for add the transaction to job queue
        thread_add_txn_to_queue = threading.Thread(target = add_txn_to_queue, args=(request_data,))
        thread_add_txn_to_queue.start()

        return "0"

# Job for fetch and sort milestone start index
thread_milestone_start_index = threading.Thread(target = milestone_start_index)
thread_milestone_start_index.start()

# Job send and sort duration of send_transfer
thread_duration_send_transfer= threading.Thread(target = duration_send_transfer)
thread_duration_send_transfer.start()
app.run(threaded=True, host = '0.0.0.0', port = 5002)

thread_milestone_start_index.join()
thread_duration_send_transfer.join()
