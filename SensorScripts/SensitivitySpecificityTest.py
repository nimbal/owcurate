# Created by Adam Vert
# April 2020

# ======================================== IMPORTS ========================================
from SensorScripts import *
import matplotlib.pyplot as plt
import datetime as dt


# ======================================== FUNCTIONS ========================================

def sensitivity_specificity(sensor_script,log_bouts, vh_min_bins=1,zhou_min_bins=1, t0 = 26):
    """
    A function that will calculate the sensitivity and specificity of non-wear times for the Zhou and Vanhees methods
    vs the gold standard log

    Args:
        sensor_script: SensorScript class object with both accelerometer and temperature initialized
        log_bouts: The log (gold standard) start and stop times for nonwear bouts
        vh_min_bins: Number of consecutive bins required for non-wear to be considered valid for Vanhees
        zhou_min_bins: Number of consecutive bins required for non-wear to be considered valid for Zhou
        t0: The threshold at which temp has to be below to be considered valid nonwear for Zhou

    Returns:
        a list of a bunch of ROC stats that will be fed into a dataframe and later into excel

    """
    s = sensor_script

    vh_df = s.vanhees_nonwear(min_number_bins=vh_min_bins)
    zhou_df = s.zhou_nonwear(min_number_4sbins=zhou_min_bins, t0 = t0)

    second_timestamps = pd.date_range(s.accelerometer_start_datetime, s.accelerometer_endtime, freq="1s")


    df_1s = pd.DataFrame({"Timestamps":second_timestamps})

    # Log
    print("Starting Log Calculations...")
    df_1s["Log Worn?"] = True

    total_nonwear_time = dt.timedelta(0)

    for index, row in log_bouts.iterrows():
        df_1s.loc[(df_1s["Timestamps"] > row["DEVICE OFF"]) & (df_1s["Timestamps"] < row["DEVICE ON"]), "Log Worn?"] = False
        non_wear_duration = row["DEVICE ON"] - row["DEVICE OFF"]
        total_nonwear_time += non_wear_duration

    print("Log Calculations Complete.")

    # Vanhees
    print("Starting Vanhees Calculations...")
    df_1s["Vanhees Worn?"] = True
    for index, row in vh_df.iterrows():
        df_1s.loc[(df_1s["Timestamps"]<row["End Time"])&(df_1s["Timestamps"]>index),"Vanhees Worn?"] = row["Device Worn?"]
    print("Vanhees Calculations Complete.")



    # Zhou
    print("Starting Zhou Calculations...")
    repeated_zhou = np.array(pd.Series(zhou_df["Device Worn?"]).repeat(4)) # Repeats each value 4 times to equal length of 1 second NW dataframe
    print(len(np.array(pd.Series(zhou_df["Device Worn?"]).repeat(4))[:len(df_1s)]))
    print(len(df_1s))
    if len(df_1s) > len(repeated_zhou):
        df_1s.drop(df_1s.tail(len(df_1s)-len(repeated_zhou)).index, inplace=True)  # drop last n rows of df to make sure same length
        df_1s["Zhou Worn?"] = repeated_zhou
    elif len(df_1s) < len(repeated_zhou):
        df_1s["Zhou Worn?"] = repeated_zhou[:len(df_1s)] # make list same length as df
    else:
        df_1s["Zhou Worn?"] = repeated_zhou
    print("Zhou Calculations Complete.")


    # Analysis

    #  Totals
    total_positive = len(df_1s.loc[df_1s["Log Worn?"] == False])
    total_negative = len(df_1s.loc[df_1s["Log Worn?"] == True])


    # True Positive (TP)
    vh_tp = len(df_1s.loc[(df_1s["Log Worn?"] == False) & (df_1s["Vanhees Worn?"] == False)])
    zhou_tp = len(df_1s.loc[(df_1s["Log Worn?"] == False) & (df_1s["Zhou Worn?"] == False)])

    #  False Positive (FP)
    vh_fp = len(df_1s.loc[(df_1s["Log Worn?"] == True) & (df_1s["Vanhees Worn?"] == False)])
    zhou_fp = len(df_1s.loc[(df_1s["Log Worn?"] == True) & (df_1s["Zhou Worn?"] == False)])

    #  False Negatives (FN)
    vh_fn = len(df_1s.loc[(df_1s["Log Worn?"] == False) & (df_1s["Vanhees Worn?"] == True)])
    zhou_fn = len(df_1s.loc[(df_1s["Log Worn?"] == False) & (df_1s["Zhou Worn?"] == True)])

    #  True Negatives (TN)
    vh_tn = len(df_1s.loc[(df_1s["Log Worn?"] == True) & (df_1s["Vanhees Worn?"] == True)])
    zhou_tn = len(df_1s.loc[(df_1s["Log Worn?"] == True) & (df_1s["Zhou Worn?"] == True)])

    # Stats
    vh_sensitivity = vh_tp/total_positive
    zhou_sensitivity = zhou_tp/total_positive

    vh_specificity = vh_tn/total_negative
    zhou_specificity = zhou_tn/total_negative

    # Output Dict
    trial_duration = s.accelerometer_endtime - s.accelerometer_start_datetime
    percent_nonwear = float(total_nonwear_time/trial_duration)
    output_list = [s.subject_id, zhou_sensitivity, vh_sensitivity, zhou_specificity, vh_specificity, trial_duration, total_nonwear_time.total_seconds()/60, percent_nonwear, zhou_tp/60, vh_tp/60, zhou_tn, vh_tn, t0, zhou_min_bins, vh_min_bins]
    return output_list




def sensitivity_specificity_zhou_t0_test(sensor_script,log_bouts, t0 = 26):
    """
    This is an altered version of the sensitivity_specificity() function above designed specifically to find the
    optimal t0 values for Zhou

    Args:
        sensor_script: SensorScript class object with both accelerometer and temperature initialized
        log_bouts: The log (gold standard) start and stop times for nonwear bouts
        t0: The threshold at which temp has to be below to be considered valid nonwear for Zhou

    Returns:
        a list of a bunch of ROC stats that will be fed into a dataframe and later into excel
    """
    s = sensor_script

    zhou_df = s.zhou_nonwear(min_number_4sbins=1, t0 = t0)

    second_timestamps = pd.date_range(s.accelerometer_start_datetime, s.accelerometer_endtime, freq="1s")

    df_1s = pd.DataFrame({"Timestamps":second_timestamps})

    # Log
    print("Starting Log Calculations...")
    df_1s["Log Worn?"] = True

    total_nonwear_time = dt.timedelta(0)

    for index, row in log_bouts.iterrows():
        df_1s.loc[(df_1s["Timestamps"] > row["DEVICE OFF"]) & (df_1s["Timestamps"] < row["DEVICE ON"]), "Log Worn?"] = False
        non_wear_duration = row["DEVICE ON"] - row["DEVICE OFF"]
        total_nonwear_time += non_wear_duration

    print("Log Calculations Complete.")


    # Zhou
    print("Starting Zhou Calculations...")
    repeated_zhou = np.array(pd.Series(zhou_df["Device Worn?"]).repeat(4)) # Repeats each value 4 times to equal length of 1 second NW dataframe
    print(len(np.array(pd.Series(zhou_df["Device Worn?"]).repeat(4))[:len(df_1s)]))
    print(len(df_1s))
    if len(df_1s) > len(repeated_zhou):
        df_1s.drop(df_1s.tail(len(df_1s)-len(repeated_zhou)).index, inplace=True)  # drop last n rows of df to make sure same length
        df_1s["Zhou Worn?"] = repeated_zhou
    elif len(df_1s) < len(repeated_zhou):
        df_1s["Zhou Worn?"] = repeated_zhou[:len(df_1s)] # make list same length as df
    else:
        df_1s["Zhou Worn?"] = repeated_zhou
    print("Zhou Calculations Complete.")


    # Analysis

    #  Totals
    total_positive = len(df_1s.loc[df_1s["Log Worn?"] == False])
    total_negative = len(df_1s.loc[df_1s["Log Worn?"] == True])


    # True Positive (TP)
    zhou_tp = len(df_1s.loc[(df_1s["Log Worn?"] == False) & (df_1s["Zhou Worn?"] == False)])

    #  False Positive (FP)
    zhou_fp = len(df_1s.loc[(df_1s["Log Worn?"] == True) & (df_1s["Zhou Worn?"] == False)])

    #  False Negatives (FN)
    zhou_fn = len(df_1s.loc[(df_1s["Log Worn?"] == False) & (df_1s["Zhou Worn?"] == True)])

    #  True Negatives (TN)
    zhou_tn = len(df_1s.loc[(df_1s["Log Worn?"] == True) & (df_1s["Zhou Worn?"] == True)])

    # Stats
    zhou_sensitivity = zhou_tp/total_positive
    zhou_specificity = zhou_tn/total_negative

    # Output Dict
    trial_duration = s.accelerometer_endtime - s.accelerometer_start_datetime
    percent_nonwear = float(total_nonwear_time/trial_duration)
    output_list = [s.subject_id, zhou_sensitivity, zhou_specificity, trial_duration,total_negative, total_positive/60, percent_nonwear, zhou_tp/60,  zhou_tn, t0,s.accelerometer_start_datetime,s.accelerometer_endtime]
    return output_list