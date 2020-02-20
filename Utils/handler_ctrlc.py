import time
import signal
import sys

def signal_handler(signal, frame):
    print('Last operation before end of the program', '*'*100)
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

while True:
    time.sleep(1)
    print('hi')
