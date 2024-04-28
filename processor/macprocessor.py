import socket
import csv
import io
import zlib

def connect_to_server(server_ip, port=65433):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((server_ip, port))
            print("Connected to server.")
            # Receive compressed CSV data
            compressed_data = b''
            while True:
                part = sock.recv(8192)
                if not part:
                    break
                compressed_data += part
            # Decompress CSV data
            if compressed_data:
                decompressed_data = zlib.decompress(compressed_data)
                print("Received decompressed CSV data:")
                file_stream = io.StringIO(decompressed_data.decode('utf-8'))
                reader = csv.reader(file_stream)
                for row in reader:
                    print(row)
            else:
                print("No data received.")
    except socket.error as e:
        print(f"Could not connect to server {server_ip} on port {port}: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    SERVER_IP = '10.0.0.224'  # Ensure this is the correct IP address
    connect_to_server(SERVER_IP, 65433)
