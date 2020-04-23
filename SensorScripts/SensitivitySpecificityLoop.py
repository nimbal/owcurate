# Created by Adam Vert
# April 2020

# ======================================== IMPORTS ========================================
from SensorScripts import *
from SensitivitySpecificityTest import *
from scipy import signal
import matplotlib.pyplot as plt
import datetime as dt
import numpy as np
import sys

# ======================================== FUNCTION ========================================
master_df = pd.DataFrame({"Subject ID":[],
                         "Sensitivity True (ZHOU)":[],
                          "Sensitivity (VH)":[],
                          "Specificity (ZHOU)":[],
                          "Specificity (VH)":[],
                          "Trial Duration":[],
                          "Time as NW in minutes(LOG)":[],
                          "% Time as NW (LOG)":[],
                          "Time as True Positives in minutes(ZHOU)":[],
                          "Time as True Positives in minutes(VH)":[],
                          "Time as True Negative in minutes(ZHOU)": [],
                          "Time as True Negative in minutes(VH)": [],
                          "Temperature threshold for Zhou":[],
                          "Minimum Bins (ZHOU)":[],
                          "Mimimum Bins (VH)":[]})


logs_df = pd.read_excel(r"O:\Data\OND07\Raw data\Tables\Nondominant_NonwearLog.xlsx") # Read non-wear logs into a dataframe
logs_df["DEVICE OFF"] = pd.to_datetime(logs_df["DEVICE OFF"],format = "%Y%b%d %H:%M")
logs_df["DEVICE ON"] = pd.to_datetime(logs_df["DEVICE ON"],format = "%Y%b%d %H:%M")
list_of_ids = logs_df["ID"].unique()

for subject_id in list_of_ids:
    print("ID:", subject_id)

    # Get log bouts
    log_bouts = logs_df.loc[logs_df["ID"] == subject_id]
    print(log_bouts)
    #log_bouts = nw_logs.loc[logs_df["ENDCOLLECTION"] == False] # Only want bouts before

    # Get end time (if applicable)
    #end_time = nw_logs["DEVICE OFF"].loc[logs_df["ENDCOLLECTION"]==True]
    #if len(end_time) == 0:
        #end_time = None
    #elif len(end_time) == 1:
        #end_time = end_time.values[0]
    # Get handedness
    handedness = log_bouts["HANDEDNESS"].values[0]
    print(handedness)
    if handedness == "Left":
        non_dominant = "R"
    else: # Both Right handed and ambidextrous will use left wrist as non-dominant
        non_dominant = "L"

    # Read in edf's
    s = SensorScripts()
    s.read_accelerometer(r"D:\Adam PC\PycharmProjects\owcurate\OND07 EDF FILES\Accelerometer\DATAFILES\OND07_WTL_%s_A_GENEActiv_Accelerometer_%sWrist.edf" % (subject_id, non_dominant))
    s.read_temperature(r"D:\Adam PC\PycharmProjects\owcurate\OND07 EDF FILES\Temperature\DATAFILES\OND07_WTL_%s_A_GENEActiv_Temperature_%sWrist.edf" % (subject_id,non_dominant))
    for i in range(26,27):  # range(16,36):
        sens_spec = pd.Series(sensitivity_specificity(s,log_bouts,minimum_window_size = 1,t0=i), index=np.array(master_df.columns))
        master_df = master_df.append(sens_spec, ignore_index=True)

    print("")
    print("")
    print("")

print(master_df)
filename = "Sensitivity and Specificity output %s.xlsx" % dt.datetime.now().strftime("%YM%mD%dTH%HM%M")
path = os.path.join(r"D:\Adam PC\PycharmProjects\owcurate\Outputs from Non-wear paper",filename)
master_df.to_excel(path)
