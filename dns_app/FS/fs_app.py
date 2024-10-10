# -*- coding: utf-8 -*-
"""
@author: 12852
"""

from flask import Flask, request, jsonify
import socket

app = Flask(__name__)

@app.route('/register', methods=['PUT'])
def register():
    data = request.get_json()
    hostname = data.get('hostname')
    ip = data.get('ip')
    as_ip = data.get('as_ip')
    as_port = data.get('as_port')

    # Check if any parameter is missing
    if not all([hostname, ip, as_ip, as_port]):
        return jsonify({"error": "Missing required parameters"}), 400

    # Send a registration request to the Authoritative Server
    registration_message = f"TYPE=A\nNAME={hostname}\nVALUE={ip}\nTTL=10\n"
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.sendto(registration_message.encode(), (as_ip, int(as_port)))

    return jsonify({"message": "Registration successful"}), 201

@app.route('/fibonacci', methods=['GET'])
def fibonacci():
    number = request.args.get('number', default=None, type=int)
    if number is None or not isinstance(number, int):
        return jsonify({"error": "Invalid or missing 'number' parameter"}), 400

    # Calculate the Fibonacci number
    fib_value = calculate_fibonacci(number)
    return jsonify({"number": number, "fibonacci": fib_value}), 200

def calculate_fibonacci(n):
    if n <= 0:
        return 0
    elif n == 1:
        return 1
    else:
        a, b = 0, 1
        for _ in range(2, n + 1):
            a, b = b, a + b
        return b

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9090)
