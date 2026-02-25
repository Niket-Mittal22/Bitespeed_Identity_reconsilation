from flask import Flask, request, jsonify
import sqlite3
from datetime import datetime
from util_func import reconcile_and_fetch

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('bitespeed.db')
    conn.row_factory = sqlite3.Row 
    return conn

@app.route('/identify', methods=['POST'])
def identify():
    data = request.json
    email = data.get('email')
    phone_number = data.get('phoneNumber')

    if not email and not phone_number:
        return jsonify({"error": "Email or phoneNumber required"}), 400

    conn = get_db_connection()
    
    result = reconcile_and_fetch(conn, email, phone_number)
    
    conn.close()
    return jsonify(result), 200

if __name__ == '__main__':
    app.run(debug=True, port=3000)