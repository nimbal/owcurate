
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
import time

# ======================================== FUNCTION ========================================



start = time.time()
master_df = pd.DataFrame({"Subject ID":[],
                         "Sensitivity True (ZHOU)":[],
                          "Specificity (ZHOU)":[],
                          "Trial Duration":[],
                          "Total Wear Time in minutes(LOG)":[],
                          "Time as NW in minutes(LOG)":[],
                          "% Time as NW (LOG)":[],
                          "Time as True Positives in minutes(ZHOU)":[],
                          "Time as True Negative in minutes(ZHOU)": [],
                          "Temperature threshold for Zhou":[],
                          "Start Datetime":[],
                          "End Datetime":[]})


logs_df = pd.read_excel(r"O:\Data\OND07\Raw data\Tables\Nondominant_NonwearLog.xlsx") # Read non-wear logs into a dataframe
logs_df["DEVICE OFF"] = pd.to_datetime(logs_df["DEVICE OFF"],format = "%Y%b%d %H:%M")
logs_df["DEVICE ON"] = pd.to_datetime(logs_df["DEVICE ON"],format = "%Y%b%d %H:%M")
list_of_ids = list(logs_df["ID"].unique())
list_of_ids.remove(3017) # Removing subject 3017 since EDF is invalid
for subject_id in list_of_ids:
    print("ID:", subject_id)
    subject_start_time = time.time()

    # Get log bouts
    log_bouts = logs_df.loc[logs_df["ID"] == subject_id]
    #log_bouts = nw_logs.loc[logs_df["ENDCOLLECTION"] == False] # Only want bouts before

    # Get end time (if applicable)
    #end_time = nw_logs["DEVICE OFF"].loc[logs_df["ENDCOLLECTION"]==True]
    #if len(end_time) == 0:
        #end_time = None
    #elif len(end_time) == 1:
        #end_time = end_time.values[0]
    # Get handedness
    handedness = log_bouts["HANDEDNESS"].values[0]
    if handedness == "Left":
        non_dominant = "R"
    else: # Both Right handed and ambidextrous will use left wrist as non-dominant
        non_dominant = "L"

    # Read in edf's
    s = SensorScripts()
    if subject_id == 3041 or subject_id == 3023: # both 3041 and 3023 are inputted as the 2nd visit
        s.read_accelerometer(r"D:\Adam PC\PycharmProjects\owcurate\OND07 EDF FILES\Accelerometer\DATAFILES\OND07_WTL_%s_B_GENEActiv_Accelerometer_%sWrist.edf" % (subject_id, non_dominant))
        s.read_temperature(r"D:\Adam PC\PycharmProjects\owcurate\OND07 EDF FILES\Temperature\DATAFILES\OND07_WTL_%s_B_GENEActiv_Temperature_%sWrist.edf" % (subject_id,non_dominant))
    else:
        s.read_accelerometer(r"D:\Adam PC\PycharmProjects\owcurate\OND07 EDF FILES\Accelerometer\DATAFILES\OND07_WTL_%s_A_GENEActiv_Accelerometer_%sWrist.edf" % (subject_id, non_dominant))
        s.read_temperature(r"D:\Adam PC\PycharmProjects\owcurate\OND07 EDF FILES\Temperature\DATAFILES\OND07_WTL_%s_A_GENEActiv_Temperature_%sWrist.edf" % (subject_id,non_dominant))
    for i in range(12,40):  # range(16,36):
        print("Testing temp value:",i)
        sens_spec = pd.Series(sensitivity_specificity_zhou_t0_test(s,log_bouts,t0=i), index=np.array(master_df.columns))
        master_df = master_df.append(sens_spec, ignore_index=True)
    print("Time taken to complete subject",str(subject_id)+":",time.time()-subject_start_time)

    print("")
    print("")
    print("")

print(master_df)
filename = "Optimal t0 output %s.xlsx" % dt.datetime.now().strftime("%YM%mD%dTH%HM%M")
path = os.path.join(r"D:\Adam PC\PycharmProjects\owcurate\Outputs from Non-wear paper",filename)
master_df.to_excel(path)

time_taken = time.time()-start
print("TOTAL TIME TAKEN IN SECONDS:",time_taken)


def t0_roc_curve(excel_path):
    excel_path = r"D:\Adam PC\PycharmProjects\owcurate\Outputs from Non-wear paper\Optimal t0 output 2020M04D22TH16M13.xlsx"
    excel_df = pd.read_excel(excel_path)
    t0_values = list(excel_df["Temperature threshold for Zhou"].unique())

    temp_thresh = []
    sensitivity = []
    specificity = []

    for t0 in t0_values:
        temp_df = excel_df.loc[excel_df["Temperature threshold for Zhou"] == t0]
        minutes_of_nw = temp_df["Time as NW in minutes(LOG)"].sum()
        minutes_of_wear = temp_df["Total Wear Time in minutes(LOG)"].sum()
        zhou_tp = temp_df["Time as True Positives in minutes(ZHOU)"].sum()
        zhou_tn = temp_df["Time as True Negative in minutes(ZHOU)"].sum()

        zhou_sensitivity = zhou_tp / minutes_of_nw
        zhou_specificity = zhou_tn / minutes_of_wear

        temp_thresh.append(t0)
        sensitivity.append(zhou_sensitivity)
        specificity.append(zhou_specificity)

    output_df = pd.DataFrame({"Temperature Threshold": temp_thresh,
                              "Sensitivity(True positive / total positive)": sensitivity,
                              "Specificity (True negative  / total negative)": specificity})

    plt.plot(1 - np.array(output_df["Sensitivity(True positive / total positive)"]),
             output_df["Specificity (True negative  / total negative)"])
    plt.xlim([0, 1])
    plt.ylim([0, 1])