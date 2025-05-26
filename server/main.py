import json
import os.path
import subprocess

def save_default():
    default = {
        'ip': 'localhost',
        'port': 49111
    }
    with open("config.json", "w") as outfile:
        outfile.write(json.dumps(default, indent=4))

if not os.path.exists('config.json'):
    save_default()

with open('config.json', 'r') as openfile:
    config = json.load(openfile)

print(f"Working TCP & UDP on {config['ip']}:{config['port']}")

subprocess.run(["python", "udp.py"], capture_output=True, text=True)
subprocess.run(["python", "tcp.py"], capture_output=True, text=True)