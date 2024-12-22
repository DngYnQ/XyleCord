import io
import threading
import numpy as np
import pyaudio
import socket
import soundfile as sf

CHUNK = 4096
FORMAT = pyaudio.paFloat32
CHANNELS = 1
RATE = 16000
p = pyaudio.PyAudio()
stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE,
                 input=True, output=True, frames_per_buffer=CHUNK)

def RAW_2_OGG(raw_chunk):
    byte_io = io.BytesIO()
    signal = np.frombuffer(raw_chunk, dtype=np.float32)
    sf.write(byte_io, signal, RATE, format='OGG')
    return byte_io.getvalue()
def OGG_2_RAW(ogg_chunk):
    byte_io = io.BytesIO(ogg_chunk)
    data, samplerate = sf.read(byte_io)
    return (data * 1.0).astype(np.float32)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.connect(("localhost", 22862))

def recv():
    while True:
        data = sock.recv(CHUNK*10)
        stream.write(OGG_2_RAW(data), CHUNK)


def send():
    while True:
        data = stream.read(CHUNK, exception_on_overflow=False)
        data = RAW_2_OGG(data)
        sock.sendall(data)

threading.Thread(target=recv).start()
threading.Thread(target=send).start()
