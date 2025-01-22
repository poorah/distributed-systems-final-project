import requests
import time
import socket
import threading
import os
import random
import json

# URL مربوط به API
api_endpoint = "http://localhost:5000/ingest"
clients = {}
client_count = 0
active_clients = 0  # Track the number of active clients
data = {}

def fetch_data():
    try:
        # ارسال درخواست GET به API
        response = requests.get(api_endpoint)
        
        # بررسی وضعیت پاسخ
        if response.status_code == 200:
            # داده‌های JSON را استخراج می‌کنیم
            data = response.json()
            return data
        else:
            print(f"Failed to fetch data. Status code: {response.status_code}")
            return None
    except Exception as e:
        print(f"Error occurred: {e}")
        return None


def handle_client(client_socket, client_id):
    global clients, data, active_clients

    while True:
        try:
            message = client_socket.recv(1024).decode("utf-8")
            if message:
                print(f"client message: {message.lower()}")
                if message.lower() == "finish":
                    client_socket.send("[CHAT ENDED] You can exit now.".encode("utf-8"))
                    break
                elif message.lower() == "data":
                    json_data = json.dumps(data[0]) 
                    client_socket.send(f"{json_data}".encode("utf-8"))
                    print(f"[SEND DATA] to {client_id}")
                else:
                    client_socket.send("Unknown command".encode("utf-8")) 
            else:
                break
        except:
            break

    client_socket.close()
    del clients[client_id]
    active_clients -= 1  # Decrease active client count
    print(f"Client[{client_id}] disconnected. Active clients: {active_clients}")

    # Check if there are no active clients left
    if active_clients == 0:
        print("No active clients left. Closing server.")
        shutdown_server()


def shutdown_server():
    for client_socket in clients.values():
        client_socket.close()
    print("Server socket closed.")
    exit(0)  # Exit the server application


def server_socket():
    global client_count, active_clients, data
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("0.0.0.0", 5555))
    server.listen(5)
    print("[SERVER STARTED] server listening on port 5555...")   

    while True:
        client_socket, client_address = server.accept()
        client_count += 1
        client_id = client_count
        clients[client_id] = client_socket
        active_clients += 1  # Increase active client count
        print(f"[ACCEPT CONNECTION] from {client_address}, assigned client ID: {client_id}")
        thread = threading.Thread(target=handle_client, args=(client_socket, client_id))
        thread.start()


def main():
    global data
    server_thread = threading.Thread(target=server_socket, daemon=True)
    server_thread.start()
    while True:
        data = fetch_data()
        if data:
            print("Received data:")
            print(data)
        time.sleep(5)
            

if __name__ == "__main__":
    # print(data)
    main()