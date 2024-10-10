# -*- coding: utf-8 -*-
"""
@author: Xueyao Zhao
"""

import socket
import threading

# A dictionary to store the DNS records
dns_records = {}

def handle_client(connection, address):
    while True:
        try:
            data, addr = connection.recvfrom(1024)
            if not data:
                break
            message = data.decode().split("\n")
            if "TYPE=A" in message[0]:
                name = message[1].split("=")[1]
                if name in dns_records:
                    response = f"TYPE=A\nNAME={name}\nVALUE={dns_records[name]['value']}\nTTL={dns_records[name]['ttl']}\n"
                    connection.sendto(response.encode(), addr)
            elif "VALUE" in message[2]:
                # This is a registration request
                name = message[1].split("=")[1]
                value = message[2].split("=")[1]
                ttl = int(message[3].split("=")[1])
                dns_records[name] = {"value": value, "ttl": ttl}
        except Exception as e:
            print(f"Error handling client {address}: {e}")
            break

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server.bind(("0.0.0.0", 53533))
    print("Authoritative Server is running on port 53533")
    while True:
        threading.Thread(target=handle_client, args=(server, server.getsockname())).start()

if __name__ == '__main__':
    start_server()
