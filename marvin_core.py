import os
import errno
import json
import serial
from time import sleep
import servo_lib.lewansoul_lx16a
from typing import List, NamedTuple
from dataclasses import dataclass


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

    currentState = MarvinState(servos=[ServoState()]*6, motors=[MotorState()]*6, sensors=[])
    targetState = MarvinState(servos=[ServoState()]*6, motors=[MotorState()]*6, sensors=[])


    def __init__(self, servoController):
        self.servoController = servoController

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
        # TODO: Finish me!
        print(f"Action Turn: angle {angle}, speed: {speed}")

    def action_head(self, pitch, yaw):
        # TODO: Finish me!
        print(f"Action Head: pitch {pitch}, yaw: {yaw}")

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

        self.servoController.move(1, self.targetState.servos[0].angle)
        sleep(0.02)
        self.servoController.move(2, self.targetState.servos[1].angle)
        sleep(0.02)
        self.servoController.move(3, self.targetState.servos[2].angle)
        sleep(0.02)
        self.servoController.move(4, self.targetState.servos[3].angle)
        sleep(0.02)
        self.servoController.move(5, self.targetState.servos[4].angle)
        sleep(0.02)
        self.servoController.move(6, self.targetState.servos[5].angle)
        sleep(0.02)

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

