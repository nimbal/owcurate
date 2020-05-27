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

    Examples:
        To calculate the zhou nonwear algorithm you would do
        s = SensorScripts()
        s.read_accelerometer("Path/To/Accelerometer/file.edf")
        s.zhou_nonwear()
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
        self.subject_id = None # Comes from Accelerometer File

    def read_accelerometer(self, path_to_accelerometer):
        """
        Read in accelerometer values into the SensorScripts class

        Args:
            path_to_accelerometer: full path to accelerometer EDF

        Returns:
            self.accelerometer: the pyedflib read file
            self.x_values: all the data point values for the x axis
            self.y_values: all the data point values for the y axis
            self.z_values: all the data point values for the z axis
            self.accelerometer_frequency: sample rate of accelerometer sensor
            self.accelerometer_start_datetime: Start date and time of the recording
            self.accelerometer_duration: Length of recording in seconds
            self.accelerometer_endtime: End date and time of the recording
            self.accelerometer_timestamps:The time stamps that correspond with each data point
            self.subject_id: This only applies to edf's using the updated ga_to_edf conversion and only is relevant for studys with subject id's (OND05,OND07, STEPS etc...)

        """
        print("Starting accelerometer reading...")
        if not os.path.exists(path_to_accelerometer):
            raise Exception("ACCELEROMETER PATH NOT CORRECT, ACCELEROMETER NOT INITIALIZED")
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
        self.subject_id = self.accelerometer.getPatientCode()[-4:]

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

        Returns:
            self.temperature: the pyedflib read file
            self.temperature_values: all the data point values for the temperature sensor
            self.temperature_frequency: sample rate of temperature sensor
            self.temperature_start_datetime: Start date and time of the recording
            self.temperature_duration: Length of recording in seconds
            self.temperature_endtime: End date and time of the recording
            self.temperature_timestamps:The time stamps that correspond with each data point

        """
        print("Starting Temperature Reading...")
        if not os.path.exists(path_to_temperature):
            raise Exception("TEMPERATURE PATH NOT CORRECT, TEMPERATURE NOT INITIALIZED")
            return

        self.temperature = pyedflib.EdfReader(path_to_temperature)
        self.temperature_values = self.temperature.readSignal(0)
        self.temperature_frequency = self.temperature.getNSamples()[0] / self.temperature.getFileDuration()
        self.temperature_start_datetime = self.temperature.getStartdatetime()
        self.temperature_duration = self.temperature.getFileDuration()

        self.temperature_endtime = self.temperature_start_datetime + dt.timedelta(
            seconds=len(self.temperature_values) / self.temperature_frequency)
        self.temperature_timestamps = np.asarray(
            pd.date_range(self.temperature_start_datetime, self.temperature_endtime,
                          periods=len(self.temperature_values)))
        #self.subject_id = self.temperature.getPatientCode()[-4:]

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

        Returns:
            self.light: the pyedflib read file
            self.light_values: all the data point values for the light sensor
            self.light_frequency: sample rate of light sensor (currently hard coded at 0.25)
            self.light_start_datetime: Start date and time of the recording
            self.light_duration: Length of recording in seconds
            self.light_endtime: End date and time of the recording
            self.light_timestamps:The time stamps that correspond with each data point
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

        #self.subject_id = self.light.getPatientCode()[-4:]

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

        Returns:
            self.button: the pyedflib read file
            self.button_values: all the data point values for the button sensor
            self.button_frequency: sample rate of button sensor (currently hard coded at 0.25)
            self.button_start_datetime: Start date and time of the recording
            self.button_duration: Length of recording in seconds
            self.button_endtime: End date and time of the recording
            self.button_timestamps:The time stamps that correspond with each data point
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

        #self.subject_id = self.button.getPatientCode()[-4:]

        self.button.close()

        print("button Frequency: ", self.button_frequency)
        print("button Start Datetime: ", self.button_start_datetime)
        print("button Duration: ", self.button_duration)
        print("Button Successfully Initialized")

    def read_sample_nonwear_log(self, filepath):
        """
        Created by Chris Wong

        Reads self reported nonwear logs for 5 day tests done with the NiMBaL staff saved in xlsx format.


        Returns:
            a dataframe of nw_on times, nw_off times and whether or not it was removed for a structured removal

        """

        df = pd.read_excel(filepath)

        off_list = df['Off']
        on_list = df['On']
        structured_removal_list = df['Structured Removal']

        return df

    @staticmethod
    def read_OND07_nonwear_log(path):
        """

        Returns:
            df of OND07 nonwear log times for non-dominant wrists of all participants
                - column names:
                    - ID
                    - DEVICE OFF
                    - DEVICE ON
                    - ENDCOLLECTION
                    - HANDEDNESS
        Notes:
            - Must have access to the NiMBaL drive
            - The time stamps have been updated to better reflect the non-wear time by Kyle Weber through visual inspection
        """
        logs_df = pd.read_excel(path)  # Read non-wear logs into a dataframe
        logs_df["DEVICE OFF"] = pd.to_datetime(logs_df["DEVICE OFF"], format="%Y%b%d %H:%M")
        logs_df["DEVICE ON"] = pd.to_datetime(logs_df["DEVICE ON"], format="%Y%b%d %H:%M")
        return logs_df

    @staticmethod
    def read_OND06_nonwear_log(path):
        logs_df = pd.read_excel(path)  # Read non-wear logs into a dataframe
        logs_df["DEVICE OFF"] = pd.to_datetime(logs_df["DEVICE OFF"], format="%Y%b%d %H:%M")
        logs_df["DEVICE ON"] = pd.to_datetime(logs_df["DEVICE ON"], format="%Y%b%d %H:%M")
        return logs_df

    def vanhees_nonwear(self, min_number_bins = 1,bin_size = 15):
        '''
        Calculated non-wear scores based on the GGIR algorithm created by Vanhees
        https://cran.r-project.org/web/packages/GGIR/vignettes/GGIR.html#non-wear-detection
        https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0061691


        Args:
            min_number_bins: The number of consecutive bins needed for the bout to be considered valid non-wear
            bin_size: the size of the bin in minutes

        Notes:
            the window is 4x the bin size, so if the bin is 15 mins, the window that has to meet the criteria is 15*4 = 60 mins

        Returns:
            A dataframe with columns:
            - StartTime (Index): The start time of the bin
            - End Time: The end time of the bin
            - Device Worn?: Indicates whether worn (1) or not worn (0) during that bin according the the algorithm


        '''
        pd.set_option('mode.chained_assignment', None)
        print("Starting Vanhees Calculation...")
        print("Bin size =", bin_size)
        print("Min Number of Bins =", min_number_bins)

        #  Create Bins

        bins = pd.date_range(self.accelerometer_start_datetime, self.accelerometer_endtime, freq='%smin' % bin_size)

        # Create Dataframe with all the raw data in it with their respective timestamps as
        data = {"x-axis": self.x_values,
                "y-axis": self.y_values,
                "z-axis": self.z_values,
                "TimeStamps": self.accelerometer_timestamps}
        df = pd.DataFrame(data)
        df = df.set_index("TimeStamps")


        # Calculate STD and range of values in each bin
        x_binned_std = []
        y_binned_std = []
        z_binned_std = []

        x_binned_range = []
        y_binned_range = []
        z_binned_range = []

        for n in range(len(bins) - 1):
            binned_std = df.loc[bins[n]-dt.timedelta(minutes = (3/2)*bin_size):bins[n+1]+dt.timedelta(minutes = (3/2)*bin_size)].std() # Look at non-wear paper method notes to understand this line
            x_binned_std.append(binned_std[0])
            y_binned_std.append(binned_std[1])
            z_binned_std.append(binned_std[2])

            binned_range = df.loc[bins[n]-dt.timedelta(minutes = (3/2)*bin_size):bins[n+1]+dt.timedelta(minutes = (3/2)*bin_size)] # Look at non-wear paper method notes to understand this line
            x_binned_range.append(abs(max(binned_range["x-axis"])- min(binned_range["x-axis"])))
            y_binned_range.append(abs(max(binned_range["y-axis"])- min(binned_range["y-axis"])))
            z_binned_range.append(abs(max(binned_range["z-axis"])- min(binned_range["z-axis"])))

        binned_data = {"Start Time": bins[:-1],
                       "End Time": bins[1:],
                       "x-std": x_binned_std,
                       "y-std": y_binned_std,
                       "z-std": z_binned_std,
                       "x-range":x_binned_range,
                       "y-range":y_binned_range,
                       "z-range":z_binned_range}

        binned_df = pd.DataFrame(binned_data)

        def nonwear_score(row):
            std_score = 0
            if row["x-std"] < 0.013 :
                std_score += 1
            if row["y-std"] < 0.013:
                std_score += 1
            if row["z-std"] < 0.013:
                std_score += 1

            value_range_score = 0
            if row["x-range"] < 0.05:
                value_range_score +=1
            if row["y-range"] < 0.05:
                value_range_score +=1
            if row["z-range"] < 0.05:
                value_range_score +=1

            print(std_score,value_range_score)


            return std_score
        #def window_sum(row):


        binned_df["Non-wear score"] = binned_df.apply(nonwear_score, axis=1) # This applies the nonwear_score function for every row in the dataframe
        binned_df["Bin Not Worn?"] = False
        binned_df["Bin Not Worn?"].loc[binned_df["Non-wear score"] >= 2] = True

        binned_df["Bin Worn Consecutive Count"] = binned_df["Bin Not Worn?"] * (binned_df["Bin Not Worn?"].groupby((binned_df["Bin Not Worn?"] != binned_df["Bin Not Worn?"].shift()).cumsum()).cumcount() + 1)

        binned_df["Device Worn?"] = True
        binned_df["Device Worn?"].loc[binned_df["Bin Worn Consecutive Count"] >= min_number_bins] = False

        final_df = binned_df[['Start Time', 'End Time', 'Device Worn?']].copy()
        final_df = final_df.set_index("Start Time")

        return final_df

    def huberty_nonwear(self):
        '''
        INCOMPLETE, DO NOT USE.

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

    def zhou_nonwear(self, min_number_bins = 1, t0 = 26, ws=60):

        '''
        Calculated non-wear results based on the algorithm created by Shang-Ming Zhou
        https://bmjopen.bmj.com/content/5/5/e007447


        Args:
            min_number_bins: The number of consecutive 4 second bins needed for the bout to be considered valid non-wear
            t0: The threshold at which temp has to be below to be considered valid nonwear
            ws: window size in seconds

        Notes:
            we are using a forward moving window of 4s since that is how often we get temperature results. The original study by Zhou used 1s

        Returns:
            A dataframe with columnsdasdss
            StartTime (Index) The start time of the bin
            - End Time -> The end time of the bin
            - Device Worn? -> Indicates whether worn (1) or not worn (0) during that bin according the the algorithm
         '''



        # Temperature
        pd.set_option('mode.chained_assignment', None)
        zhou_df = pd.DataFrame({"Temperature Timestamps": self.temperature_timestamps,
                                "Raw Temperature Values": self.temperature_values})

        temperature_moving_average = pd.Series(self.temperature_values).rolling(
            int(ws * self.temperature_frequency)).mean()

        # Accelerometer

        zhou_accelerometer_df = pd.DataFrame({"X": self.x_values, "Y": self.y_values, "Z": self.z_values},
                                             index=self.accelerometer_timestamps)
        zhou_accelerometer_rolling_std = zhou_accelerometer_df.rolling(int(ws * self.accelerometer_frequency)).std()
        # takes the row of every next one
        binned_df = zhou_accelerometer_rolling_std.iloc[::int(self.accelerometer_frequency / self.temperature_frequency), :]

        # Combined
        temp_moving_average_list = list(temperature_moving_average.values)
        if len(temp_moving_average_list) > len(binned_df):
            temp_moving_average_list = temp_moving_average_list[:len(binned_df)]
        if len(temp_moving_average_list) < len(binned_df):
            temp_moving_average_list.append(0)
        print("LENGTH Temp list:", len(temp_moving_average_list))
        print("LENGTH BINNED 4s DF:", len(binned_df))

        binned_df["Temperature Moving Average"] = temp_moving_average_list

        # Zhou Algorithm

        not_worn = []
        end_times = []
        for index, row in binned_df.iterrows():
            end_times.append(index + dt.timedelta(seconds=4))
            if (row["Temperature Moving Average"] < t0) and (((row["X"] + row["Y"] + row["Z"]) / 3) < 0.013):
                not_worn.append(True)
            elif row["Temperature Moving Average"] >= t0:
                not_worn.append(False)
            else:
                earlier_window_temp = binned_df["Temperature Moving Average"].shift(int(ws * self.temperature_frequency)).loc[index]
                if row["Temperature Moving Average"] > earlier_window_temp:
                    not_worn.append(False)
                elif row["Temperature Moving Average"] < earlier_window_temp:
                    not_worn.append(True)
                elif row["Temperature Moving Average"] == earlier_window_temp:
                    not_worn.append(not_worn[-1])
                else:
                    not_worn.append(False)

        binned_df["Bin Not Worn?"] = not_worn
        binned_df["Bin Worn Consecutive Count"] = binned_df["Bin Not Worn?"] * (binned_df["Bin Not Worn?"].groupby((binned_df["Bin Not Worn?"] != binned_df["Bin Not Worn?"].shift()).cumsum()).cumcount() + 1)
        binned_df["Device Worn?"] = True
        binned_df["Device Worn?"].loc[binned_df["Bin Worn Consecutive Count"] >= min_number_bins] = False
        binned_df["End Time"] = end_times

        final_df = binned_df[['End Time', 'Device Worn?']].copy()

        return final_df
