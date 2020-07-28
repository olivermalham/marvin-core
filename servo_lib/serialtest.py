import serial
from time import sleep

port = serial.Serial("/dev/serial0", 115200)

command = [0x55, 0x55, 0x05, 0x03, 0x0E, 0xE9]

port.write(command)

print("In buffer: {0}".format(port.in_waiting))

for byte in command:
    port.read()

while True:
    if port.in_waiting:
        print((port.read()), end=' ', flush=True)
