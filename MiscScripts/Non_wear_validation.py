# ====================================================================================================
# ==================== THIS SCRIPT WAS MADE TO TEST VARIOUS METHODS OF NON-WEAR ALGORITHMS TOGETHER
# ==================== DAVID DING
# ==================== NEUROSCIENCE BALANCE AND MOBILITY LAB
# ==================== UNIVERSITY OF WATERLOO
# ====================================================================================================
from Files.Converters import *
from Sensor.Sensor import *
import datetime
from pandas.plotting import register_matplotlib_converters
import seaborn as sns
from matplotlib import style

# ======================================== INITIALIZING CONSTANTS AND VARIABLES
register_matplotlib_converters()
S = Sensor()
EDFToSensor(S, "/Users/nimbal/Desktop/Accelerometer/KW_NW_Validation_RW_Accelerometer.EDF", "",
            "/Users/nimbal/Desktop/Temperature/KW_NW_Validation_RW_Temperature.EDF",
            "/Users/nimbal/Desktop/Light/KW_NW_Validation_RW_Light.EDF",
            "/Users/nimbal/Desktop/Button/KW_NW_Validation_RW_Button.EDF")

TIMES = S.generate_times(75, len(S.accelerometer.x))

# ======================================== ARRAY OF ITEMS TO BE COMPARED AGAINST
ACTUAL_NON_WEAR_STARTS = [datetime.datetime(year=2019, month=11, day=18, hour=11, minute=37, second=35),
                          datetime.datetime(year=2019, month=11, day=18, hour=15, minute=55, second=46),
                          datetime.datetime(year=2019, month=11, day=18, hour=19, minute=42, second=22),
                          datetime.datetime(year=2019, month=11, day=18, hour=21, minute=23, second=14),
                          datetime.datetime(year=2019, month=11, day=19, hour=10, minute=24, second=54),
                          datetime.datetime(year=2019, month=11, day=19, hour=14, minute=59, second=10),
                          datetime.datetime(year=2019, month=11, day=19, hour=16, minute=44, second=30)]

ACTUAL_NON_WEAR_ENDS = [datetime.datetime(year=2019, month=11, day=18, hour=11, minute=54, second=59),
                        datetime.datetime(year=2019, month=11, day=18, hour=16, minute=50, second=33),
                        datetime.datetime(year=2019, month=11, day=18, hour=20, minute=5, second=21),
                        datetime.datetime(year=2019, month=11, day=19, hour=7, minute=18, second=53),
                        datetime.datetime(year=2019, month=11, day=19, hour=12, minute=41, second=36),
                        datetime.datetime(year=2019, month=11, day=19, hour=15, minute=34, second=13),
                        datetime.datetime(year=2019, month=11, day=19, hour=23, minute=2, second=2)]

# ======================================== COMPARISON OF VAN HEES AND DING ALGORITHMS
S.accelerometer.calculate_svms()

# Using VanHees without temperature checking
S.VanHeesNonWear()
S.Check_Temperature()
VanHeesStarts_NT = S.start_indices
VanHeesEnds_NT = S.end_indices
VanHeesStarts_T = S.non_wear_starts
VanheesEnds_T = S.non_wear_ends


S.NonWear()
S.Check_Temperature()
DingStarts_NT = S.start_indices
DingEnds_NT = S.end_indices
DingStarts_T = S.non_wear_starts
DingEnds_T = S.non_wear_ends


sns.set()
fig, ((ax1, ax2), (ax3, ax4), (ax5, ax6)) = plt.subplots(3, 2, figsize=(12, 8), sharex=True)

ax1.plot(TIMES, S.accelerometer.svms)
ax2.plot(TIMES, S.accelerometer.svms)

for i in ACTUAL_NON_WEAR_STARTS:
    ax1.axvline(i, color='black')
    ax2.axvline(i, color='black')

for i in ACTUAL_NON_WEAR_ENDS:
    ax1.axvline(i, color='red')
    ax2.axvline(i, color='red')


for i in VanHeesStarts_NT:
    ax3.axvline(TIMES[i], color='black')
for i in VanHeesEnds_NT:
    ax3.axvline(TIMES[i], color='red')
for i in VanHeesStarts_T:
    ax5.axvline(TIMES[i], color='black')
for i in VanheesEnds_T:
    ax5.axvline(TIMES[i], color='red')


for i in DingStarts_NT:
    ax4.axvline(TIMES[i], color='black')
for i in DingEnds_NT:
    ax4.axvline(TIMES[i], color='red')
for i in DingStarts_T:
    ax6.axvline(TIMES[i], color='black')
for i in DingEnds_T:
    ax6.axvline(TIMES[i], color='red')


ax1.set_title("Van Hees Algorithm")
ax2.set_title("Ding Algorithm")

fig.autofmt_xdate()
fig.tight_layout()



