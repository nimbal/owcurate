# Created by Adam Vert
# March 2020
# ======================================== IMPORTS ========================================
from SensorScripts import *
import matplotlib.pyplot as plt
import datetime as dt

# ======================================== FUNCTION ========================================

'''
To create a visual comparison of vanhees vs zhou vs gold standard log data

Returns:
    a plot of logged nonwear values vs algorithm non-wear values overlayed on top of accelerometer and temperature plots

'''

s = SensorScripts()
subject_id = 1039
accel_path = r"E:\nimbal\data\OND06_processed_%d\Accelerometer\DATAFILES\OND06_SBH_%d_A_SE01_GABL_GENEActiv_Accelerometer_LW.edf" % (subject_id, subject_id)
temp_path = r"E:\nimbal\data\OND06_processed_%d\Temperature\DATAFILES\OND06_SBH_%d_A_SE01_GABL_GENEActiv_Temperature_LW.edf" % (subject_id, subject_id)
s.read_accelerometer(accel_path)
s.read_temperature(temp_path)



# endtime and timestamps
end_time = s.accelerometer_start_datetime + dt.timedelta(seconds=len(s.x_values) / s.accelerometer_frequency)  # Currently Doing X values
timestamps = np.asarray(pd.date_range(s.accelerometer_start_datetime, end_time, periods=len(s.x_values)))


#  Vanhess nonwear calculation
vh_df = s.vanhees_nonwear(bin_size=15)
vh_nw_starts = vh_df.loc[vh_df["Device Worn?"] == False].index
vh_nw_ends = vh_df["End Time"].loc[vh_df["Device Worn?"] == False].to_numpy()
del vh_df

# Set up subplot
fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True, gridspec_kw={'height_ratios': [3, 3]})
xfmt = mdates.DateFormatter("%c")
locator = mdates.HourLocator(byhour=[0, 6, 12, 18, 24], interval=1)
plt.xticks(rotation=45, fontsize=6)
plt.sca(ax1)

# Subplot 1 (Accelerometer)
epoch_accel = np.sqrt(s.x_values**2 + s.y_values**2 + s.z_values**2) - 1
ax1.plot(timestamps, epoch_accel, color='purple', label="epoched accel")
ax1.legend(loc='upper left')
ax1.set_ylabel("G")
ax1.xaxis.set_major_formatter(xfmt)
ax1.xaxis.set_major_locator(locator)
ax1.set_title("Vanhees=Red, Huberty=Green, Zhou=Orange, Log=Blue")
del timestamps

# Subplot 2 (Temperature)
timestamps_temperature = np.asarray(
    pd.date_range(s.temperature_start_datetime, end_time, periods=len(s.temperature_values)))
ax2.plot(timestamps_temperature, s.temperature_values, color='black', label="Temperature")
ax2.legend(loc="upper left")
ax2.xaxis.set_major_formatter(xfmt)
ax2.xaxis.set_major_locator(locator)

# Logged NW times:
logged_nw_df = s.read_OND06_nonwear_log(path=r"E:\\nimbal\\data\\non-wear_data\\Sensor_Removal_Log_Data.xlsx")
logged_nw_subject_df = logged_nw_df.loc[logged_nw_df["ID"] == subject_id]
logged_nw_starts = logged_nw_subject_df["DEVICE OFF"]
logged_nw_ends = logged_nw_subject_df["DEVICE ON"]

# # Huberty NW Times
# huberty_df = s.huberty_nonwear()
# huberty_nw_starts = huberty_df.loc[huberty_df["Device Worn?"] == False].index
# huberty_nw_ends = huberty_df["End Time"].loc[huberty_df["Device Worn?"] == False].to_numpy()
# del huberty_df

# Zhou NW Times
zhou_df = s.zhou_nonwear()
zhou_nw_starts = zhou_df.loc[zhou_df["Device Worn?"] == False].index
zhou_nw_ends = zhou_df["End Time"].loc[zhou_df["Device Worn?"] == False].to_numpy()
del zhou_df

# fill non-wear times
try:
    for start, end in zip(vh_nw_starts, vh_nw_ends):
        ax1.fill_between(x=[np.datetime64(start), end], y1=3, y2=8, color='red', alpha=0.60, linewidth=0.0)
        ax2.fill_between(x=[np.datetime64(start), end], y1=np.max(s.temperature_values) - (
                    np.max(s.temperature_values) - np.min(s.temperature_values)) /3 + 0.5,
                         y2=np.max(s.temperature_values), color='red', alpha=0.60, linewidth=0.0)

    for start, end in zip(zhou_nw_starts, zhou_nw_ends):
        ax1.fill_between(x=[np.datetime64(start), end], y1=-2.5, y2=2.5, color='Orange', alpha=0.60, linewidth=0.0)
        ax2.fill_between(x=[np.datetime64(start), end], y1=np.max(s.temperature_values) - (
                    np.max(s.temperature_values) - np.min(s.temperature_values))*2 /3 + 0.5,
                         y2=np.max(s.temperature_values) - (
                    np.max(s.temperature_values) - np.min(s.temperature_values)) /3 - 0.5,
                         color='orange', alpha=0.60, linewidth=0.0)
    for start, end in zip(logged_nw_starts, logged_nw_ends):
        if end < start:
            #temporary fix
            end += dt.timedelta(days=1)
        if not (pd.isnull(start) or pd.isnull(end)):
            ax1.fill_between(x=[start, end], y1=-8, y2=-3, color='blue', alpha=0.60, linewidth=0.0)
            ax2.fill_between(x=[start, end], y1=np.min(s.temperature_values),y2=np.max(s.temperature_values) - (
                        np.max(s.temperature_values) - np.min(s.temperature_values))*2 /3 - 0.5,color='blue', alpha=0.60,linewidth=0.0)
except (IndexError, AttributeError):
    pass

plt.show()
del end_time