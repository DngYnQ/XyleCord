import socket
import json

with open('config.json', 'r') as openfile:
    config = json.load(openfile)
sock_srv = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock_srv.bind((config['ip'], config['port']))
CHUNK = 4096
clients = []
print("[UDP] OK")
while True:
    try:
        message, address = sock_srv.recvfrom(CHUNK * 10)
        print(f"{address} connected.", clients)
        if not address in clients:
            clients.append(address)
        for i in clients:
            if 1 != address:
                try:
                    sock_srv.sendto(message, i)
                except Exception as e:
                    print(e)
                    clients.remove(i)
    except Exception as e:
        print(e)