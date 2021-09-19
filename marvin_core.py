import json
import serial
from time import sleep
import servo_lib.lewansoul_lx16a
from typing import List
from dataclasses import dataclass
from pprint import pprint


@dataclass
class ServoState:
    angle: float = 0.0


@dataclass
class MotorState:
    distance: float = 0.0
    speed: float = 0.0


@dataclass
class MarvinState:
    servos : List[ServoState]
    motors : List[MotorState]
    sensors : List[str] # TODO: Don't know about this yet


class MarvinCore:
    """ Core code that handles directly interfacing with Marvin's low level hardware. 
    Comunicates with higher level systems via a pair of FIFOs. Low level comms is via serial ports. """
    
    servoController = None

    # Allowable absolute difference between commanded position and actual position when stopped
    servo_tolerance = 10

    # Hard coded for now - angle the steering wheels need to be at in order to turn on the spot.
    turn_angle = 45.0  # TODO: Calculate!

    def __init__(self, servoController):
        self.servoController = servoController
        self.currentState = MarvinState(servos=[ServoState(), ServoState(), ServoState(), ServoState(), ServoState(), ServoState()], 
                                       motors=[MotorState(), MotorState(), MotorState(), MotorState(), MotorState(), MotorState()], sensors=[])
        self.targetState = MarvinState(servos=[ServoState(), ServoState(), ServoState(), ServoState(), ServoState(), ServoState()], 
                                       motors=[MotorState(), MotorState(), MotorState(), MotorState(), MotorState(), MotorState()], sensors=[])

    def execute(self, commandString):
        """ Executes the json encoded command string. Uses introspection, requires action names in the JSON to
        have a matching self.action_XXXX method or an exception is thrown.
        """
        packet = json.loads(commandString)
        
        for action in packet:
            getattr(self, "action_"+action)(**packet[action])

    def action_move(self, distance, speed):
        print(f"Action Move: distance {distance}, speed: {speed}")

        for motor in self.targetState.motors:
            motor.distance = distance
            motor.speed = speed

        for servo in self.targetState.servos[:4]:
            servo.angle = 0.0

        self.update_servos()
        self.update_motors()

    def action_turn(self, angle, speed):
        print(f"Action Turn: angle {angle}, speed: {speed}")

        for motor in self.targetState.motors:
            motor.distance = 0.0
            motor.speed = speed

        # TODO: Need to calculate all of this, after measuring wheel base etc
        self.targetState.motors[0].distance = 0
        self.targetState.motors[0].speed = 0

        self.targetState.motors[1].distance = 0
        self.targetState.motors[1].speed = 0

        self.targetState.motors[2].distance = 0
        self.targetState.motors[2].speed = 0

        self.targetState.motors[3].distance = 0
        self.targetState.motors[3].speed = 0

        self.targetState.motors[4].distance = 0
        self.targetState.motors[4].speed = 0

        self.targetState.motors[5].distance = 0
        self.targetState.motors[5].speed = 0

        self.targetState.servos[0].angle = self.turn_angle
        self.targetState.servos[1].angle = -self.turn_angle
        self.targetState.servos[2].angle = self.turn_angle
        self.targetState.servos[3].angle = -self.turn_angle

        self.update_servos()
        self.update_motors()

    def action_head(self, pitch, yaw):
        print(f"Action Head: pitch {pitch}, yaw: {yaw}")
        self.targetState.servos[4] = yaw
        self.targetState.servos[5] = pitch
        self.update_servos()

    def action_action(self, command):
        # TODO: Finish me!
        print(f"Action Command: {command}")

    def update_motors(self):
        """ Send motor control commands to the controller on the serial port
            
            MOVE Command
            Format:
            MOVE:D<motor 1 distance>,V<motor 1 velocity>....D<motor 6 distance>,V<motor 6 velocity>;
            e.g.
            MOVE:D0.0,V0.0,D1.0,V1.0,D2.0,V2.0,D3.0,V3.0,D4.0,V4.0,D5.0,V5.0
        """
        
        command = "MOVE:"
        for motor in self.targetState.motors:
            command = command + f"D{motor.distance},V{motor.speed},"
        command = command[:-1]

        # TODO: send to the controller via serial port
        print(command)

    def update_servos(self):
        """ Send servo commands so that the current state matches the target state
        """
        print(f"Target state:\n {self.targetState}")
        # for servo in range[6]:
        #     self.servoController.move(servo, self.targetState.servos[servo].angle)
        #     sleep(0.2)

    def servos_ready(self):
        """ Return true if all the servos are within an error factor
        """
        sleep(0.1)
        position = self.servoController.get_position(1)
        if abs(position - self.targetState.servos[0].angle) > self.servo_tolerance:
            return False

        sleep(0.1)
        position = self.servo_controller.get_position(2)
        if abs(position - self.targetState.servos[0].angle) > self.servo_tolerance:
            return False

        sleep(0.1)
        position = self.servo_controller.get_position(3)
        if abs(position - self.targetState.servos[0].angle) > self.servo_tolerance:
            return False

        sleep(0.1)
        position = self.servo_controller.get_position(4)
        if abs(position - self.targetState.servos[0].angle) > self.servo_tolerance:
            return False

        sleep(0.1)
        position = self.servo_controller.get_position(5)
        if abs(position - self.targetState.servos[0].angle) > self.servo_tolerance:
            return False

        sleep(0.1)
        position = self.servo_controller.get_position(6)
        if abs(position - self.targetState.servos[0].angle) > self.servo_tolerance:
            return False

        return True

    def motors_ready(command):
        """ Return true if the motors have moved the target distance
        """
        return True

