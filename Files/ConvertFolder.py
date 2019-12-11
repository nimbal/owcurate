# ====================================================================================================
# ==================== THIS SCRIPT CONVERTS ALL GENEACTIV BIN FILES INTO EDF OF THE SAME FOLDER
# ==================== DAVID DING
# ==================== NEUROSCIENCE BALANCE AND MOBILITY LABORATORY
# ==================== UNIVERSITY OF WATERLOO
# ====================================================================================================

from Sensor.Sensor import *
from Files.Converters import *
from Device.GENEActiv import *
from Subject import *
from os import mkdir
input_dir = input()

out_dir = input()


files = [f for f in listdir(input_dir) if (isfile(join(input_dir, f)) and ".bin" in f)]
files.sort()

for f in files:
    curr = GENEActiv()
    curr.read_from_raw(join(input_dir, f))
    curr.calculate_time_shift()
    GENEActivToEDF(curr, out_dir)

