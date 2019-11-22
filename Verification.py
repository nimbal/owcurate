# File to run QA on the raw file and the edf file


from Files.Converters import *
from Device.GENEActiv import *
from os import listdir
from os.path import join, isfile


raw = GENEActiv()
edf = GENEActiv()

input_dir = "/Users/nimbal/Documents/OND05/RawData"

accel_dir = "/Users/nimbal/Documents/OND05/GENEActiv/Accelerometer"
temp_dir = "/Users/nimbal/Documents/OND05/GENEActiv/Temperature"
light_dir = "/Users/nimbal/Documents/OND05/GENEActiv/Light"
button_dir = "/Users/nimbal/Documents/OND05/GENEActiv/Button"

files = [f for f in listdir(input_dir) if (isfile(join(input_dir, f)) and ".bin" in f)]
files.sort()

for f in files:
    raw.read_from_raw(join(input_dir, f))
    EDFToSensor(edf, "%s/%s_Accelerometer.EDF" % (accel_dir, f[:-4]), "", "%s/%s_Temperature.EDF" % (temp_dir, f[:-4]),
                "%s/%s_Light.EDF" % (light_dir, f[:-4]), "%s/%s_Button.EDF" % (button_dir, f[:-4]))






