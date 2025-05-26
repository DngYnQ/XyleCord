import io
import threading
import numpy as np
import pyaudio
import socket
import soundfile as sf

srv = ("localhost", 49111)

CHUNK = 4096
FORMAT = pyaudio.paFloat32
CHANNELS = 1
RATE = 16000
p = pyaudio.PyAudio()
stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE,
                 input=True, output=True, frames_per_buffer=CHUNK)



def udp():
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
        while True:
            try:
                data = udp_sock.recv(CHUNK * 10)
                stream.write(OGG_2_RAW(data), CHUNK)
            except:return 0
    def send():
        while True:
            try:
                data = stream.read(CHUNK, exception_on_overflow=False)
                data = RAW_2_OGG(data)
                udp_sock.sendall(data)
            except:return 0

    def check():
        while True:
            if not recv_th.is_alive() or not send_th.is_alive():
                print("udp  : voice   : not work  - died")
                return 0

    recv_th = threading.Thread(target=recv)
    recv_th.start()
    send_th=threading.Thread(target=send)
    send_th.start()
    check_th = threading.Thread(target=check)
    check_th.start()



def tcp():
    ...

print('TYPE : SERVICE : STATUS')
try:
    udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_sock.connect(srv)
    print('udp  : voice   : work')
    udp()
except:print("udp  : voice   : not work")

try:
    tcp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_sock.connect(srv)
    print('tcp  : chat   : work')
    tcp()
except:print("tcp  : chat    : not work")




