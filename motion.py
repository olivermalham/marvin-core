import os
import errno
import json

BASE_DIR = '/etc/marvin/'
MOTION_FIFO = 'motion'

"""
Example JSON packet
{
  'wheels': {
    'direction': [1, 2, 3, 4 ,5 ,6],
    'speed': [0, 0, 0, 255, 255, 255]
  },
  'head': {
    'pitch': 0,
    'yaw': 0
  }
}
"""

try:
    os.mkfifo(BASE_DIR+MOTION_FIFO)
except OSError as oe:
    if oe.errno != errno.EEXIST:
        raise

while True:
    print("Opening motion FIFO...")
    with open(BASE_DIR+MOTION_FIFO) as fifo:
        print("FIFO opened")
        while True:
            data = fifo.read()
            if len(data) == 0:
                print("Client disconnected")
                break
            try:
              command = json.loads(data)
              print('Read: "{0}"'.format(data))
              
            except:
              print("Error reading JSON packet")
              # Need better error handling!
              
