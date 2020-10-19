#!/usr/bin/python3

import os
import errno
import json
import serial
from time import sleep
import servo_lib.lewansoul_lx16a

BASE_DIR = '/etc/marvin/'
MOTION_FIFO = 'motion'
SENSORS_FIFO = 'sensors'

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

# Allowable absolute difference between commanded position and actual position when stopped
servo_error = 10


"""
Note that the wheels are numbered front to back, odd on the left, even on the right.
- Wheel array *must* have exactly six entries.
- Angle values for wheels 3 and 4 are ignored (as they don't steer)
- Speed is between 0 and 1.0, and is treated as a fraction of the maximum speed.
- All directions are 0 for straight foward, positive for right, negaive for left.
- Positive head pitch is up.

We're assuming that the wheel servo IDs match the numbering described above. Head yaw will have ID 5, pitch 6.
"""

class servo_feedback(object):
    position = 0
    id = 0
    
    def __init__(self):
        pass


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
    print(command)

    servo_controller.move(1, command["wheel"][0]["angle"])
    sleep(0.1)
    servo_controller.move(2, command["wheel"][1]["angle"])
    sleep(0.1)
    servo_controller.move(3, command["wheel"][4]["angle"])
    sleep(0.1)
    servo_controller.move(4, command["wheel"][5]["angle"])
    sleep(0.1)
    
    servo_controller.move(5, command["head"]["yaw"])
    sleep(0.1)
    servo_controller.move(6, command["head"]["pitch"])
    sleep(0.1)
    print('')
        

def servos_ready(command):
    """ Return true if all the servos are within an error factor
    """

    sleep(0.1)
    position = servo_controller.get_position(1)
    if abs(position - command["wheel"][0]["angle"]) > servo_error:
        return False

    sleep(0.1)
    position = servo_controller.get_position(2)
    if abs(position - command["wheel"][1]["angle"]) > servo_error:
        return False

    sleep(0.1)
    position = servo_controller.get_position(3)
    if abs(position - command["wheel"][4]["angle"]) > servo_error:
        return False

    sleep(0.1)
    position = servo_controller.get_position(4)
    if abs(position - command["wheel"][5]["angle"]) > servo_error:
        return False

    sleep(0.1)
    position = servo_controller.get_position(5)
    if abs(position - command["head"]["yaw"]) > servo_error:
        return False

    sleep(0.1)
    position = servo_controller.get_position(6)
    if abs(position - command["head"]["pitch"]) > servo_error:
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
    print(f"Listening to motion FIFO on {BASE_DIR}{MOTION_FIFO}...", end="")
    input_fifo_fd = os.open(BASE_DIR+MOTION_FIFO, os.O_RDONLY | os.O_NONBLOCK)
    input_fifo = os.fdopen(input_fifo_fd)
    print("OK")
    
#    print(f"Opening sensor FIFO on {BASE_DIR}{SENSORS_FIFO}...", end="")
#    output_fifo = open(BASE_DIR+SENSORS_FIFO, 'w')
#    print("OK")

    i = 0

    while True:
#        try:
#            output_fifo.write(f"TEST {i}")
#            output_fifo.flush()
#            os.fsync(output_fifo.fileno())
#            i = i + 1
#        except:
#            pass

        data = input_fifo.readline()
        if len(data) == 0:
            sleep(0.2)
            continue
        try:
            command = json.loads(data)
            if not valid_command(command):
                print("Invalid command!")
            update_motors(command)
            update_servos(command)
            while not servos_ready(command) and not motors_ready(command):
                pass

        except Exception as e:
            print("Error reading JSON packet")
            print(repr(e))
            # Need better error handling!
            

