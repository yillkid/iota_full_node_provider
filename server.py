import threading
from flask import Flask, render_template, request
from apps.jobs import milestone_start_index, duration_send_transfer
from config.config_logging import LOG_MILESTONE_START_INDEX, LOG_DURATION_SEND

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

# Job for fetch and sort milestone start index
thread_milestone_start_index = threading.Thread(target = milestone_start_index)
thread_milestone_start_index.start()

# Job send and sort duration of send_transfer
thread_duration_send_transfer= threading.Thread(target = duration_send_transfer)
thread_duration_send_transfer.start()
app.run(threaded=True, host = '0.0.0.0', port = 5003)

thread_milestone_start_index.join()
thread_duration_send_transfer.join()
