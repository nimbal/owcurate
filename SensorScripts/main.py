# Adam Vert (Based on David Dings Sensor class)
# Feb 29, 2020

# ======================================== IMPORTS ========================================
import pyedflib
import os
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import pandas as pd
import datetime
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
        self.vanhees_nonwear_df = None
        self.log_nonwear_df = None
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
        self.accelerometer_endtime = self.accelerometer_start_datetime + datetime.timedelta(
            seconds=len(self.x_values) / self.accelerometer_frequency)  # Currently using X values
        self.accelerometer_timestamps = np.asarray(
            pd.date_range(self.accelerometer_start_datetime, self.accelerometer_endtime, periods=len(self.x_values)))  # Currently using X values

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
        self.temperature_frequency = self.temperature.samplefrequency(0)
        self.temperature_start_datetime = self.temperature.getStartdatetime()
        self.temperature_duration = self.temperature.getFileDuration()
        self.temperature_endtime = self.temperature_start_datetime + datetime.timedelta(
            seconds=len(self.temperature_values) / self.temperature_frequency)
        self.temperature_timestamps = np.asarray(
            pd.date_range(self.temperature_start_datetime, self.temperature_endtime, periods=len(self.temperature_values)))

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
        self.light_endtime = self.light_start_datetime + datetime.timedelta(seconds=len(self.light_values) / self.light_frequency)
        self.light_timestamps = np.asarray(pd.date_range(self.light_start_datetime, self.light_endtime, periods=len(self.light_values)))

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
        self.button_endtime = self.button_start_datetimen + datetime.timedelta(seconds=len(self.button_values) / self.button_frequency)
        self.button_timestamps = np.asarray(pd.date_range(self.button_start_datetime, self.button_endtime, periods=len(self.button_values)))

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
        self.log_nonwear_df = df

        return df

    def read_OND07_nonwear_log(self):
        """

        Returns:
            df of OND07 nonwear log times for the subject ID in in self.subject_id
        """
        df = pd.read_excel(r"O:\Data\OND07\Raw data\Tables\Sensor_Removal_Log_Data.xlsx", usecols="A:M")

        print(df.loc[:, :5])

    def vanhees_nonwear(self):
        '''
        Calculated non-wear scores based on the GGIR algorithm created by Vanhees

        Returns:
            A dataframe with columns:
             - StartTime: The start time of the 15 minute bin
             - EndTime: The end time of the 15 minute bin
             - x-std
             - y-std
             - z-std
             - Non-wear score: The count of axis std values less than 0.013

        '''

        #  Vanhess nonwear calculation

        #  Create Endtime, timestamps and 15 min bin timestamps
        end_time = self.accelerometer_start_datetime + datetime.timedelta(
            seconds=len(self.x_values) / self.accelerometer_frequency)  # Currently Doing X values
        timestamps = np.asarray(pd.date_range(self.accelerometer_start_datetime, end_time, periods=len(self.x_values)))
        bins_15 = pd.date_range(self.accelerometer_start_datetime + datetime.timedelta(minutes=22.5), end_time, freq='15min')

        data = {"x-axis": self.x_values,
                "y-axis": self.y_values,
                "z-axis": self.z_values,
                "TimeStamps": timestamps}
        df = pd.DataFrame(data)
        df = df.set_index("TimeStamps")

        x_binned_std = []
        y_binned_std = []
        z_binned_std = []
        for n in range(len(bins_15) - 1):
            binned_std = df.loc[(bins_15[n] - datetime.timedelta(minutes=22.5)):(bins_15[n + 1] + datetime.timedelta(minutes=22.5))].std()
            x_binned_std.append(binned_std[0])
            y_binned_std.append(binned_std[1])
            z_binned_std.append(binned_std[2])

        binned_data = {"StartTime": bins_15[:-1],
                       "EndTime": bins_15[1:],
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

        self.vanhees_nonwear_df = binned_df

        return binned_df

    def plot_nw_vs_log(self):
        '''
        To create a visual comparison of vanhees vs gold standard log data

        Returns:
            a plot of logged nonwear values in blue and vanhees nonwear values in red overlayed on subplots with non-wear scores, axis values and temperature values

        Notes:
            Must have read into the class the accelerometer EDF and the log data.
            TODO: Must add error messages if accelerometer/logs aren't initiated

        Example:
            s = SensorScripts()

            accelerometer_path = "accelerometer/path/name.EDF"
            temperature_path = "temperature/path/name.EDF"
            log_path = "log/path/name.xlsx"
            s.read_accelerometer(accelerometer_path)
            s.read_temperature(temperature_path)
            s.read_nonwear_log(log_path)

            s.plot_vanhees_vs_log()


        '''

        # endtime and timestamps
        end_time = self.accelerometer_start_datetime + datetime.timedelta(
            seconds=len(self.x_values) / self.accelerometer_frequency)  # Currently Doing X values
        timestamps = np.asarray(pd.date_range(self.accelerometer_start_datetime, end_time, periods=len(self.x_values)))

        #  Vanhess nonwear calculation
        binned_df = self.vanhees_nonwear()

        vh_nw_starts = binned_df["StartTime"].loc[binned_df["Non-wear score"] >= 2].to_numpy()
        vh_nw_ends = binned_df["EndTime"].loc[binned_df["Non-wear score"] >= 2].to_numpy()

        # Set up subplot
        fig, (ax1, ax2, ax3) = plt.subplots(3, 1, sharex=True, gridspec_kw={'height_ratios': [1, 3, 3]})
        xfmt = mdates.DateFormatter("%c")
        locator = mdates.HourLocator(byhour=[0, 6, 12, 18, 24], interval=1)
        plt.xticks(rotation=45, fontsize=6)
        plt.sca(ax1)
        plt.yticks([0, 1, 2, 3])

        # Subplot 1 (Non-wear Score)
        ax1.plot(binned_df["StartTime"], binned_df["Non-wear score"], color="black", label="Non-wear score")
        ax1.xaxis.set_major_formatter(xfmt)
        ax1.xaxis.set_major_locator(locator)
        ax1.set_title("Red = Vanhees, Green = Huberty (In progress), Blue = Log (Gold Standard)")

        # Subplot 2 (Accelerometer)
        ax2.plot(timestamps, self.x_values, color='purple', label="x")
        ax2.plot(timestamps, self.y_values, color='blue', label="y")
        ax2.plot(timestamps, self.z_values, color='black', label="z")
        ax2.legend(loc='upper left')
        ax2.set_ylabel("G")
        ax2.xaxis.set_major_formatter(xfmt)
        ax2.xaxis.set_major_locator(locator)

        # Subplot 3 (Temperature)
        timestamps_temperature = np.asarray(pd.date_range(self.temperature_start_datetime, end_time, periods=len(self.temperature_values)))
        ax3.plot(timestamps_temperature, self.temperature_values, color='black', label="Temperature")
        ax3.legend(loc="upper left")
        ax3.xaxis.set_major_formatter(xfmt)
        ax3.xaxis.set_major_locator(locator)

        # Logged NW times:
        logged_nw_df = self.log_nonwear_df
        logged_nw_starts = logged_nw_df["Off"]
        logged_nw_ends = logged_nw_df["On"]

        # Huberty NW Times
        huberty_df = self.huberty_nonwear()
        huberty_nw_starts = huberty_df["Time stamps start"].loc[huberty_df["60 minutes?"] == 1].to_numpy()
        huberty_nw_ends = huberty_df["Time stamps end"].loc[huberty_df["60 minutes?"] == 1].to_numpy()

        # fill non-wear times
        try:
            for start, end in zip(vh_nw_starts, vh_nw_ends):
                ax1.fill_between(x=[start, end], y1=2.1, y2=3, color='red', alpha=0.60, linewidth=0.0)
                ax2.fill_between(x=[start, end], y1=2.75, y2=8, color='red', alpha=0.60, linewidth=0.0)
                ax3.fill_between(x=[start, end], y1=np.min(self.temperature_values)+(np.max(self.temperature_values)-np.min(self.temperature_values))*2/3+0.5,
                                 y2=np.max(self.temperature_values), color='red', alpha=0.60, linewidth=0.0)

            for start, end in zip(huberty_nw_starts, huberty_nw_ends):
                ax1.fill_between(x=[start, end], y1=1.1, y2=1.9, color='green', alpha=0.60, linewidth=0.0)
                ax2.fill_between(x=[start, end], y1=-2.50, y2=2.6, color='green', alpha=0.60, linewidth=0.0)
                ax3.fill_between(x=[start, end], y1=np.min(self.temperature_values)+(np.max(self.temperature_values)-np.min(self.temperature_values))/3+0.5,
                                 y2=np.min(self.temperature_values)+(np.max(self.temperature_values)-np.min(self.temperature_values))*2/3-0.5, color='green', alpha=0.60, linewidth=0.0)

            for start, end in zip(logged_nw_starts, logged_nw_ends):
                ax1.fill_between(x=[start, end], y1=0, y2=0.9, color='blue', alpha=0.60, linewidth=0.0)
                ax2.fill_between(x=[start, end], y1=-8, y2=-2.70, color='blue', alpha=0.60, linewidth=0.0)
                ax3.fill_between(x=[start, end], y1=np.min(self.temperature_values),
                                 y2=np.min(self.temperature_values)+(np.max(self.temperature_values)-np.min(self.temperature_values))/3-0.5, color='blue', alpha=0.60,
                                 linewidth=0.0)

        except (IndexError, AttributeError):
            pass

        plt.show()

    def huberty_nonwear(self):
        '''
        Calculates non-wear periods based on Huberty algorithm

        Returns:
            A dataframe with the epoched sums, epoched std and a boolean column that states whether it is less than 0.05
        '''
        len_40hz = int(len(self.x_values) * (40 / self.accelerometer_frequency))
        x_values_40hz = signal.resample(self.x_values, len_40hz)
        y_values_40hz = signal.resample(self.y_values, len_40hz)
        z_values_40hz = signal.resample(self.z_values, len_40hz)

        timestamps_1s_start = pd.date_range(self.accelerometer_start_datetime,end = self.accelerometer_endtime-datetime.timedelta(minutes=1), freq = "T")
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

        df = pd.DataFrame({"Time stamps start":timestamps_1s_start,"Time stamps end":timestamps_1s_end,"Epoched Means": epoched_means, "Epoched Std": epoched_std})
        df["Less than 0.05"] = False
        df.loc[df["Epoched Std"] <= 0.05, "Less than 0.05"] = True
        df["60 minutes?"] = False
        df.loc[df["Less than 0.05"].rolling(60).sum() == 60,"60 minutes?"] = True

        return df
