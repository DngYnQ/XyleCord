import socket
import json

with open('config.json', 'r') as openfile:
    config = json.load(openfile)

sock_srv = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
sock_srv.bind((config['ip'], config['port']))

def run():
    print("[TCP] OK")


run()