# -*- coding: utf-8 -*-
"""
@author: Xueyao Zhao
"""

from flask import Flask, request, jsonify
import requests
import socket

app = Flask(__name__)

@app.route('/fibonacci', methods=['GET'])
def fibonacci():
    hostname = request.args.get('hostname')
    fs_port = request.args.get('fs_port')
    number = request.args.get('number')
    as_ip = request.args.get('as_ip')
    as_port = request.args.get('as_port')

    # Check if any parameter is missing
    if not all([hostname, fs_port, number, as_ip, as_port]):
        return jsonify({"error": "Missing required parameters"}), 400

    # Query the Authoritative Server to resolve hostname to IP
    fs_ip = query_authoritative_server(hostname, as_ip, int(as_port))
    if not fs_ip:
        return jsonify({"error": "Could not resolve hostname"}), 400

    # Make a request to the Fibonacci Server
    try:
        response = requests.get(f"http://{fs_ip}:{fs_port}/fibonacci?number={number}")
        if response.status_code == 200:
            return response.json(), 200
        else:
            return jsonify({"error": "Fibonacci Server error"}), response.status_code
    except requests.RequestException as e:
        return jsonify({"error": str(e)}), 500

def query_authoritative_server(hostname, as_ip, as_port):
    # Send a UDP request to the Authoritative Server
    message = f"TYPE=A\nNAME={hostname}\n"
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.sendto(message.encode(), (as_ip, as_port))
        try:
            data, _ = sock.recvfrom(1024)
            response = data.decode().split("\n")
            if response[0].strip() == "TYPE=A" and response[1].strip().startswith("NAME="):
                return response[2].strip().split("=")[1]
        except socket.timeout:
            return None
    return None

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
