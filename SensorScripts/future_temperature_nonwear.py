# Created by Adam Vert
# SEPTEMBER 2020

# ======================================== IMPORTS ========================================
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os
from SensorScripts import *
import datetime


# ======================================== FUNCTIONS ========================================

def temp_after_start(id, location, min_after=5):
    """
    Will return the temperature values a specific amount of time after the start of the non-wear periods
    """
    pd.options.mode.chained_assignment = None

    # Lists
    starting_temp = []
    future_temp = []

    # Parse Gold standard to relevant values
    gs_df = pd.read_csv(os.path.join("O:/", "Data", "ReMiNDD", "Processed Data", "GENEActiv_Nonwear",
                                     "ReMiNDDNonWearReformatted_vt_25AUG2020.csv"))  # Gold Standard Dataframe
    gs_df['start_time'] = pd.to_datetime(gs_df['start_time'], format='%Y-%m-%dT%H:%M:%S')
    gs_df['end_time'] = pd.to_datetime(gs_df['end_time'], format='%Y-%m-%dT%H:%M:%S')
    gs_df = gs_df.astype({"ID": str})
    gs_df_id = gs_df.loc[gs_df["ID"] == str(id)]
    if len(gs_df_id) == 0:
        print("NO NON-WEAR PERIODS FOR ID", id, "EITHER INVALID ID NUMBER OR NO NON-WEAR TIMES FOUND")
    gs_df_id_loc = gs_df_id.loc[gs_df_id["location"] == location]
    if len(gs_df_id_loc) == 0:
        print("NO NON-WEAR PERIODS FOR THE LOCATION (", location, ") LISTED")
    duration_of_nw = gs_df_id_loc["end_time"] - gs_df_id_loc["start_time"]
    sensor_script_object = SensorScripts()
    sensor_script_object.read_temperature(
        r"D:\Adam PC\PycharmProjects\owcurate\OND06 (ReMiNDD) EDF FILES\Temperature\DATAFILES\OND06_SBH_%s_GNAC_TEMPERATURE_%srist.edf" % (
            id, location))

    for start_time in gs_df_id_loc["start_time"]:
        temp_df = pd.DataFrame({"temperature_timestamps": sensor_script_object.temperature_timestamps,
                                "temperature_values": sensor_script_object.temperature_values})

        temp_start_value = temp_df["temperature_values"].loc[(temp_df["temperature_timestamps"] > start_time) & (
                temp_df["temperature_timestamps"] < start_time + datetime.timedelta(seconds=4))]
        if len(temp_start_value) != 1:
            raise ("EITHER NO TIME VALUE FOUND OR MULTIPLE TIME VALUES FOUND FOR THE STARTING TEMPERATURE")
        else:
            temp_start_value = temp_start_value.T.values[0]

        temp_future_value = temp_df["temperature_values"].loc[
            (temp_df["temperature_timestamps"] > start_time + datetime.timedelta(minutes=min_after)) & (
                    temp_df["temperature_timestamps"] < start_time + datetime.timedelta(minutes=min_after,
                                                                                        seconds=4))]
        if len(temp_future_value) != 1:
            raise ("EITHER NO TIME VALUE FOUND OR MULTIPLE TIME VALUES FOUND FOR THE FUTURE TEMPERATURE")
        else:
            temp_future_value = temp_future_value.T.values[0]

        starting_temp.append(temp_start_value)
        future_temp.append(temp_future_value)

        # plt.plot(temp_df["temperature_timestamps"].loc[
        #              (temp_df["temperature_timestamps"] > start_time - datetime.timedelta(minutes=10)) & (
        #                          temp_df["temperature_timestamps"] < start_time + datetime.timedelta(minutes=60))],
        #          temp_df["temperature_values"].loc[
        #              (temp_df["temperature_timestamps"] > start_time - datetime.timedelta(minutes=10)) & (
        #                          temp_df["temperature_timestamps"] < start_time + datetime.timedelta(minutes=60))])
        # plt.show()


    return pd.DataFrame({"ID":gs_df_id_loc["ID"],"start_times": gs_df_id_loc["start_time"], "end_times": gs_df_id_loc["end_time"],
                         "nw_bout_duration": duration_of_nw,
                         "starting_temperature": starting_temp,
                         "temp_%s_mins_after_start" % min_after: future_temp})


def temp_after_end(id, location, min_after=5):
    """
    Will return the temperature values a specific amount of time after the end of the non-wear periods
    """
    pd.options.mode.chained_assignment = None

    # Lists
    ending_temp = []
    future_temp = []

    # Parse Gold standard to relevant values
    gs_df = pd.read_csv(os.path.join("O:/", "Data", "ReMiNDD", "Processed Data", "GENEActiv_Nonwear",
                                     "ReMiNDDNonWearReformatted_vt_25AUG2020.csv"))  # Gold Standard Dataframe
    gs_df['start_time'] = pd.to_datetime(gs_df['start_time'], format='%Y-%m-%dT%H:%M:%S')
    gs_df['end_time'] = pd.to_datetime(gs_df['end_time'], format='%Y-%m-%dT%H:%M:%S')
    gs_df = gs_df.astype({"ID": str})
    gs_df_id = gs_df.loc[gs_df["ID"] == str(id)]
    if len(gs_df_id) == 0:
        print("NO NON-WEAR PERIODS FOR ID", id, "EITHER INVALID ID NUMBER OR NO NON-WEAR TIMES FOUND")
    gs_df_id_loc = gs_df_id.loc[gs_df_id["location"] == location]
    if len(gs_df_id_loc) == 0:
        print("NO NON-WEAR PERIODS FOR THE LOCATION (", location, ") LISTED")
    duration_of_nw = gs_df_id_loc["end_time"] - gs_df_id_loc["start_time"]

    sensor_script_object = SensorScripts()
    sensor_script_object.read_temperature(
        r"D:\Adam PC\PycharmProjects\owcurate\OND06 (ReMiNDD) EDF FILES\Temperature\DATAFILES\OND06_SBH_%s_GNAC_TEMPERATURE_%srist.edf" % (
            id, location))

    for end_time in gs_df_id_loc["end_time"]:
        temp_df = pd.DataFrame({"temperature_timestamps": sensor_script_object.temperature_timestamps,
                                "temperature_values": sensor_script_object.temperature_values})

        temp_end_value = temp_df["temperature_values"].loc[(temp_df["temperature_timestamps"] > end_time) & (
                temp_df["temperature_timestamps"] < end_time + datetime.timedelta(seconds=4))]
        if len(temp_end_value) != 1:
            raise ("EITHER NO TIME VALUE FOUND OR MULTIPLE TIME VALUES FOUND FOR THE STARTING TEMPERATURE")
        else:
            temp_end_value = temp_end_value.T.values[0]

        temp_future_value = temp_df["temperature_values"].loc[
            (temp_df["temperature_timestamps"] > end_time + datetime.timedelta(minutes=min_after)) & (
                    temp_df["temperature_timestamps"] < end_time + datetime.timedelta(minutes=min_after,
                                                                                      seconds=4))]
        if len(temp_future_value) != 1:
            raise ("EITHER NO TIME VALUE FOUND OR MULTIPLE TIME VALUES FOUND FOR THE FUTURE TEMPERATURE")
        else:
            temp_future_value = temp_future_value.T.values[0]

        ending_temp.append(temp_end_value)
        future_temp.append(temp_future_value)

        # plt.plot(temp_df["temperature_timestamps"].loc[
        #              (temp_df["temperature_timestamps"] > end_time - datetime.timedelta(minutes=60)) & (
        #                          temp_df["temperature_timestamps"] < end_time + datetime.timedelta(minutes=15))],
        #          temp_df["temperature_values"].loc[
        #              (temp_df["temperature_timestamps"] > end_time - datetime.timedelta(minutes=60)) & (
        #                          temp_df["temperature_timestamps"] < end_time + datetime.timedelta(minutes=15))])
        # #plt.show()

    return pd.DataFrame({"ID":gs_df_id_loc["ID"],"start_times": gs_df_id_loc["start_time"], "end_times": gs_df_id_loc["end_time"],
                         "nw_bout_duration": duration_of_nw,
                         "ending_temperature": ending_temp,
                         "temp_%s_mins_after_end" % min_after: future_temp})


# Creating CSV

id_list = []
start_time_list = []
end_time_list = []
nw_duration_list = []
starting_temp_list = []
future_starting_temp_list = []
ending_temp_list = []
future_ending_temp_list = []

gold_standard_df = pd.read_csv(os.path.join("O:/", "Data", "ReMiNDD", "Processed Data", "GENEActiv_Nonwear", "ReMiNDDNonWearReformatted_vt_25AUG2020.csv"))  # Gold Standard Dataframe
mins_after = 10
for id in gold_standard_df["ID"].unique():
    start_df = temp_after_start(id, "RW", min_after=mins_after)
    end_df = temp_after_end(id, "RW", min_after=mins_after)

    id_list.extend(start_df["ID"])
    start_time_list.extend(start_df["start_times"])
    end_time_list.extend(start_df["end_times"])
    nw_duration_list.extend(start_df["nw_bout_duration"])
    starting_temp_list.extend(start_df["starting_temperature"])
    future_starting_temp_list.extend(start_df["temp_%s_mins_after_start" % mins_after])
    ending_temp_list.extend(end_df["ending_temperature"])
    future_ending_temp_list.extend(end_df["temp_%s_mins_after_end" % mins_after])

final_df = pd.DataFrame({"ID":id_list,
                         "START TIME": start_time_list,
                         "END TIME":end_time_list,
                         "NW BOUT DURATION": nw_duration_list,
                         "STARTING TEMP": starting_temp_list,
                         "TEMP %s MINS AFTER START" % mins_after: future_starting_temp_list,
                         "ENDING TEMP": ending_temp_list,
                         "TEMP %s MINS AFTER END" % mins_after: future_ending_temp_list})
final_df = final_df.loc[final_df["NW BOUT DURATION"] > datetime.timedelta(minutes = mins_after)] # Removes rows where future value is longer than nw bout

final_df.to_csv(r"D:\Adam PC\PycharmProjects\owcurate\Outputs\OND06_%sMIN_TEMP_CHANGES.csv" % mins_after,index = False)