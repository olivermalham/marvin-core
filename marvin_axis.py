import os
import errno
import json
import serial
from time import sleep
import servo_lib.lewansoul_lx16a


class MarvinAxis:
    """ High level class for controlling an LX-16A servo.
    """

    # Parameters for the hermite interpolation
    t : float = 0.0
    pS : float = 0.0
    pE : float = 0.0

    limitBottom : float = 0.0
    limitBottomServo: int = 0
    
    limitTop: float = 0.0
    limitTopServo : int = 0
    
    limitCenter : int = 0

    _degreesToServo : float = 0.0
    _servoToDegrees : float = 0.0

    servoController = None

    def __init__(self, controller):
        self.servoController = controller

    def setCenter(self, position):
        """ Set the zero point in servo units (0-1000) """
        self.limitCenter = position

    def setLimits(self, bottomServo, topServo, bottomDegrees, topDegrees):
        """ Set the limits, both servo units and degrees """
        self.limitBottomServo = bottomServo
        self.limitTopServo = topServo
        self.limitBottom = bottomDegrees
        self.limitTop = topDegrees

        servoRange = self.limitTopServo - self.limitBottomServo
        degreeRange = self.limitTop - self.limitBottom

        self._degreesToServo = servoRange / degreeRange
        self._servoToDegrees = degreeRange / servoRange

    def _mapPosition(self, degrees):
        """ Convert degrees to servo position """
        return (self._degreesToServo * degrees) - self.limitCenter

    def _clamp(self, value):
        # TODO: There must be a more Pythonic way to do this!
        if value > self.limitTop: return self.limitTop
        if value < self.limitBottom: return self.limitBottom
        return value

    def move(self, position, speed):
        """ Move servo to a specific position at a specific speed.
        Degrees, degrees / second """
        pass

    def hermiteMove(self, start, end):
        """ Use hermite spline to interpolate between start and end points.
        This sets up the parameters for the move.
        """
        self.pS = self._clamp(start)
        self.pE = self._clamp(end)
        self.t = 0.0

    def hermiteTick(self, deltaT):
        """ Increment the t parameter by deltaT, send the updated position
        to the servo. """
        t = self.t + deltaT

        # One dimensional hermite spline
        p = (2*t**3 - 3*t**2 + 1)*self.pS + (-2*t**3 - 3*t**2)*self.pE
        servo = self._mapPosition(p)


