import pyedflib
import pandas as pd
import os
from SensorScripts import *
import datetime as dt

# s = SensorScripts()
# s.read_accelerometer(r"D:\Adam PC\PycharmProjects\owcurate\Test0_Accelerometer.EDF")
# s.read_temperature(r"D:\Adam PC\PycharmProjects\owcurate\Test0_Temperature.EDF")
# s.zhou_nonwear()

def nw_start_stop_times(SensorScript_object):
    zhou_df = SensorScript_object.zhou_df
    zhou_nw_starts = zhou_df.loc[(zhou_df["Device Worn?"] == False) & (zhou_df["Device Worn?"].shift(1) == True)].index
    zhou_nw_ends = zhou_df["End Time"].loc[
        ((zhou_df["Device Worn?"] == False) & (zhou_df["Device Worn?"].shift(-1) == True)) | ((zhou_df["Device Worn?"].iloc[-1] == False) & (zhou_df["End Time"] == zhou_df["End Time"].iloc[-1]))].to_numpy()
    zhou_nw_duration = zhou_nw_ends-zhou_nw_starts
    start_stop_df = pd.DataFrame({"PATIENT NUM": str(SensorScript_object.subject_id),
                                  "NW Start Time": zhou_nw_starts,
                                  "NW End Time": zhou_nw_ends,
                                  "NW Duration":zhou_nw_duration})
    return start_stop_df

def plot_nonwear(SensorScript_object, show = True, savepath = "no", id = "N/A"):

    # Zhou NW Times
    zhou_df = SensorScript_object.zhou_df
    zhou_nw_starts = zhou_df.loc[(zhou_df["Device Worn?"] == False) & (zhou_df["Device Worn?"].shift(1) == True)].index
    zhou_nw_ends = zhou_df["End Time"].loc[
        (zhou_df["Device Worn?"] == False) & (zhou_df["Device Worn?"].shift(-1) == True)].to_numpy()
    del zhou_df

    # endtime and timestamps
    end_time = SensorScript_object.accelerometer_start_datetime + dt.timedelta(
        seconds=len(SensorScript_object.x_values) / SensorScript_object.accelerometer_frequency)  # Currently Doing X values
    timestamps = np.asarray(pd.date_range(SensorScript_object.accelerometer_start_datetime, end_time, periods=len(SensorScript_object.x_values)))
    # Set up subplot
    fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True, gridspec_kw={'height_ratios': [3, 3]}, figsize = (19.2,10.8))
    xfmt = mdates.DateFormatter("%c")
    locator = mdates.HourLocator(byhour=[0, 6, 12, 18, 24], interval=1)
    plt.xticks(rotation=45, fontsize=6)
    plt.sca(ax1)

    # Subplot 1 (Accelerometer)
    epoch_accel = np.sqrt(SensorScript_object.x_values ** 2 + SensorScript_object.y_values ** 2 + SensorScript_object.z_values ** 2) - 1
    epoch_accel[epoch_accel < 0] = 0
    ax1.plot(timestamps, epoch_accel, color='purple', label="epoched accel")
    ax1.legend(loc='upper left')
    ax1.set_ylabel("G")
    ax1.xaxis.set_major_formatter(xfmt)
    ax1.xaxis.set_major_locator(locator)
    ax1.set_title("Non-wear overview plot for Left Wrist: %s" % id)

    # Subplot 2 (Temperature)
    temperature_moving_average = pd.Series(SensorScript_object.temperature_values).rolling(
        int(60 * SensorScript_object.temperature_frequency)).mean()
    timestamps_temperature = np.asarray(
        pd.date_range(SensorScript_object.temperature_start_datetime, end_time, periods=len(SensorScript_object.temperature_values)))
    ax2.plot(timestamps_temperature, temperature_moving_average, color='black', label="Temperature")
    ax2.legend(loc="upper left")
    ax2.xaxis.set_major_formatter(xfmt)
    ax2.xaxis.set_major_locator(locator)

    print("Filling between")
    n=0
    # fill non-wear times
    for start, end in zip(zhou_nw_starts, zhou_nw_ends):
        n+=1
        print(n)
        if end - start > dt.timedelta(seconds=30):
            ax1.fill_between(x=[np.datetime64(start), end], y1=np.min(epoch_accel), y2=np.max(epoch_accel),
                            color='Red', alpha=0.60, linewidth=0.0)
            ax2.fill_between(x=[np.datetime64(start), end], y1=np.min(SensorScript_object.temperature_values),
                            y2=np.max(SensorScript_object.temperature_values), color='Red', alpha=0.60, linewidth=0.0)

    if show == True:
        plt.show()
    if savepath != "no":
        plt.savefig(savepath)

def compliance_hist(compliance_rates, show = True, savepath = "no"):
    plt.hist(compliance_rates, edgecolor="black", linewidth=1.2)
    plt.suptitle("Compliance Rate by Person")
    if show == True:
        plt.show()
    if savepath != "no":
        plt.savefig(savepath)


accel_dir = r"D:\Adam PC\PycharmProjects\owcurate\PD and DANCE EDF FILES\Accelerometer\DATAFILES"
ids = [f.split("_")[2]+"_"+f.split("_")[3] for f in os.listdir(accel_dir) if f.lower().endswith('.edf') and f[:-4].split('_')[-1] in ["LWrist"]] # This part may need to be changed depending on the study
ids = np.unique(ids)
print(ids)
compliance = []
s=1
# for id in ids:
#     print(id)
#     try:
#         del s
#         s = SensorScripts()
#         s.read_accelerometer(r"D:\Adam PC\PycharmProjects\owcurate\PD and DANCE EDF FILES\Accelerometer\DATAFILES\OND08_TWH_%s_GENEActiv_Accelerometer_LWrist.edf" % id)
#         s.read_temperature(r"D:\Adam PC\PycharmProjects\owcurate\PD and DANCE EDF FILES\Temperature\DATAFILES\OND08_TWH_%s_GENEActiv_Temperature_LWrist.edf" % id)
#         #s.read_accelerometer(r"D:\Adam PC\PycharmProjects\owcurate\Test0_Accelerometer.EDF")
#         #s.read_temperature(r"D:\Adam PC\PycharmProjects\owcurate\Test0_Temperature.EDF")
#         s.zhou_nonwear()
#
#         start_stop_df=nw_start_stop_times(s)
#         daily_nw_duration = start_stop_df["NW Duration"].groupby(start_stop_df["NW Start Time"].dt.date).sum()
#         daily_nw_duration.index.names = ['Date']
#         id_compliance = daily_nw_duration.sum().total_seconds()/s.accelerometer_duration
#         compliance.append(id_compliance)
#         daily_nw_duration.to_csv(r"O:\Data\TWH\Processed Data\NW Outputs\Start and Stop Times\OND08_NW_daily_metrics_%s_LWrist.csv"%id)
#         start_stop_df.to_csv(r"O:\Data\TWH\Processed Data\NW Outputs\Start and Stop Times\OND08_NW_start_stop_%s_LWrist.csv"%id)
#         plot_nonwear(s, show=False,savepath=r"O:\Data\TWH\Processed Data\NW Outputs\Overview Plots\OND08_NW_overview_%s_LWrist.png"% id, id = id)
#
#         plt.close(fig='all')
#         compliance_hist(compliance,show = False, savepath = r"O:\Data\TWH\Processed Data\NW Outputs\Histograms\Compliance Rate Histogram LWrist.png")
#         plt.close(fig='all')
#
#     except:
#         print("ERROR?????")
#         continue
#
accel_dir = r"D:\Adam PC\PycharmProjects\owcurate\PD and DANCE EDF FILES\Accelerometer\DATAFILES"
ids = [f.split("_")[2]+"_"+f.split("_")[3] for f in os.listdir(accel_dir) if f.lower().endswith('.edf') and f[:-4].split('_')[-1] in ["LWrist"]] # This part may need to be changed depending on the study
ids = np.unique(ids)
print(ids)
collection_times = []
left_nw_duration = []
right_nw_duration = []
combined_nw_duration = []
left_compliance = []
right_compliance = []
combined_compliance = []
for id in ids:
    # Fix Daily Metrics
    s = SensorScripts()
    s.read_temperature(
        r"D:\Adam PC\PycharmProjects\owcurate\PD and DANCE EDF FILES\Temperature\DATAFILES\OND08_TWH_%s_GENEActiv_Temperature_RWrist.edf" % id)
    daily_nw = pd.DataFrame({"Timestamps":s.temperature_timestamps,
                             "Device Worn?": dt.timedelta(seconds = 0) })
    temp_left_start_stop = pd.read_csv(
        r"O:\Data\TWH\Processed Data\NW Outputs\Start and Stop Times\OND08_NW_start_stop_%s_LWrist.csv" % id)
    left_daily_copy = daily_nw.copy()
    temp_right_start_stop = pd.read_csv(
        r"O:\Data\TWH\Processed Data\NW Outputs\Start and Stop Times\OND08_NW_start_stop_%s_RWrist.csv" % id)
    right_daily_copy = daily_nw.copy()
    master_daily_copy = daily_nw.copy()
    for start, end in zip(temp_left_start_stop["NW Start Time"], temp_left_start_stop["NW End Time"]):
        left_daily_copy["Device Worn?"].loc[(left_daily_copy["Timestamps"]> start) & (left_daily_copy["Timestamps"] < end)] = dt.timedelta(seconds = 4)
        master_daily_copy["Device Worn?"].loc[
            (master_daily_copy["Timestamps"] > start) & (master_daily_copy["Timestamps"] < end)] = dt.timedelta(seconds = 4)
    for start, end in zip(temp_right_start_stop["NW Start Time"], temp_right_start_stop["NW End Time"]):
        right_daily_copy["Device Worn?"].loc[
            (right_daily_copy["Timestamps"] > start) & (right_daily_copy["Timestamps"] < end)] = dt.timedelta(seconds = 4)
        master_daily_copy["Device Worn?"].loc[
            (master_daily_copy["Timestamps"] > start) & (master_daily_copy["Timestamps"] < end)] = dt.timedelta(seconds = 4)

    left_daily_nw_duration = left_daily_copy["Device Worn?"].groupby(left_daily_copy["Timestamps"].dt.date).sum()
    right_daily_nw_duration = right_daily_copy["Device Worn?"].groupby(right_daily_copy["Timestamps"].dt.date).sum()
    combined_daily_nw_duration = master_daily_copy["Device Worn?"].groupby(master_daily_copy["Timestamps"].dt.date).sum()

    daily_nw_df = pd.concat([left_daily_nw_duration,right_daily_nw_duration,combined_daily_nw_duration], axis = 1)
    daily_nw_df.columns = ["Left NW Duration", "Right NW Duration", "Combined NW Duration"]

    daily_nw_df.to_csv(r"O:\Data\TWH\Processed Data\NW Outputs\Start and Stop Times\OND08_NW_daily_metrics_%s.csv" % id)
    # Master Collection Times
    ct = dt.timedelta(seconds = s.temperature_duration)
    collection_times.append(ct)

    # Left and Right total NW durations
    left_nw_duration.append(daily_nw_df["Left NW Duration"].sum())
    right_nw_duration.append(daily_nw_df["Right NW Duration"].sum())
    combined_nw_duration.append(daily_nw_df["Combined NW Duration"].sum())

    # Compliances
    left_compliance.append(daily_nw_df["Left NW Duration"].sum()/ct)
    right_compliance.append(daily_nw_df["Right NW Duration"].sum()/ct)
    combined_compliance.append(daily_nw_df["Combined NW Duration"].sum()/ct)

collection_compliance_df = pd.DataFrame({"ID":ids,
                                         "Collection Time": collection_times,
                                         "Left NW Duration": left_nw_duration,
                                         "Right NW Duration": right_nw_duration,
                                         "Combined NW Duration": combined_nw_duration,
                                         "Left Compliance":left_compliance,
                                         "Right Compliance": right_compliance,
                                         "Combined Compliance": combined_compliance})

collection_compliance_df.to_csv(r"O:\Data\TWH\Processed Data\NW Outputs\Start and Stop Times\OND08_NW_Compliance_and_CollectionTime.csv")


