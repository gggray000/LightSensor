from flask import Flask, request, render_template
from flask_cors import CORS
from db_connector import write_to_influx, get_data

app = Flask(__name__)
CORS(app)

@app.route('/add', methods=['POST'])
def add_brightness():
    # bright == 0, dark == 1
    light_detected = request.json['light_detected']
    write_to_influx(light_detected)

@app.route('/', methods=['GET'])
def show_data():
    record = get_data()
    data = [{
        'light_detected': record["value"],
        'timestamp': record["time"],
    }]
    return render_template('showData.html', data=data)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
