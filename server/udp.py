import socket
import json

from collections import defaultdict
import time

with open('config.json', 'r') as openfile:
    config = json.load(openfile)
sock_srv = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock_srv.bind((config['ip'], config['port']))
CHUNK = 4096
clients = []
last_seen = defaultdict(float)

print("[UDP] OK")
while True:
    try:
        message, address = sock_srv.recvfrom(CHUNK * 10)
        last_seen[address] = time.time()

        if address not in clients:
            clients.append(address)
        for i in clients:
            if 1 != address:
                try:
                    sock_srv.sendto(message, i)
                except Exception as e:
                    print("f ", e)
                    clients.remove(i)

    except OSError as e:
        if e.winerror == 10054:
            print("→ 10054 (вероятно кто-то умер)")
        continue
    now = time.time()
    dead = [addr for addr, ts in list(last_seen.items()) if now - ts > 20]

    for addr in dead:
        if addr in clients:
            clients.remove(addr)
        del last_seen[addr]
        print(f"Удалён по таймауту: {addr}")