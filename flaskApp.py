from flask import Flask, request, jsonify, render_template
import sqlite3

from flask_cors import CORS

app = Flask(__name__)
CORS(app)

def connect_db():
    return sqlite3.connect('light_data.db')

def cleanup_old_data():
    try:
        with connect_db() as conn:
            with conn.cursor() as cursor:
                # Delete records older than 30 days
                cursor.execute('''
                    DELETE FROM light 
                    WHERE timestamp < datetime('now', '-30 days')
                ''')
                conn.commit()
    except sqlite3.Error as e:
        print(f"Error cleaning up old data: {e}")

@app.route('/add', methods=['POST'])
def add_brightness():
    light_detected = request.json['light_detected']
    try:
        with connect_db() as conn:
            with conn.cursor() as cursor:
                cursor.execute('INSERT INTO light (light_detected) VALUES (?)', (light_detected,))
                cleanup_old_data()
                conn.commit()
        return jsonify({'status': 'success'})
    except sqlite3.Error as e:
        return jsonify({'error': str(e)}), 500

@app.route('/data', methods=['GET'])
def get_data():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT light_detected, timestamp FROM light ORDER BY timestamp DESC LIMIT 1')
    row = cursor.fetchone()
    conn.close()
    if row:
        return jsonify({
            'light_detected': row[0],
            'timestamp': row[1]
        })
    else:
        return jsonify({'error': 'No data found'}), 404

@app.route('/', methods=['GET'])
def show_data():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT light_detected, timestamp FROM light ORDER BY timestamp DESC LIMIT 1')
    rows = cursor.fetchall()
    conn.close()
    data = []
    for row in rows:
        data.append({
            'light_detected': row[0],
            'timestamp': row[1]
        })
    return render_template('showData.html', data=data)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
