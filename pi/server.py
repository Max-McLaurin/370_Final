import socket
import select
import zlib
import json
import csv

def json_to_csv(data, filename='weather_data.csv'):
    if isinstance(data, dict) and 'temperature' in data and 'weather' in data:
        fields = ['date', 'temp_min', 'temp_max', 'weather_main', 'weather_description']
        with open(filename, 'w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=fields)
            writer.writeheader()
            for entry in data:
                writer.writerow({
                    'date': entry['date'],
                    'temp_min': entry['temperature']['min'],
                    'temp_max': entry['temperature']['max'],
                    'weather_main': entry['weather']['main'],
                    'weather_description': entry['weather']['description']
                })

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
        # Receive the size of the compressed data
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
        print("Decompressed data received and processed:")
        print(json.dumps(data, indent=4))
        # Optionally convert to CSV
        json_to_csv(data, 'weather_data.csv')
        print("Data converted to CSV.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    start_server()
