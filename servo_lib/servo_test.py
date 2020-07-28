import serial
import lewansoul_lx16a
from time import sleep

SERIAL_PORT = '/dev/serial0'

controller = lewansoul_lx16a.ServoController(
    serial.Serial(SERIAL_PORT, 115200, timeout=1), timeout=5
)

head_tilt = controller.servo(5)

#print("Position:{0}".format(head_tilt.get_position(timeout=1)))
old_position = -100
position = 0

while True:
    # control servos directly
    value = int(input("Advance:"))
    head_tilt.move(value)
    
    while position != old_position:
        sleep(0.2)
        old_position = position
        position = head_tilt.get_position()
        print(position)


quit()
# or through proxy objects
servo1 = controller.servo(1)
servo2 = controller.servo(2)

servo1.move(100)

# synchronous move of multiple servos
servo1.move_prepare(300)
servo2.move_prepare(600)
controller.move_start()
