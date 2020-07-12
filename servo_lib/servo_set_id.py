import sys
import serial
import lewansoul_lx16a
from time import sleep

SERIAL_PORT = '/dev/serial0'

controller = lewansoul_lx16a.ServoController(
    serial.Serial(SERIAL_PORT, 115200, timeout=0.5), timeout=1
)

new_id = 42
servo_id = None
servo = None


if __name__ == '__main__':
    new_id = int(sys.argv[1])
    print("Searching for servo", end='', flush=True)
    for search_id in range(255):
        try:
            servo = controller.servo(search_id)
            servo.get_servo_id(search_id)
            servo_id = search_id
            break
        except lewansoul_lx16a.TimeoutError as e:
            print(".", end='', flush=True)

    if servo_id is None:
        print("No servo found.")
        quit()

    print(f"Servo found with id of {servo_id}. Updating to {new_id}")
    servo.set_servo_id(servo_id, new_id)

    quit()

