import socket
import threading
import ast


def handle_client(client_socket, client_address):
    while True:
        try:
            # First receive the length of the message
            length = int.from_bytes(client_socket.recv(8), 'big')
            # Then receive the message itself
            data = client_socket.recv(length).decode('utf-8')
            if not data:
                break
            print(f"Received from {client_address}: {data}")

            # Extract the recipient client's address from the message
            recipient_address, message = data.split(':', 1)

            # Find the recipient client's socket
            recipient_socket = None
            for client in clients:
                if client[1] == ast.literal_eval(recipient_address):
                    recipient_socket = client[0]
                    break
            if recipient_socket:
                # Send the message to the recipient client
                # First send the length of the message
                recipient_socket.send(len(message).to_bytes(8, 'big'))
                # Then send the message itself
                recipient_socket.send(message.encode('utf-8'))
            else:
                print(f"No client with address {recipient_address} found.")
        except socket.error:
            break

    print(f"Connection closed with {client_address}")
    clients.remove((client_socket, client_address))
    client_socket.close()

def start_server():
    host = 'localhost'
    port = 8000

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"Server started on {host}:{port}")
    while True:
        client_socket, client_address = server_socket.accept()
        clients.append((client_socket, client_address))
        print(f"Connected with {client_address}")
        threading.Thread(target=handle_client, args=(client_socket, client_address)).start()

if __name__ == '__main__':
    clients = []
    start_server()