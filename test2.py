import pyaudio

CHUNK=4096
FORMAT = pyaudio.paFloat32
CHANNELS = 1
RATE = 16000
p = pyaudio.PyAudio()
stream=p.open(format=FORMAT,channels=CHANNELS,rate=RATE,
            input=True,output=True,frames_per_buffer=CHUNK)

while True:
    data = stream.read(CHUNK, exception_on_overflow=False)
    stream.write(data)