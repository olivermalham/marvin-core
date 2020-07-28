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

servos = {}
sleep(1)

if __name__ == '__main__':
    print("Searching for servos", flush=True)
    for search_id in range(255):
        try:
            servo = controller.servo(search_id)
            servo.get_servo_id(search_id)
            servo_id = search_id
            servos[search_id] = servo
            print(search_id, end='', flush=True)
        except lewansoul_lx16a.TimeoutError as e:
            print(".", end='', flush=True)
        except KeyboardInterrupt:
            print("\nExiting")
            quit()

