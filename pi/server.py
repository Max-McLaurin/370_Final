import socket
import select
from collections import deque
import json


def start_server(host='0.0.0.0', port=65433):
   server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
   server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
   server_socket.bind((host, port))
   server_socket.listen(2)
   print(f"Server listening on {host}:{port}")


   sockets_list = [server_socket]
   client_address_map = {}
   clients = {"scraper": None, "processor": None}
   data_queue = deque()


   while True:
       read_sockets, _, exception_sockets = select.select(sockets_list, [], sockets_list)


       for notified_socket in read_sockets:
           if notified_socket == server_socket:
               client_socket, client_address = server_socket.accept()
               sockets_list.append(client_socket)
               client_address_map[client_socket] = client_address
               print(f"Accepted new connection from {client_address}")
              
               if not clients["scraper"]:
                   clients["scraper"] = client_socket
                   print(f"Scraper client connected: {client_address}")
               elif not clients["processor"]:
                   clients["processor"] = client_socket
                   print(f"Processor client connected: {client_address}")


           else:
               message = notified_socket.recv(4096)  # Larger buffer size
               print(message, "Data recieved from scraper.")
               if message:
                   if notified_socket == clients["scraper"]:
                       # Save or forward the data
                       if clients["processor"]:








                           clients["processor"].sendall(message)
                       else:
                           data_queue.append(message)
                           # Convert bytes to string and then to JSON
                           data = json.loads(message.decode('utf-8'))
                           # Save the JSON data to a file
                           with open('received_data.json', 'w') as json_file:
                               json.dump(data, json_file, indent=4)
                               print("Data saved to received_data.json")
               else:
                   print(f"Closed connection from {client_address_map[notified_socket]}")
                   sockets_list.remove(notified_socket)
                   del client_address_map[notified_socket]
                   if notified_socket == clients["scraper"]:
                       clients["scraper"] = None
                   elif notified_socket == clients["processor"]:
                       clients["processor"] = None
                   notified_socket.close()


       for notified_socket in exception_sockets:
           sockets_list.remove(notified_socket)
           del client_address_map[notified_socket]
           notified_socket.close()


if __name__ == "__main__":
   start_server()
