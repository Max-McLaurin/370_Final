import socket
import os
import subprocess
import time
import json
import brotli  
import zlib

class ServerConnection:
    def __init__(self, server_ip, port):
        self.server_ip = server_ip
        self.port = port
        self.sock = None

    def connect(self):
        """Establish a connection to the server."""
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.server_ip, self.port))
        print("Connected to server.")

    def close(self):
        """Close the server connection."""
        if self.sock:
            self.sock.close()
            print("Disconnected from server.")

    def send_file(self, file_path):
        """Send a compressed file using the existing connection."""
        try:
            with open(file_path, 'rb') as file:
                file_data = file.read()  # Read the entire file into memory

            # Compress the data using Brotli
            compressed_data = brotli.compress(file_data)
            compressed_size = len(compressed_data)
            print(f"Original size: {os.path.getsize(file_path)} bytes; Compressed size: {compressed_size} bytes")

            # Send the size of the compressed file to the server
            self.sock.sendall(compressed_size.to_bytes(8, 'big'))

            # Send the compressed file data
            self.sock.sendall(compressed_data)
            print(f"Compressed file {file_path} has been sent successfully.")
            
        except socket.error as e:
            print(f"Socket error during file send: {e}")
        except Exception as e:
            print(f"Error during file send: {e}")

    def receive_and_process_data(self):
        """Receive compressed data, decompress, save and call a subprocess."""
        try:
            data_size = int.from_bytes(self.sock.recv(4), 'big')
            print("Size of data_size: ", data_size)
            compressed_data = b''
            while len(compressed_data) < data_size:
                packet = self.sock.recv(4096)
                if not packet:
                    break
                compressed_data += packet

            # Decompress the data using zlib
            decompressed_data = zlib.decompress(compressed_data)
            data = json.loads(decompressed_data.decode('utf-8'))
            print("Received decompressed JSON data:")
            print(json.dumps(data, indent=4))

            # Save data to a JSON file
            with open('output.json', 'w') as json_file:
                json.dump(data, json_file, indent=4)
            print("Data saved to 'output.json'.")

            # Wait and then call a subprocess
            time.sleep(20)
            print("Calling subprocess: pretty.py")
            subprocess.call(['python3', 'pretty.py'])
            time.sleep(10)
            print("Calling twitter.py to upload weather")
            subprocess.call(['python3', 'twitter.py'])
            

        except socket.error as e:
            print(f"Socket error during data receive: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    SERVER_IP = '10.0.0.224'
    PORT = 65434
    FILE_PATH = 'weather_dashboard.png'
    
    conn = ServerConnection(SERVER_IP, PORT)
    conn.connect()
    conn.receive_and_process_data()
    conn.send_file(FILE_PATH)
    conn.close()
    print("Operations completed on server.")
