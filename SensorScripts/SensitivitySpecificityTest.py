# Created by Adam Vert
# March 2020

from SensorScripts.main import *
import matplotlib.pyplot as plt
import datetime as dt

s = SensorScripts()
test_num = 1
s.read_accelerometer(r"O:\OBI\ONDRI@Home\Data Processing\Algorithms\Non-Wear\Non-Wear Data\Test%s_Accelerometer.EDF" % test_num)
s.read_temperature(r"O:\OBI\ONDRI@Home\Data Processing\Algorithms\Non-Wear\Non-Wear Data\Test%s_Temperature.EDF" % test_num)

log_df = s.read_sample_nonwear_log(
    r"O:\OBI\ONDRI@Home\Data Processing\Algorithms\Non-Wear\Non-Wear Data\Test%s.xlsx" % test_num)
vh_df = s.vanhees_nonwear()
huberty_df = s.huberty_nonwear()
zhou_df = s.zhou_nonwear()

second_timestamps = pd.date_range(s.accelerometer_start_datetime, s.accelerometer_endtime, freq="4s")


df = pd.DataFrame({"Timestamps":second_timestamps})

# Log
print("Starting Log Calculations...")
df["Log Worn?"] = True
for index, row in log_df.iterrows():
    df.loc[(df["Timestamps"]<row["On"])&(df["Timestamps"]>row["Off"]),"Log Worn?"] = False
print("Log Calculations Complete.")

# Vanhees
print("Starting Vanhees Calculations...")
df["Vanhees Worn?"] = True
for index, row in vh_df.iterrows():
    df.loc[(df["Timestamps"]<row["End Time"])&(df["Timestamps"]>index),"Vanhees Worn?"] = row["Device Worn?"]
print("Vanhees Calculations Complete.")

# Huberty
print("Starting Huberty Calculations...")
df["Huberty Worn?"] = True
for index, row in huberty_df.iterrows():
    df.loc[(df["Timestamps"]<row["End Time"])&(df["Timestamps"]>index),"Huberty Worn?"] = row["Device Worn?"]
print("Huberty Calculations Complete.")

# Zhou
print("Starting Zhou Calculations...")
df["Zhou Worn?"] = True
for index, row in zhou_df.iterrows():
    df.loc[(df["Timestamps"]<row["End Time"])&(df["Timestamps"]>index),"Zhou Worn?"] = row["Device Worn?"]
print("Zhou Calculations Complete.")


# Analysis

#  Totals
total_positive = len(df.loc[df["Log Worn?"] == False])
total_negative = len(df.loc[df["Log Worn?"] == True])


# True Positive (TP)
vh_tp = len(df.loc[(df["Log Worn?"] == False) & (df["Vanhees Worn?"] == False)])
huberty_tp = len(df.loc[(df["Log Worn?"] == False) & (df["Huberty Worn?"] == False)])
zhou_tp = len(df.loc[(df["Log Worn?"] == False) & (df["Zhou Worn?"] == False)])

#  False Positive (FP)
vh_fp = len(df.loc[(df["Log Worn?"] == True) & (df["Vanhees Worn?"] == False)])
huberty_fp = len(df.loc[(df["Log Worn?"] == True) & (df["Huberty Worn?"] == False)])
zhou_fp = len(df.loc[(df["Log Worn?"] == True) & (df["Zhou Worn?"] == False)])

#  False Negatives (FN)
vh_fn = len(df.loc[(df["Log Worn?"] == False) & (df["Vanhees Worn?"] == True)])
huberty_fn = len(df.loc[(df["Log Worn?"] == False) & (df["Huberty Worn?"] == True)])
zhou_fn = len(df.loc[(df["Log Worn?"] == False) & (df["Zhou Worn?"] == True)])

#  True Negatives (TN)
vh_tn = len(df.loc[(df["Log Worn?"] == True) & (df["Vanhees Worn?"] == True)])
huberty_tn = len(df.loc[(df["Log Worn?"] == True) & (df["Huberty Worn?"] == True)])
zhou_tn = len(df.loc[(df["Log Worn?"] == True) & (df["Zhou Worn?"] == True)])

# Stats
vh_sensitivity = vh_tp/total_positive
huberty_sensitivity = huberty_tp/total_positive
zhou_sensitivity = zhou_tp/total_positive

vh_specificity = vh_tn/total_negative
huberty_specificity = huberty_tn/total_negative
zhou_specificity = zhou_tn/total_negative


print("Vanhees Sensitivity:", vh_sensitivity)
print("Huberty Sensitivity:", huberty_sensitivity)
print("Zhou Sensitivity:", zhou_sensitivity)
print("")
print("Vanhees Specificity:", vh_specificity)
print("Huberty Specificity:", huberty_specificity)
print("Zhou Specificity:", zhou_specificity)