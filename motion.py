#!/usr/bin/python3

import os
import errno
import json

BASE_DIR = '/etc/marvin/'
MOTION_FIFO = 'motion'

# USB serial ports for Arduino Nanos that control left and right side motors
left_control_port = '/dev/ttyUSB0'
right_control_port = '/dev/ttyUSB1'

valid_attributes = ["wheel", "head"]

"""
Note that the wheels are numbered front to back, odd on the left, even on the right.
Wheel array *must* have exactly six entries.
Speed is between 0 and 1.0, and is treated as a fraction of the maximum speed.
All directions are 0 for straight foward, positive for right, negaive for left.
Positive head pitch is up.

Example JSON packet.
{
  'wheel': [
        {
            'direction': 0,
            'speed': 0.25 
        },
        {
            'direction': 0,
            'speed': 0.25 
        }
    ]
  'head': {
    'pitch': 0,
    'yaw': 0
  }
}

We're assuming that the wheel servo IDs match the numbering described above. Head yaw will have ID 7, pitch 8.
"""


def valid_command(command):
    """ Check the received JSON matches what we expect
    """
    for key in command:
        if key not in valid_attributes:
            return False
    return True



while True:
    print(f"Listening to motion FIFO on {BASE_DIR}{MOTION_FIFO}...")
    with open(BASE_DIR+MOTION_FIFO) as fifo:
        print(f"FIFO opened")
        while True:
            data = fifo.read()
            print('Read: "{0}"'.format(data.strip()))
            if len(data) == 0:
                print("Client disconnected")
                break
            try:
              command = json.loads(data)
              print(f'Command: {command}')
              if not valid_command(command):
                  print("Invalid command!")
              
            except Exception as e:
              print("Error reading JSON packet")
              print(e)
              # Need better error handling!
              
