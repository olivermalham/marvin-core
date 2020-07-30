#!/usr/bin/python3

import os
import errno
import json
import serial
from time import sleep
import servo_lib.lewansoul_lx16a

BASE_DIR = '/etc/marvin/'
MOTION_FIFO = 'motion'

# UART serial port for servo bus
SERIAL_PORT = '/dev/serial0'

# USB serial ports for Arduino Nanos that control left and right side motors
left_motor_path = '/dev/ttyUSB0'
right_motor_path = '/dev/ttyUSB1'

valid_attributes = ["wheel", "head"]

servo_controller = servo_lib.lewansoul_lx16a.ServoController(
        serial.Serial(SERIAL_PORT, 115200, timeout=0.2), 
        timeout=0.5
)


"""
Note that the wheels are numbered front to back, odd on the left, even on the right.
Wheel array *must* have exactly six entries.
Speed is between 0 and 1.0, and is treated as a fraction of the maximum speed.
All directions are 0 for straight foward, positive for right, negaive for left.
Positive head pitch is up.

We're assuming that the wheel servo IDs match the numbering described above. Head yaw will have ID 7, pitch 8.
"""


def update_motors(command):
    """ Send motor control commands to the Ardunio Nanos
    """
    command_left = ""
    command_right = ""

    for index, wheel in enumerate(command["wheel"]):
        if index % 2:
            command_left = f"{command_left},{wheel['distance']},{wheel['speed']}"
        else:
            command_right = f"{command_right},{wheel['distance']},{wheel['speed']}"

    command_left = command_left[1:]
    command_right = command_right[1:]

    print(f"Motors left: {command_left}")
    print(f"Motors right: {command_right}")


def update_servos(command):
    """ Send servo commands
    """
    for index, wheel in enumerate(command["wheel"]):
        position = int(wheel["angle"])
        servo_id = index + 1
        print(f"Servo {servo_id}: {position}; ", end='')
        servo_controller.move(servo_id, position)
    print('')
        

def servos_ready(command):
    """ Return true is all the servos are within an error factor
    """

    for index, wheel in enumerate(command["wheel"]):
        position = servo_controller.get_position(index + 1)
        if abs(position - wheel["angle"]) > servo_error:
            return False
    return True


def motors_ready(command):
    """ Return true if the motors have moved the target distance
    """
    return True


def valid_command(command):
    """ Check the received JSON matches what we expect
    """
    for key in command:
        if key not in valid_attributes:
            return False
    return True


if __name__ == "__main__":
    print(f"Listening to motion FIFO on {BASE_DIR}{MOTION_FIFO}...")
    while True:
        with open(BASE_DIR+MOTION_FIFO) as fifo:
            print(f"FIFO opened")
            while True:
                data = fifo.read()
                if len(data) == 0:
                    print("Client disconnected")
                    print("")
                    break
                try:
                    command = json.loads(data)
                    if not valid_command(command):
                        print("Invalid command!")
                    update_motors(command)
                    update_servos(command)
                    while not servos_ready(command) and not motors_ready(command):
                        sleep(0.2)

                except Exception as e:
                    print("Error reading JSON packet")
                    print(repr(e))
                    # Need better error handling!
            

