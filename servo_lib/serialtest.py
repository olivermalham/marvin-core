import serial

port = serial.Serial("/dev/serial0", 115200)

command = [0x55, 0x55, 0x05, 0x03, 0x17, 0xE0]

port.write(command)
port.flushInput()

while True:
    if port.in_waiting:
        print((port.read()), end=' ', flush=True)
