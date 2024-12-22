import socket

sock_srv = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
sock_srv.bind(("localhost", 22862))
CHUNK=4096
clients = []
while True:
    try:
        message, address = sock_srv.recvfrom(CHUNK*10)
        sock_srv.sendto(message, address)
    except Exception as e:
        print(e)