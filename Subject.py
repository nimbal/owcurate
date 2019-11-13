# DAVID DING
# THIS CLASS IS SPECIFIC TO THE NIMBAL LAB


# ======================================== IMPORTS ========================================
from Device.GENEActiv import *
from Device.Bittium import *
from Sensor.Sensor import *


class Subject:
    def __init__(self, path, subjectID):
        self.path = path
        self.id = subjectID
        self.Sensors = {}

    def init_sensor(self, sensor_name):
        self.Sensors.update({sensor_name: Sensor()})


