# Created by Adam Vert
# March 2020

from SensorScripts.main import *
import matplotlib.pyplot as plt
import datetime as dt

'''
To create a visual comparison of vanhees vs gold standard log data

Returns:
    a plot of logged nonwear values vs algorithm non-wear values overlayed on top of accelerometer and temperature plots

'''

s = SensorScripts()
test_num = 0
s.read_accelerometer(r"O:\OBI\ONDRI@Home\Data Processing\Algorithms\Non-Wear\Non-Wear Data\Test%s_Accelerometer.EDF" % test_num)
s.read_temperature(r"O:\OBI\ONDRI@Home\Data Processing\Algorithms\Non-Wear\Non-Wear Data\Test%s_Temperature.EDF" % test_num)
#s.read_accelerometer(r"D:\Adam PC\PycharmProjects\owcurate\Test%s_Accelerometer.EDF" % test_num)
#s.read_temperature(r"D:\Adam PC\PycharmProjects\owcurate\Test%s_Temperature.EDF" % test_num)


# endtime and timestamps
end_time = s.accelerometer_start_datetime + dt.timedelta(seconds=len(s.x_values) / s.accelerometer_frequency)  # Currently Doing X values
timestamps = np.asarray(pd.date_range(s.accelerometer_start_datetime, end_time, periods=len(s.x_values)))

#  Vanhess nonwear calculation
vh_df = s.vanhees_nonwear()

vh_nw_starts = vh_df.loc[vh_df["Device Worn?"] == False].index
vh_nw_ends = vh_df["End Time"].loc[vh_df["Device Worn?"] == False].to_numpy()

# Set up subplot
fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True, gridspec_kw={'height_ratios': [3, 3]})
xfmt = mdates.DateFormatter("%c")
locator = mdates.HourLocator(byhour=[0, 6, 12, 18, 24], interval=1)
plt.xticks(rotation=45, fontsize=6)
plt.sca(ax1)

# Subplot 1 (Accelerometer)
ax1.plot(timestamps, s.x_values, color='purple', label="x")
ax1.plot(timestamps, s.y_values, color='blue', label="y")
ax1.plot(timestamps, s.z_values, color='black', label="z")
ax1.legend(loc='upper left')
ax1.set_ylabel("G")
ax1.xaxis.set_major_formatter(xfmt)
ax1.xaxis.set_major_locator(locator)
ax1.set_title("Vanhees=Red, Huberty=Green, Zhou=Orange, Log=Blue")

# Subplot 2 (Temperature)
timestamps_temperature = np.asarray(
    pd.date_range(s.temperature_start_datetime, end_time, periods=len(s.temperature_values)))
ax2.plot(timestamps_temperature, s.temperature_values, color='black', label="Temperature")
ax2.legend(loc="upper left")
ax2.xaxis.set_major_formatter(xfmt)
ax2.xaxis.set_major_locator(locator)

# Logged NW times:
logged_nw_df = s.read_sample_nonwear_log(r"O:\OBI\ONDRI@Home\Data Processing\Algorithms\Non-Wear\Non-Wear Data\Test%s.xlsx" % test_num)
logged_nw_starts = logged_nw_df["Off"]
logged_nw_ends = logged_nw_df["On"]

# Huberty NW Times
huberty_df = s.huberty_nonwear()
vh_nw_starts = vh_df.loc[vh_df["Device Worn?"] == False].index
huberty_nw_starts = huberty_df.loc[huberty_df["Device Worn?"] == False].index
huberty_nw_ends = huberty_df["End Time"].loc[huberty_df["Device Worn?"] == False].to_numpy()

# Zhou NW Times
zhou_df = s.zhou_nonwear()
zhou_nw_starts = zhou_df.loc[zhou_df["Device Worn?"] == False].index
zhou_nw_ends = zhou_df["End Time"].loc[zhou_df["Device Worn?"] == False].to_numpy()

# fill non-wear times
try:
    for start, end in zip(vh_nw_starts, vh_nw_ends):
        ax1.fill_between(x=[np.datetime64(start), end], y1=4.25, y2=8, color='red', alpha=0.60, linewidth=0.0)
        ax2.fill_between(x=[np.datetime64(start), end], y1=np.min(s.temperature_values) + (
                    np.max(s.temperature_values) - np.min(s.temperature_values)) * 3 / 4 + 0.5,
                         y2=np.max(s.temperature_values), color='red', alpha=0.60, linewidth=0.0)

    for start, end in zip(huberty_nw_starts, huberty_nw_ends):
        ax1.fill_between(x=[np.datetime64(start), end], y1=0.25, y2=3.75, color='green', alpha=0.60, linewidth=0.0)
        ax2.fill_between(x=[np.datetime64(start), end], y1=np.min(s.temperature_values) + (
                    np.max(s.temperature_values) - np.min(s.temperature_values)) * 2 / 4 + 0.5,
                         y2=np.min(s.temperature_values) + (
                                     np.max(s.temperature_values) - np.min(s.temperature_values)) * 3 / 4 - 0.5,
                         color='green', alpha=0.60, linewidth=0.0)

    for start, end in zip(zhou_nw_starts, zhou_nw_ends):
        ax1.fill_between(x=[np.datetime64(start), end], y1=-3.75, y2=-0.25, color='Orange', alpha=0.60, linewidth=0.0)
        ax2.fill_between(x=[np.datetime64(start), end], y1=np.min(s.temperature_values) + (
                    np.max(s.temperature_values) - np.min(s.temperature_values)) / 4 + 0.5,
                         y2=np.min(s.temperature_values) + (
                                     np.max(s.temperature_values) - np.min(s.temperature_values)) * 2 / 4 - 0.5,
                         color='orange', alpha=0.60, linewidth=0.0)

    for start, end in zip(logged_nw_starts, logged_nw_ends):
        ax1.fill_between(x=[start, end], y1=-8, y2=-4.25, color='blue', alpha=0.60, linewidth=0.0)
        ax2.fill_between(x=[start, end], y1=np.min(s.temperature_values),
                         y2=np.min(s.temperature_values) + (
                                 np.max(s.temperature_values) - np.min(s.temperature_values)) / 4 - 0.5,
                         color='blue', alpha=0.60,
                         linewidth=0.0)

except (IndexError, AttributeError):
    pass

plt.show()
