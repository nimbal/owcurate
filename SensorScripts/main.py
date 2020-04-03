# Adam Vert (Based on David Dings Sensor class)
# Feb 29, 2020

# ======================================== IMPORTS ========================================
import pyedflib
import os
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import pandas as pd
import datetime as dt
from scipy import signal


# ======================================== CLASS ==========================================

class SensorScripts:
    '''
    The purpose of the SensorScripts class is to have the ability to easily access and analyze multiple sensor EDFs at the same time.
    '''

    def __init__(self):
        self.accelerometer = None
        self.x_values = None
        self.y_values = None
        self.z_values = None
        self.accelerometer_frequency = None
        self.accelerometer_start_datetime = None
        self.accelerometer_duration = None
        self.accelerometer_endtime = None
        self.accelerometer_timestamps = None
        self.temperature = None
        self.temperature_values = None
        self.temperature_frequency = None
        self.temperature_start_datetime = None
        self.temperature_duration = None
        self.temperature_endtime = None
        self.temperature_timestamps = None
        self.light = None
        self.light_values = None
        self.light_frequency = None
        self.light_start_datetime = None
        self.light_duration = None
        self.light_endtime = None
        self.light_timestamps = None
        self.button = None
        self.button_values = None
        self.button_frequency = None
        self.button_start_datetime = None
        self.button_duration = None
        self.button_endtime = None
        self.button_timestamps = None
        self.subject_id = None

    def read_accelerometer(self, path_to_accelerometer):
        """
        Read in accelerometer values into the SensorScripts class

        Args:
            path_to_accelerometer: full path to accelerometer EDF

        """
        if not os.path.exists(path_to_accelerometer):
            print("ACCELEROMETER PATH NOT CORRECT, ACCELEROMETER NOT INITIALIZED")
            return

        self.accelerometer = pyedflib.EdfReader(path_to_accelerometer)
        self.x_values = self.accelerometer.readSignal(0)
        self.y_values = self.accelerometer.readSignal(1)
        self.z_values = self.accelerometer.readSignal(2)
        self.accelerometer_frequency = self.accelerometer.samplefrequency(0)
        self.accelerometer_start_datetime = self.accelerometer.getStartdatetime()
        self.accelerometer_duration = self.accelerometer.getFileDuration()
        self.accelerometer_endtime = self.accelerometer_start_datetime + dt.timedelta(
            seconds=len(self.x_values) / self.accelerometer_frequency)  # Currently using X values
        self.accelerometer_timestamps = np.asarray(
            pd.date_range(self.accelerometer_start_datetime, self.accelerometer_endtime,
                          periods=len(self.x_values)))  # Currently using X values

        if self.subject_id is None or self.subject_id == os.path.basename(path_to_accelerometer).split("_")[-1][:-4]:
            self.subject_id = os.path.basename(path_to_accelerometer).split("_")[-1][:-4]
        else:
            print("WARNING, SUBJECT ID'S DOES NOT MATCH")

        self.accelerometer.close()

        print("Accelerometer Frequency: ", self.accelerometer_frequency)
        print("Accelerometer Start Datetime: ", self.accelerometer_start_datetime)
        print("Accelerometer Duration: ", self.accelerometer_duration)
        print("Accelerometer Successfully Initialized")

    def read_temperature(self, path_to_temperature):
        """
        Read in temperature values into the SensorScripts class

        Args:
            path_to_temperature: full path to temperature EDF

        """
        if not os.path.exists(path_to_temperature):
            print("TEMPERATURE PATH NOT CORRECT, TEMPERATURE NOT INITIALIZED")
            return

        self.temperature = pyedflib.EdfReader(path_to_temperature)
        self.temperature_values = self.temperature.readSignal(0)
        self.temperature_frequency = 0.25  # self.temperature.samplefrequency(0)
        self.temperature_start_datetime = self.temperature.getStartdatetime()
        self.temperature_duration = self.temperature.getFileDuration()

        self.temperature_endtime = self.temperature_start_datetime + dt.timedelta(
            seconds=len(self.temperature_values) / self.temperature_frequency)
        self.temperature_timestamps = np.asarray(
            pd.date_range(self.temperature_start_datetime, self.temperature_endtime,
                          periods=len(self.temperature_values)))

        if self.subject_id is None or self.subject_id == os.path.basename(path_to_temperature).split("_")[-1][:-4]:
            self.subject_id = os.path.basename(path_to_temperature).split("_")[-1][:-4]
        else:
            print("WARNING, SUBJECT ID'S DOES NOT MATCH")

        self.temperature.close()

        print("Temperature Frequency: ", self.temperature_frequency)
        print("Temperature Start Datetime: ", self.temperature_start_datetime)
        print("Temperature Duration: ", self.temperature_duration)
        print("Temperature Successfully Initialized")

    def read_light(self, path_to_light):
        """
        Read in light values into the SensorScripts class

        Args:
            path_to_light: full path to light EDF

        """
        if not os.path.exists(path_to_light):
            print("LIGHT PATH NOT CORRECT, LIGHT NOT INITIALIZED")
            return

        self.light = pyedflib.EdfReader(path_to_light)
        self.light_values = self.light.readSignal(0)
        self.light_frequency = self.light.samplefrequency(0)
        self.light_start_datetime = self.light.getStartdatetime()
        self.light_duration = self.light.getFileDuration()
        self.light_endtime = self.light_start_datetime + dt.timedelta(
            seconds=len(self.light_values) / self.light_frequency)
        self.light_timestamps = np.asarray(
            pd.date_range(self.light_start_datetime, self.light_endtime, periods=len(self.light_values)))

        if self.subject_id is None or self.subject_id == os.path.basename(path_to_light).split("_")[-1][:-4]:
            self.subject_id = os.path.basename(path_to_light).split("_")[-1][:-4]
        else:
            print("WARNING, SUBJECT ID'S DOES NOT MATCH")

        self.light.close()

        print("light Frequency: ", self.light_frequency)
        print("light Start Datetime: ", self.light_start_datetime)
        print("light Duration: ", self.light_duration)
        print("Light Successfully Initialized")

    def read_button(self, path_to_button):
        """
        Read in button values into the SensorScripts class

        Args:
            path_to_button: full path to button EDF

        """
        if not os.path.exists(path_to_button):
            print("BUTTON PATH NOT CORRECT, BUTTON NOT INITIALIZED")
            return

        self.button = pyedflib.EdfReader(path_to_button)
        self.button_values = self.button.readSignal(0)
        self.button_frequency = self.button.samplefrequency(0)
        self.button_start_datetime = self.button.getStartdatetime()
        self.button_duration = self.button.getFileDuration()
        self.button_endtime = self.button_start_datetimen + dt.timedelta(
            seconds=len(self.button_values) / self.button_frequency)
        self.button_timestamps = np.asarray(
            pd.date_range(self.button_start_datetime, self.button_endtime, periods=len(self.button_values)))

        if self.subject_id is None or self.subject_id == os.path.basename(path_to_button).split("_")[-1][:-4]:
            self.subject_id = os.path.basename(path_to_button).split("_")[-1][:-4]
        else:
            print("WARNING, SUBJECT ID'S DOES NOT MATCH")

        self.button.close()

        print("button Frequency: ", self.button_frequency)
        print("button Start Datetime: ", self.button_start_datetime)
        print("button Duration: ", self.button_duration)
        print("Button Successfully Initialized")

    def read_sample_nonwear_log(self, filepath):
        """
        Created by Chris Wong

        Reads self reported nonwear logs saved in xlsx format


        Returns:
            a dataframe of nw_on times, nw_off times and whether or not it was removed for a structured removal

        """

        df = pd.read_excel(filepath)

        off_list = df['Off']
        on_list = df['On']
        structured_removal_list = df['Structured Removal']

        off_list = pd.to_datetime(off_list)
        on_list = pd.to_datetime(on_list)

        return df

    def read_OND07_nonwear_log(self):
        """

        Returns:
            df of OND07 nonwear log times for the subject ID in in self.subject_id
        """
        df = pd.read_excel(r"O:\Data\OND07\Raw data\Tables\Sensor_Removal_Log_Data.xlsx", usecols="A:M")

        print(df.loc[:, :5])

    def vanhees_nonwear(self,minimum_window_size = 60, bin_size = 15):
        '''
        Calculated non-wear scores based on the GGIR algorithm created by Vanhees

        Args:
            minimum_window_size:
            bin_size:

        Returns:
            A dataframe with columns:
             - StartTime: The start time of the 15 minute bin
             - EndTime: The end time of the 15 minute bin
             - x-std
             - y-std
             - z-std
             - Non-wear score: The count of axis std values less than 0.013

        '''
        pd.set_option('mode.chained_assignment', None)
        print("Starting Vanhees Calculation...")
        print("Bin size =", bin_size)
        print("Window size =", minimum_window_size)
        #  Create Endtime, timestamps and 15 min bin timestamps
        end_time = self.accelerometer_start_datetime + dt.timedelta(
            seconds=len(self.x_values) / self.accelerometer_frequency)  # Currently Doing X values
        timestamps = np.asarray(pd.date_range(self.accelerometer_start_datetime, end_time, periods=len(self.x_values)))
        bins = pd.date_range(self.accelerometer_start_datetime, end_time, freq='%smin' % bin_size)

        data = {"x-axis": self.x_values,
                "y-axis": self.y_values,
                "z-axis": self.z_values,
                "TimeStamps": timestamps}
        df = pd.DataFrame(data)
        df = df.set_index("TimeStamps")

        x_binned_std = []
        y_binned_std = []
        z_binned_std = []
        for n in range(len(bins) - 1):
            binned_std = df.loc[bins[n]:bins[n + 1]].std()
            x_binned_std.append(binned_std[0])
            y_binned_std.append(binned_std[1])
            z_binned_std.append(binned_std[2])

        binned_data = {"Start Time": bins[:-1],
                       "End Time": bins[1:],
                       "x-std": x_binned_std,
                       "y-std": y_binned_std,
                       "z-std": z_binned_std}

        binned_df = pd.DataFrame(binned_data)

        def nonwear_score(row):
            score = 0
            if row["x-std"] < 0.013:
                score += 1
            if row["y-std"] < 0.013:
                score += 1
            if row["z-std"] < 0.013:
                score += 1
            return score

        binned_df["Non-wear score"] = binned_df.apply(nonwear_score, axis=1)
        binned_df["Bin Not Worn?"] = False
        binned_df["Bin Not Worn?"].loc[binned_df["Non-wear score"] >= 2] = True

        binned_df["Bin Worn Consecutive Count"] = binned_df["Bin Not Worn?"] * (binned_df["Bin Not Worn?"].groupby((binned_df["Bin Not Worn?"] != binned_df["Bin Not Worn?"].shift()).cumsum()).cumcount() + 1)

        binned_df["Device Worn?"] = True
        binned_df["Device Worn?"].loc[binned_df["Bin Worn Consecutive Count"] >= minimum_window_size/bin_size] = False

        final_df = binned_df[['Start Time', 'End Time', 'Device Worn?']].copy()
        final_df = final_df.set_index("Start Time")

        return final_df

    def huberty_nonwear(self):
        '''
        Calculates non-wear periods based on Huberty algorithm

        Returns:
            A dataframe with the epoched sums, epoched std and a boolean column that states whether it is less than 0.05

        Notes:
            Original huberty algorithm removes sleep periods before running non-wear
        '''
        pd.set_option('mode.chained_assignment', None)
        len_40hz = int(len(self.x_values) * (40 / self.accelerometer_frequency))
        x_values_40hz = signal.resample(self.x_values, len_40hz)
        y_values_40hz = signal.resample(self.y_values, len_40hz)
        z_values_40hz = signal.resample(self.z_values, len_40hz)

        timestamps_1s_start = pd.date_range(self.accelerometer_start_datetime,
                                            end=self.accelerometer_endtime - dt.timedelta(minutes=1), freq="T")
        timestamps_1s_end = timestamps_1s_start.shift(1)

        def epoch_accel(x, y, z, epoch_len, frequency):
            epoch_len = epoch_len
            epoched_means = []
            vm = abs(np.sqrt(np.square(np.array([x, y, z])).sum(axis=0)) - 1)
            for i in range(0, len(vm), int(frequency * epoch_len)):
                if i + epoch_len * frequency > len(vm):
                    break

                vm_mean = np.mean(vm[i:i + epoch_len * int(frequency)])

                epoched_means.append(vm_mean)

            epoched_means = np.array(epoched_means)
            print("Epoching complete.")
            return epoched_means

        epoched_means = epoch_accel(x_values_40hz, y_values_40hz, z_values_40hz, 60, 40)

        epoched_std = []
        for n in range(0, len(epoched_means) - 20):
            epoched_std.append(np.std(epoched_means[n:n + 20]))
        for n in range(20):
            epoched_std.append(None)
        epoched_std = np.array(epoched_std)

        df = pd.DataFrame(
            {"Start Time": timestamps_1s_start, "End Time": timestamps_1s_end, "Epoched Means": epoched_means,
             "Epoched Std": epoched_std})
        df["Less than 0.05"] = False
        df.loc[df["Epoched Std"] <= 0.05, "Less than 0.05"] = True
        df["Device Worn?"] = True
        df["less than 0.05 consecutive count"] = df["Less than 0.05"] * (df["Less than 0.05"].groupby((df["Less than 0.05"] != df["Less than 0.05"].shift()).cumsum()).cumcount() + 1)
        df.loc[df["less than 0.05 consecutive count"] >= 60, "Device Worn?"] = False
        for n in df["less than 0.05 consecutive count"].loc[df["less than 0.05 consecutive count"]==60].index:
            df["Device Worn?"].iloc[n-60:n] = False

        #df.loc[df["Less than 0.05"].rolling(60).sum() == 60, "Device Worn?"] = False
        #return df
        final_df = df[['Start Time', 'End Time', 'Device Worn?']].copy()
        final_df = final_df.set_index('Start Time')

        return final_df

    def zhou_nonwear(self, minimum_window_size = 15, t0 = 26):

        '''Note that we are using a forward moving window of 4s since that is how often we get temperature results. The
        original study by Zhou used 1s '''
        # Zhou Non-wear

        temp_thresh = 26
        window_size = 60  # seconds

        # Temperature
        pd.set_option('mode.chained_assignment', None)
        zhou_df = pd.DataFrame({"Temperature Timestamps": self.temperature_timestamps,
                                "Raw Temperature Values": self.temperature_values})

        temperature_moving_average = pd.Series(self.temperature_values).rolling(
            int(60 * self.temperature_frequency)).mean()

        # Accelerometer

        zhou_accelerometer_df = pd.DataFrame({"X": self.x_values, "Y": self.y_values, "Z": self.z_values},
                                             index=self.accelerometer_timestamps)
        zhou_accelerometer_rolling_std = zhou_accelerometer_df.rolling(int(60 * self.accelerometer_frequency)).std()
        binned_4s_df = zhou_accelerometer_rolling_std.iloc[::int(4 * self.accelerometer_frequency), :]
        y = zhou_accelerometer_rolling_std.iloc[:6000]

        # Combined
        temp_moving_average_list = list(temperature_moving_average.values)
        if len(temp_moving_average_list) - len(binned_4s_df) > 0:
           temp_moving_average_list = temp_moving_average_list[:len(binned_4s_df) - len(temp_moving_average_list)]

        binned_4s_df["Temperature Moving Average"] = temp_moving_average_list

        # Zhou Algorithm

        not_worn = []
        end_times = []
        for index, row in binned_4s_df.iterrows():
            end_times.append(index + dt.timedelta(seconds=4))
            if (row["Temperature Moving Average"] < t0) and (((row["X"] + row["Y"] + row["Z"]) / 3) < 0.013):
                not_worn.append(True)
            elif row["Temperature Moving Average"] >= t0:
                not_worn.append(False)
            else:
                earlier_window_temp = binned_4s_df["Temperature Moving Average"].shift(15).loc[index]
                if row["Temperature Moving Average"] > earlier_window_temp:
                    not_worn.append(False)
                elif row["Temperature Moving Average"] < earlier_window_temp:
                    not_worn.append(True)
                elif row["Temperature Moving Average"] == earlier_window_temp:
                    not_worn.append(not_worn[-1])
                else:
                    not_worn.append(False)

        binned_4s_df["Bin not worn?"] = not_worn
        binned_4s_df["Device Worn?"] = True
        binned_4s_df["Device Worn?"].loc[binned_4s_df["Bin Worn Consecutive Count"] >= minimum_window_size / (4/60)] = False
        binned_4s_df["End Time"] = end_times

        final_df = binned_4s_df[['End Time', 'Device Worn?']].copy()

        return final_df
