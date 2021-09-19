# Unit tests for the marvin_core class
from marvin_core import MarvinCore
from pprint import pprint
import unittest
from unittest.case import skip


class TestMarvinCore(unittest.TestCase):
    """ Test core marvin control class operations. """
    
    fullPacket : str = ""
    movePacket : str = ""
    turnPacket : str = ""
    headPacket : str = ""
    actionPacket : str = ""

    unknownAction : str = ""
    wrongParams : str = ""


    def setUp(self) -> None:
        return super().setUp()

    def tearDown(self) -> None:
        return super().tearDown()

    def test_getCommandMethod(self):
        core = MarvinCore()
        self.assertTrue(callable(core.getCommandMethod("move")))    