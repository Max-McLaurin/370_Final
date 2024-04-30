import socket
import zlib
import json
import os

def start_server(host='0.0.0.0', port=65433):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"Server listening on {host}:{port}")

    try:
        while True:
            client_socket, addr = server_socket.accept()
            print(f"Accepted connection from {addr}")
            handle_connection(client_socket)
    except KeyboardInterrupt:
        print("Server is shutting down.")
    finally:
        server_socket.close()

def handle_connection(client_socket):
    # First, check if it's a data sending or file receiving
    mode = client_socket.recv(1).decode('utf-8')  # Expect 'D' for data, 'F' for file
    if mode == 'D':
        data = handle_client_data(client_socket)
        print("Data received from client and processed.")
        if data:
            # Optionally send data back or notify other systems
            pass
    elif mode == 'F':
        receive_file_from_client(client_socket, 'received_image.png')
        print("Image received from processor.")
    client_socket.close()

def handle_client_data(client_socket):
    try:
        # Receive the size of the compressed data first
        data_size = int.from_bytes(client_socket.recv(4), 'big')
        compressed_data = b''
        while len(compressed_data) < data_size:
            packet = client_socket.recv(4096)
            if not packet:
                break
            compressed_data += packet
        
        # Decompress the data
        decompressed_data = zlib.decompress(compressed_data)
        data = json.loads(decompressed_data.decode('utf-8'))
        print("Decompressed data received and processed:", json.dumps(data, indent=4))
        
        return data
    except Exception as e:
        print(f"An error occurred (server): {e}")
        return None

def receive_file_from_client(client_socket, file_path):
    try:
        file_size = int.from_bytes(client_socket.recv(8), 'big')
        with open(file_path, 'wb') as file:
            bytes_received = 0
            while bytes_received < file_size:
                chunk = client_socket.recv(4096)
                if not chunk:
                    break
                file.write(chunk)
                bytes_received += len(chunk)
        print(f"File {file_path} has been received successfully.")
    except Exception as e:
        print(f"An error occurred while receiving the file: {e}")

if __name__ == "__main__":
    start_server()
