# DAVID DING
# THIS CLASS IS SPECIFIC TO THE NIMBAL LAB


# ======================================== IMPORTS ========================================
from Sensor import *


class Subject:
    def __init__(self):
        self.path = None
        self.id = None
        self.Sensors = {}

    def set_subject_id(self, subjID):
        self.id = subjID

    def set_path(self, path):
        self.path = path

    def init_sensor(self, sensor_name):
        self.Sensors.update({sensor_name: Sensor()})


