from Sensor.Sensor import *
from Files.Converters import *
from Device.GENEActiv import *
from Subject import *
from os import mkdir
input_dir = input()

out_dir = input()


files = [f for f in listdir(input_dir) if (isfile(join(input_dir, f)) and ".bin" in f)]
files.sort()

for f in files[:4]:
    curr = GENEActiv()
    curr.read_from_raw(join(input_dir, f))
    curr.calculate_time_shift()
    GENEActivToEDF(curr, out_dir)


'''
from Sensor.Sensor import *
from Files.Converters import *
from Device.GENEActiv import *
from Subject import *
from os import mkdir
OND05_2000 = Subject("/Users/nimbal/Document/OND05/ProcessedEDF/OND05_SAT_2000_01_GA_RAnkle", 2000)
OND05_2000.init_sensor("RA")
EDFToSensor(OND05_2000.Sensors["RA"], "/Users/nimbal/Documents/OND05/ProcessedEDF/OND05_SAT_2000_01_GA_RAnkle", "Accelerometer.EDF", "", "Thermometer.EDF", "", "")
OND05_2000.Sensors["RA"].accelerometer.calculate_svms()
OND05_2000.Sensors["RA"].non_wear_accel_temp(3, 4)




fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8), sharex=True)
ax1.plot(OND07_3001.Sensors["LA"].accelerometer.x, linewidth=0.7)
ax2.plot(OND07_3001.Sensors["RA"].accelerometer.x, linewidth=0.7)

ax3 = ax1.twinx()
ax4 = ax2.twinx()

ax4.plot([300 * i for i in range(len(OND07_3001.Sensors["RA"].thermometer.temperatures))], OND07_3001.Sensors["RA"].thermometer.temperatures, c="m", linewidth=0.8)
ax3.plot([300 * i for i in range(len(OND07_3001.Sensors["LA"].thermometer.temperatures))], OND07_3001.Sensors["LA"].thermometer.temperatures, c="m", linewidth=0.8)


for i in range(len(OND07_3001.Sensors["LA"].non_wear_starts)):
    ax1.axvline(OND07_3001.Sensors["LA"].non_wear_starts[i], -10, 10, c="green")
    ax1.axvline(OND07_3001.Sensors["LA"].non_wear_ends[i], -10, 10, c="red")

for i in range(len(OND07_3001.Sensors["RA"].non_wear_starts)):
    ax2.axvline(OND07_3001.Sensors["RA"].non_wear_starts[i], -10, 10, c="green")
    ax2.axvline(OND07_3001.Sensors["RA"].non_wear_ends[i], -10, 10, c="red")
'''
