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
    if len(sys.argv) == 2:
        target_id = int(sys.argv[1])
    else:
        quit()
    
    print("--------------------------------------")
    print("Connecting to servo...", end='', flush=True)
            
    servo_id = controller.get_servo_id(target_id)

    if servo_id is None:
        print("No servo found.")
        quit()

    print(servo_id)

    print("--------------------------------------")
    print(" Configuration")
    print("--------------------------------------")
    print("Mode: \t\t\t {}".format(controller.get_mode(servo_id)))
    print("Move Limits: \t\t {}".format(controller.get_position_limits(servo_id)))
    print("Move offset: \t\t {}".format(controller.get_position_offset(servo_id)))
    print("Volt Limits: \t\t {}".format(controller.get_voltage_limits(servo_id)))
    print("Max Temp: \t\t {}".format(controller.get_max_temperature_limit(servo_id)))
    print("--------------------------------------")
    print(" Current Status")
    print("--------------------------------------")
    print("Position: \t\t {}".format(controller.get_position(servo_id)))
    print("Supply Voltage: \t {}".format(controller.get_voltage(servo_id)))
    print("Temperature: \t\t {}".format(controller.get_temperature(servo_id)))
    print("Speed: \t\t\t {}".format(controller.get_motor_speed(servo_id)))
    print("--------------------------------------")

