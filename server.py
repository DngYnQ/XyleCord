import socket

sock_srv = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
sock_srv.bind(("localhost", 59159))
CHUNK=4096
clients = []
while True:
    try:
        message, address = sock_srv.recvfrom(CHUNK*10)
        print(f"{address} connected.")
        clients.append(address)
        for i in clients:
            if i != address:
                sock_srv.sendto(message, i)
    except Exception as e:
        print(e)