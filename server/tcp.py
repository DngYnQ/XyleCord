import socket
import json
import threading
import uuid

with open('config.json', 'r') as openfile:
    config = json.load(openfile)

sock_srv = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
sock_srv.bind((config['ip'], config['port']))
sock_srv.listen(5)

channels = [
    {"uuid": uuid.uuid4().__str__(), "name":"test", "type": "text", "max_users": -1},
    {"uuid": uuid.uuid4().__str__(), "name": "test_2", "type": "voice", "max_users": -1}
]

def run():
    def handle_client(sock: socket.socket, addr):
        while sock:
            data = sock.recv(2048)
            if data != b'':
                pass

            if data != b'':
                print(data)
                if data.startswith(b"PING"):
                    sock.sendall(b"PONG")
                    pass
                else:
                    print(data)
                    data = json.loads(data)
                    if data['action'] == 'get_channels':
                        sock.send(json.dumps(channels).encode())
                    if data['action'] == 'connect_to':
                        sock.send(json.dumps({"data": "OK!", "host": {"ip": "127.0.0.1", "port": 49111}}).encode())
                    if data['action'] == 'disconnect':
                        sock.send(json.dumps({"data": "OK!"}).encode())





    print("[TCP] OK")
    while True:
        sock, addr = sock_srv.accept()
        threading.Thread(target=handle_client, args=(sock,addr)).start()

run()