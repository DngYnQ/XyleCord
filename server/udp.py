import socket
import json
from collections import defaultdict
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

# ────────────────────────────────────────
with open('config.json', 'r') as f:
    config = json.load(f)

sock_srv = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock_srv.bind((config['ip'], config['port']))

CHUNK = 4096
clients = []
last_seen = defaultdict(float)

# Один пул на 8–16 потоков обычно хватает
executor = ThreadPoolExecutor(max_workers=12)

print("[UDP] OK")

def send_to_client(client_addr, data):
    try:
        sock_srv.sendto(data, client_addr)
    except Exception as e:
        print(f"  send failed → {client_addr}  {e}")
        return client_addr   # вернём, чтобы удалить
    return None


while True:
    try:
        message, address = sock_srv.recvfrom(CHUNK * 10)
        last_seen[address] = time.time()

        if address not in clients:
            clients.append(address)
            print(f"→ new {address}  ({len(clients)})")
        dead_from_send = []
        futures = [
            executor.submit(send_to_client, addr, message)
            for addr in clients
        ]

        for future in as_completed(futures):
            failed_addr = future.result()
            if failed_addr is not None:
                dead_from_send.append(failed_addr)
        for addr in dead_from_send:
            if addr in clients:
                clients.remove(addr)
                print(f"  removed on send fail: {addr}")

    except OSError as e:
        if e.winerror == 10054:
            print("→ 10054 (кто-то умер)")
        continue

    # таймаут чистка (можно вынести в отдельный поток позже)
    now = time.time()
    dead = [addr for addr, ts in list(last_seen.items()) if now - ts > 20]

    for addr in dead:
        if addr in clients:
            clients.remove(addr)
        if addr in last_seen:
            del last_seen[addr]
        print(f"Удалён по таймауту: {addr}")