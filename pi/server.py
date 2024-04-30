import socket
import zlib
import json

def start_server(host='0.0.0.0', port=65433):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"Server listening on {host}:{port}")

    connections = []

    try:
        while True:
            client_socket, addr = server_socket.accept()
            print(f"Accepted connection from {addr}")
            connections.append(client_socket)
            if len(connections) == 1:
                # Handle scraper connection
                data = handle_client_connection(client_socket)
                print("Data received from scraper and processed.")
            elif len(connections) == 2:
                # Handle processor connection
                send_data_to_processor(client_socket, data)
                print("Data sent to processor.")
            else:
                print("Unexpected connection ignored.")
            
    except KeyboardInterrupt:
        print("Server is shutting down.")
    finally:
        server_socket.close()

def handle_client_connection(client_socket):
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

def send_data_to_processor(client_socket, data):
    try:
        serialized_data = json.dumps(data).encode('utf-8')
        compressed_data = zlib.compress(serialized_data)
        # Send the size of the compressed data first
        client_socket.sendall(len(compressed_data).to_bytes(4, 'big'))
        # Then send the compressed data
        client_socket.sendall(compressed_data)
        print("Compressed data sent to processor.")
    except Exception as e:
        print(f"An error occurred when sending to processor: {e}")

if __name__ == "__main__":
    start_server()