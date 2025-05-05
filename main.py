import logging

import pytz
from flask import Flask, request, render_template, jsonify
from flask_cors import CORS
from db_connector import write_to_influx, get_data

app = Flask(__name__)
CORS(app)

@app.route('/add', methods=['POST'])
def add_brightness():
    # bright == 0, dark == 1
    light_detected = request.json['light_detected']
    try:
        write_to_influx(light_detected)
    except Exception as e:
        return jsonify({"error": str(e)})
    return jsonify({"message": "Data added successfully"}), 200

@app.route('/', methods=['GET'])
def show_data():
    record = get_data()
    print(f"Retrieved record from InfluxDB: {record}")
    if record["value"] is None or record["time"] is None:
        data = [{
            'light_detected': 'No data',
            'timestamp': 'N/A',
        }]
    else:
        data = [{
            'light_detected': record["value"],
            'timestamp': record["time"].astimezone(pytz.timezone("Europe/Berlin")).strftime("%Y-%m-%d %H:%M:%S"),
        }]
    print(f"Data: {data}")
    return render_template('showData.html', data=data)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
