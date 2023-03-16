import time
from flask import Flask, render_template, jsonify
import random
import threading
from datetime import datetime

app = Flask(__name__)

random_value = 0
data_points = []


def generate_random():
    global random_value
    while True:
        random_value = random.randint(0, 100)
        data_points.append(random_value)
        time.sleep(1)


@app.route('/')
def hello_world():  # put application's code here
    return render_template('charts/index.html')


@app.route('/get-random-data-value')
def get_random_data_value():
    return jsonify({'value': random_value})


@app.route('/data')
def get_data():
    # get the time and value data
    now = datetime.now()
    formatted_time = now.strftime("%I:%M:%S %p")

    MAX_DATA_POINTS = 30

    if (x := len(data_points)) > MAX_DATA_POINTS:
        extras = x - MAX_DATA_POINTS
        for i in range(extras):
            try:
                data_points.pop(i)
            except:
                pass

    # create a dictionary with the time and value data
    data = {'time': formatted_time, 'value': data_points}

    # return the data as JSON
    return jsonify(data)


threading.Thread(target=generate_random).start()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8888)
