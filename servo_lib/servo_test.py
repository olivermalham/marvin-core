import sys
import serial
import lewansoul_lx16a
from time import sleep

SERIAL_PORT = '/dev/serial0'

controller = lewansoul_lx16a.ServoController(
    serial.Serial(SERIAL_PORT, 115200, timeout=1), timeout=5
)

if __name__ == '__main__':
    servo_id = int(sys.argv[1])

    servo = controller.servo(servo_id)
    if servo.get_servo_id() is None:
        print(f"Failed to connect to servo {servo_id}")
        quit()

    print(f"Connected to servo {servo_id}")
    old_position = servo.get_position(timeout=1)
    
    print(f"Current position:{old_position}")
    position = 0

    while True:
        # control servos directly
        target = input("Target: ")
        if target == "q":
            print("Quitting")
            quit()
        if target == "p":
            position = servo.get_position()
            print(f"Position: {position}", flush=True)
        else:
            servo.move(int(target), 1500)
            sleep(2.0)
            position = servo.get_position()
            print(f"Position: {position}", flush=True)
 
