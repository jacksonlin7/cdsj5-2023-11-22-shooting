import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('172.16.172.218', 3000))
