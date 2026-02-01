import io
import json
import threading
import numpy as np
import pyaudio
import socket
import soundfile as sf
import time

srv = ("localhost", 49111)

recv_all = 0
send_all = 0

CHUNK = 4096
FORMAT = pyaudio.paFloat32
CHANNELS = 1
RATE = 16000
p = pyaudio.PyAudio()
stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE,
                 input=True, output=True, frames_per_buffer=CHUNK)

class udp:
    def __init__(self):
        self.connected = False
        self.udp_sock: socket.socket = None
        self.recv_th = None
        self.send_th = None
        self.check_th = None
        self.muted = False

    def connect(self, host, port):
        self.connected = True
        print(host, port)
        self.udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.udp_sock.connect((host, port))

        def RAW_2_OGG(raw_chunk):
            byte_io = io.BytesIO()
            signal = np.frombuffer(raw_chunk, dtype=np.float32)
            sf.write(byte_io, signal, RATE, format='OGG')
            return byte_io.getvalue()

        def OGG_2_RAW(ogg_chunk):
            byte_io = io.BytesIO(ogg_chunk)
            data, samplerate = sf.read(byte_io)
            return (data * 1.0).astype(np.float32)

        def recv():
            global recv_all
            while True:
                if not self.connected:
                    return
                try:
                    data = self.udp_sock.recv(CHUNK * 10)
                    recv_all += CHUNK * 10
                    stream.write(OGG_2_RAW(data), CHUNK)
                except:
                    return 0

        def send():
            global send_all
            while True:
                if not self.connected:
                    return

                if not self.muted:
                    pass
                try:

                    data = stream.read(CHUNK, exception_on_overflow=False)
                    data = RAW_2_OGG(data)
                    self.udp_sock.sendall(data)
                    send_all += len(data)
                except:
                    return 0

        def check():
            b = 0
            while True:
                if not self.connected:
                    return
                if b % 1000000 == 0:
                    print(f'packs udp: {send_all} | {recv_all} {self.connected}')
                b += 1
                if not self.recv_th.is_alive() or not self.send_th.is_alive():
                    print("udp  : voice   : not work  - died")
                    return 0

        self.recv_th = threading.Thread(target=recv)
        self.recv_th.start()
        self.send_th = threading.Thread(target=send)
        self.send_th.start()
        self.check_th = threading.Thread(target=check)
        self.check_th.start()

    def disconnect(self):
        if self.connected:
            self.connected = False
            self.udp_sock.close()

class tcp:
    def __init__(self,host, port):
        self.host = host
        self.port = port

    def ping(self) -> float:
        tcp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcp_sock.connect((self.host, self.port))
        ping_time = time.perf_counter_ns()
        tcp_sock.send(b'PING')
        tcp_sock.recv(1024)
        ping_answer_time = time.perf_counter_ns()
        return (ping_answer_time-ping_time)/ 1_000_000

    def get_channels(self):
        tcp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcp_sock.connect((self.host, self.port))
        tcp_sock.send(json.dumps({'action': "get_channels"}).encode())
        return tcp_sock.recv(1024).decode()

    def connect(self, uuid):
        tcp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcp_sock.connect((self.host, self.port))
        tcp_sock.send(json.dumps({'action': "connect_to", "uuid": uuid}).encode())
        return tcp_sock.recv(1024).decode()

    def disconnect(self):
        tcp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcp_sock.connect((self.host, self.port))
        tcp_sock.send(json.dumps({'action': "disconnect"}).encode())
        return tcp_sock.recv(1024).decode()
try:
    tcp(srv[0], srv[1])
except:print("tcp  : all   : not work")





