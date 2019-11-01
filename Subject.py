# DAVID DING
# THIS CLASS IS SPECIFIC TO THE NIMBAL LAB


# ======================================== IMPORTS ========================================
from Device.GENEActiv import *
from Device.Bittium import *

class Subject:
    def __init__(self, path, subjectID):
        self.path = path
        self.id = subjectID
        LA_file = input("Input Left Ankle File")
        self.LA = GENEActiv()
