# ====================================================================================================
# ==================== THIS SCRIPT WAS MADE TO TEST METHODS OF NON-WEAR ALGORITHMS ON REAL DATA
# ==================== DAVID DING
# ==================== NEUROSCIENCE BALANCE AND MOBILITY LAB
# ==================== UNIVERSITY OF WATERLOO
# ====================================================================================================

# ======================================== IMPORTS ========================================
from Backups.Converters import *
from Sensor.Sensor import *
import datetime
from pandas.plotting import register_matplotlib_converters
import seaborn as sns

# ======================================== INITIALIZATION ========================================
register_matplotlib_converters()

# ======================================== Four Sensor Objects, one representing each attached device
LW = Sensor()
RW = Sensor()
LA = Sensor()
RA = Sensor()

# ======================================== Getting the ID and trial numbers
subject_ID = input()
trial_num = input()

t0 = datetime.datetime.now()
# ======================================== Getting input (Reading Files)
print(" ======================================== READING FILES ========================================")
EDFToSensor(LA, "/Users/nimbal/Documents/OND07/EDF/Accelerometer/OND07_WTL_%s_%s_GA_LAnkle_Accelerometer.EDF"
            % (subject_ID, trial_num), "",
            "/Users/nimbal/Documents/OND07/EDF/Temperature/OND07_WTL_%s_%s_GA_LAnkle_Temperature.EDF"
            % (subject_ID, trial_num),
            "/Users/nimbal/Documents/OND07/EDF/Light/OND07_WTL_%s_%s_GA_LAnkle_Light.EDF"
            % (subject_ID, trial_num),
            "/Users/nimbal/Documents/OND07/EDF/Button/OND07_WTL_%s_%s_GA_LAnkle_Button.EDF"
            % (subject_ID, trial_num))

EDFToSensor(RA, "/Users/nimbal/Documents/OND07/EDF/Accelerometer/OND07_WTL_%s_%s_GA_RAnkle_Accelerometer.EDF"
            % (subject_ID, trial_num), "",
            "/Users/nimbal/Documents/OND07/EDF/Temperature/OND07_WTL_%s_%s_GA_RAnkle_Temperature.EDF"
            % (subject_ID, trial_num),
            "/Users/nimbal/Documents/OND07/EDF/Light/OND07_WTL_%s_%s_GA_RAnkle_Light.EDF"
            % (subject_ID, trial_num),
            "/Users/nimbal/Documents/OND07/EDF/Button/OND07_WTL_%s_%s_GA_RAnkle_Button.EDF"
            % (subject_ID, trial_num))

EDFToSensor(LW, "/Users/nimbal/Documents/OND07/EDF/Accelerometer/OND07_WTL_%s_%s_GA_LWrist_Accelerometer.EDF"
            % (subject_ID, trial_num), "",
            "/Users/nimbal/Documents/OND07/EDF/Temperature/OND07_WTL_%s_%s_GA_LWrist_Temperature.EDF"
            % (subject_ID, trial_num),
            "/Users/nimbal/Documents/OND07/EDF/Light/OND07_WTL_%s_%s_GA_LWrist_Light.EDF"
            % (subject_ID, trial_num),
            "/Users/nimbal/Documents/OND07/EDF/Button/OND07_WTL_%s_%s_GA_LWrist_Button.EDF"
            % (subject_ID, trial_num))

EDFToSensor(RW, "/Users/nimbal/Documents/OND07/EDF/Accelerometer/OND07_WTL_%s_%s_GA_RWrist_Accelerometer.EDF"
            % (subject_ID, trial_num), "",
            "/Users/nimbal/Documents/OND07/EDF/Temperature/OND07_WTL_%s_%s_GA_RWrist_Temperature.EDF"
            % (subject_ID, trial_num),
            "/Users/nimbal/Documents/OND07/EDF/Light/OND07_WTL_%s_%s_GA_RWrist_Light.EDF"
            % (subject_ID, trial_num),
            "/Users/nimbal/Documents/OND07/EDF/Button/OND07_WTL_%s_%s_GA_RWrist_Button.EDF"
            % (subject_ID, trial_num))
t1 = datetime.datetime.now()

print("Finished Reading Files Took {} Seconds".format((t1-t0).seconds))


# ======================================== PROCESSING ========================================
# ======================================== Generating Values that are needed for further processing
print(" ======================================== GENERATING TIMES ========================================")
LA_TIMES = LA.generate_times(LA.accelerometer.frequency, len(LA.accelerometer.x))
RA_TIMES = RA.generate_times(RA.accelerometer.frequency, len(RA.accelerometer.x))
LW_TIMES = LW.generate_times(LW.accelerometer.frequency, len(LW.accelerometer.x))
RW_TIMES = RW.generate_times(RW.accelerometer.frequency, len(RW.accelerometer.x))
t2 = datetime.datetime.now()
print("Finished Generating Times, Took {} Seconds".format((t2 - t1).seconds))

print(" ======================================== CALCULATING SVMS ======================================== ")
LA.accelerometer.calculate_svms()
LW.accelerometer.calculate_svms()
RA.accelerometer.calculate_svms()
RW.accelerometer.calculate_svms()
t3 = datetime.datetime.now()
print("Finished Calculating SVMs, Took {} Seconds".format((t3 - t2).seconds))

# Checking for NonWear
print(" ======================================== LEFT WRIST NONWEAR ========================================")
LW.NonWear()
LW.Check_Temperature()
t4 = datetime.datetime.now()
print("Finished Left Wrist Nonwear, Took {} Seconds".format((t4 - t3).seconds))

print(" ======================================== RIGHT WRIST NONWEAR ========================================")
RW.NonWear()
RW.Check_Temperature()
t5 = datetime.datetime.now()
print("Finished Right Wrist Nonwear, Took {} Seconds".format((t5 - t4).seconds))

print(" ======================================== LEFT ANKLE NONWEAR ========================================")
LA.NonWear()
LA.Check_Temperature()
t6 = datetime.datetime.now()
print("Finished Left Ankle Nonwear, Took {} Seconds".format((t6 - t5).seconds))

print(" ======================================== RIGHT ANKLE NONWEAR ========================================")
RA.NonWear()
RA.Check_Temperature()
t7 = datetime.datetime.now()
print("Finished Right Ankle Nonwear, Took {} Seconds".format((t7 - t6).seconds))

print(" ======================================== DONE ========================================")


# ======================================== OUTPUT ========================================
# ======================================== Displaying information Graphically
sns.set()
fig, (ax1, ax2, ax3, ax4) = plt.subplots(4, 1, sharex=True)
ax1.plot(LW_TIMES[::2], LW.accelerometer.svms[::2])
ax2.plot(RW_TIMES[::2], RW.accelerometer.svms[::2])

ax3.plot(LA_TIMES[::2], LA.accelerometer.svms[::2])
ax4.plot(RA_TIMES[::2], RA.accelerometer.svms[::2])


for i in LW.non_wear_starts:
    ax1.axvline(LW_TIMES[i], color='black')
for i in LW.non_wear_ends:
    ax1.axvline(LW_TIMES[i], color='red')

for i in RW.non_wear_starts:
    ax2.axvline(RW_TIMES[i], color='black')
for i in RW.non_wear_ends:
    ax2.axvline(RW_TIMES[i], color='red')

for i in LA.non_wear_starts:
    ax3.axvline(LA_TIMES[i], color='black')
for i in LA.non_wear_ends:
    ax3.axvline(LA_TIMES[i], color='red')

for i in RA.non_wear_starts:
    ax4.axvline(RA_TIMES[i], color='black')
for i in RA.non_wear_ends:
    ax4.axvline(RA_TIMES[i], color='red')


ax1.set_title("Left Wrist")
ax2.set_title("Right Wrist")
ax3.set_title("Left Ankle")
ax4.set_title("Right Ankle")

fig.autofmt_xdate()
fig.tight_layout()

t8 = datetime.datetime.now()

print("Finished Plotting, Took {} Seconds".format((t8 - t7).seconds))

print("Total Time: {} Seconds".format((t8 - t0).seconds))


