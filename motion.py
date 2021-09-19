#!/usr/bin/python3

from marvin_core import MarvinCore
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


# servo_controller = servo_lib.lewansoul_lx16a.ServoController(
#         serial.Serial(SERIAL_PORT, 115200, timeout=0.2), 
#         timeout=0.5
# )

class MockServoController:
    def move(self, servo, position):
        print(f"move {servo} to {position}")
    def get_position(self, servo):
        return 500

servo_controller = MockServoController()

if __name__ == "__main__":
    
    # TODO: Update so that this doesn't block if there is no one on the other end of the pipe
    print(f"Listening to motion FIFO on {BASE_DIR}{MOTION_FIFO}...", end="")
    input_fifo_fd = os.open(BASE_DIR+MOTION_FIFO, os.O_RDONLY | os.O_NONBLOCK)
    input_fifo = os.fdopen(input_fifo_fd)
    print("OK")

    # TODO: Don't block if there is no one on the other end of the pipe
#    print(f"Opening sensor FIFO on {BASE_DIR}{SENSORS_FIFO}...", end="")
#    output_fifo = open(BASE_DIR+SENSORS_FIFO, 'w')
#    print("OK")

    i = 0

    core = MarvinCore(servo_controller)

    try:
        while True:
            # TODO: Need to figure out how to read in sensor data here, in a way that does not block the loop
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
                print("--------------------------------------------------------------")
                print(f"Executing: {data}")
                core.execute(data)
            except Exception as e:
                # TODO: Need better error handling!
                print("Error processing JSON packet")
                print(repr(e))
                print(data)
    finally:
        print("\nClosing FIFO")
        input_fifo.close()
        quit()
