import socket
import zlib
import json
import csv

def json_to_csv(data):
    if isinstance(data, list):  # Assuming data is a list of dictionaries
        output = io.StringIO()
        if data:
            keys = data[0].keys()  # Assumes all dictionaries have the same structure
            writer = csv.DictWriter(output, fieldnames=keys)
            writer.writeheader()
            writer.writerows(data)
        return output.getvalue()
    else:
        raise ValueError("Data is not in expected list format.")

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
            handle_client_connection(client_socket)
            client_socket.close()
    except KeyboardInterrupt:
        print("Server is shutting down.")
    finally:
        server_socket.close()

def handle_client_connection(client_socket):
    try:
        # Receive data
        compressed_data = client_socket.recv(4096)
        # Decompress data
        decompressed_data = zlib.decompress(compressed_data)
        data = json.loads(decompressed_data.decode('utf-8'))
        print("Decompressed data received and processed:")
        # Convert to CSV
        csv_data = json_to_csv(data)
        compressed_csv = zlib.compress(csv_data.encode('utf-8'))
        # Send compressed CSV
        client_socket.sendall(compressed_csv)
        print("Compressed CSV data sent to processor.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    start_server()
