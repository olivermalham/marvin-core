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
    print("Searching for servo...", end='', flush=True)
            
    # Find what ever servo is currently on the bus
    servo_id = controller.get_servo_id()

    if servo_id is None:
        print("No servo found.")
        quit()

    print(servo_id)

    if input("Continue? (Y/n)") == "Y":

        print(f"Servo found with id of {servo_id}. Updating to {new_id}")
        controller.set_servo_id(servo_id, new_id)

        quit()

