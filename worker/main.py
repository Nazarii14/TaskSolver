import os
import logging
import psycopg2
from constants import *
from database import conn, find_nth_prime_number
from flask import Flask, g, request
from flask import jsonify
from psycopg2 import sql
from flask_cors import CORS

logging.basicConfig(level=logging.INFO)
app = Flask(__name__)

CORS(app, resources={
    r"/*": {
        "origins": "*",
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})

@app.route('/process_number/', methods=['POST'])
def process_number():
    data = request.get_json()
    print(f'Processing number: {data}')
    id = data['task_id']
    number = int(data['number'])
    result = find_nth_prime_number(number, id)
    conn.commit()

    return jsonify({'status': 'success', 'result': result})


@app.route('/home', methods=['GET'])
def home():
    return jsonify({'served_from': str(os.getpid())})


if __name__ == '__main__':
    app.run(debug=True, use_reloader=True, host='0.0.0.0', port=1001)
