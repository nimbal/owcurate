# ====================================================================================================
# ==================== DAVID DING
# ==================== NEUROSCIENCE BALANCE AND MOBILITY LABORATORY
# ==================== UNIVERSITY OF WATERLOO
# ==================== PYTHON IMPLEMENTATION OF VAN HEES SLEEP DETECTION ALGORITHM WITHIN THE NIMBAL LAB
# ====================================================================================================


# ======================================== IMPORTS
from Files.Converters import *
from Sensor.Sensor import *
import matplotlib.pyplot as plt
from pandas.plotting import register_matplotlib_converters
import statistics
import math

register_matplotlib_converters()

# ======================================== VARIABLE DECLARATION AND INITIALIZATION
S = Sensor()

window_len = 375

rolling_x = []
rolling_y = []
rolling_z = []
angles = []
avg_angles = []
non_wear_starts = []
non_wear_ends = []
sleep_starts = []
sleep_ends = []

start_indices = []
end_indices = []

EDFToSensor(S, "/Users/nimbal/Documents/OND07/EDF/Accelerometer/OND07_WTL_3031_02_GA_LWrist_Accelerometer.EDF", "",
            "/Users/nimbal/Documents/OND07/EDF/Temperature/OND07_WTL_3031_02_GA_LWrist_Temperature.EDF",
            "/Users/nimbal/Documents/OND07/EDF/Light/OND07_WTL_3031_02_GA_LWrist_Light.EDF",
            "/Users/nimbal/Documents/OND07/EDF/Button/OND07_WTL_3031_02_GA_LWrist_Button.EDF")

times = S.generate_times(75, len(S.accelerometer.x))

print("Finding Median Values on windows")

for i in range(0, len(S.accelerometer.x) - window_len, 75):
    rolling_x.append(statistics.median(S.accelerometer.x[i: i + window_len]))
    rolling_y.append(statistics.median(S.accelerometer.y[i: i + window_len]))
    rolling_z.append(statistics.median(S.accelerometer.z[i: i + window_len]))
    print("%.5f" % (i / (len(S.accelerometer.x) - window_len)))

for i in range(len(rolling_x)):
    angles.append(
        math.atan(rolling_z[i] / math.sqrt(math.pow(rolling_x[i], 2) + math.pow(rolling_y[i], 2))) * 180 / math.pi)

for i in range(0, len(angles), 5):
    avg_angles.append(statistics.mean(angles[i:i + 5]))

angles_diff = np.diff(avg_angles)
angles_diff = np.append(angles_diff, 0)

i = 0
while i < len(angles_diff) - 1:
    if angles_diff[i] < 5:
        j = i
        while angles_diff[j] < 5 and j < len(angles_diff) - 1:
            j += 1
        if j - i > (5 * 60):
            start_indices.append(i * window_len)
            end_indices.append(j * window_len)
        i = j
    i += 1

fig, (ax1, ax2, ax3, ax4) = plt.subplots(4, 1, sharex=True)


ax1.plot(times, S.accelerometer.x)
ax2.plot([times[300 * i] for i in range(len(S.thermometer.temperatures) - 1)], S.thermometer.temperatures[:-1])


sleep_starts = []
sleep_ends = []

# Minimum sleep bout of 30 mins
for i in range(len(start_indices)):
    if end_indices[i] - start_indices[i] > (30 * 60 * 75):
        sleep_starts.append(start_indices[i])
        sleep_ends.append(end_indices[i])


# This is for the start and end periods
"""start = []
end = []
j = 0
for i in range(len(sleep_starts) - 1 - j):
    print(i)
    if sleep_starts[i+1] - sleep_ends[i] < (60 * 60 * 75):
        sleep_starts.remove(sleep_starts[i+1])
        sleep_ends.remove(sleep_ends[i])
        j += 1
        i -= 1"""


for i in range(len(start_indices)):
    start_index = start_indices[i] // 300
    end_index = start_index + 75  # 75 DERIVED FROM N_MINS * SECONDS_PER_MIN * SAMPLES_PER_SECOND // 300
    indices = np.array([j for j in range(start_index, end_index)])
    curr_temps = np.array(S.thermometer.temperatures[start_index:end_index])
    m = (statistics.mean(curr_temps) * statistics.mean(indices) - statistics.mean(curr_temps * indices))
    ax2.plot(times[start_index * 300], S.thermometer.temperatures[start_index], "m.")
    ax2.plot(times[end_index * 300], S.thermometer.temperatures[end_index], "g.")

    if m > 8.75:
        non_wear_starts.append(start_indices[i])
        non_wear_ends.append(end_indices[i])
    else:
        sleep_starts.append(start_indices[i])
        sleep_ends.append(end_indices[i])


for i in non_wear_starts:
    ax3.axvline(times[i], -10, 10, color='black')

for i in non_wear_ends:
    ax3.axvline(times[i], -10, 10, color="red")

