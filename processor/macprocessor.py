import socket
import zlib
import json

def connect_to_server(server_ip, port=65433):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((server_ip, port))
            print("Connected to server.")
            # Receive the size of the compressed data first
            data_size = int.from_bytes(sock.recv(4), 'big')
            compressed_data = b''
            while len(compressed_data) < data_size:
                packet = sock.recv(4096)
                if not packet:
                    break
            compressed_data += packet
            # Decompress the data
            decompressed_data = zlib.decompress(compressed_data)
            data = json.loads(decompressed_data.decode('utf-8'))
            print("Received decompressed JSON data:")
            print(json.dumps(data, indent=4))
            # Implement data processing logic here
    except socket.error as e:
        print(f"Could not connect to server {server_ip} on port {port}: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    SERVER_IP = '10.0.0.224'
    connect_to_server(SERVER_IP, 65433)
