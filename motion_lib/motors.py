import serial

class WheelIO:

    def __init__(self):
        pass

    def update_motors(self, command):
        """ Send motor control commands to the Arduino Nanos that drive the motors
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

        print(f"Command_left: {command_left}")
        print(f"Command_right: {command_right}")
