from Sensor.Accelerometer import *
from Sensor.Thermometer import *


class Sensor():
    def __init__(self):
        self.metadata = {}
        self.accelerometer = None
        self.thermometer = None
        self.ecg = None
        self.light = None
        self.button = None

    def init_accelerometer(self):
        self.accelerometer = Accelerometer()

    def init_thermometer(self):
        self.thermometer = Thermometer()

