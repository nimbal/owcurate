# ======================================== IMPORTS ========================================
from Sensor.Accelerometer import *
from Sensor.Thermometer import *
from Sensor.Light import *
from Sensor.Button import *
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import datetime
import statistics


# Sensor class adds a layer of modularity between sensor and person
# This class hopes to solve multi-sensor but uni-device problems such as nonwear
class Sensor:
    def __init__(self):
        self.metadata = {}
        self.accelerometer = None
        self.thermometer = None
        self.ecg = None
        self.light = None
        self.button = None
        self.non_wear_starts = None
        self.non_wear_ends = None

    def init_accelerometer(self):
        self.accelerometer = Accelerometer()

    def init_thermometer(self):
        self.thermometer = Thermometer()

    def init_light(self):
        self.light = Light()

    def init_button(self):
        self.button = Button()

    def generate_times(self, frequency, length):
        start_time = self.metadata["start_time"]
        return np.array([start_time + datetime.timedelta(seconds=i/frequency) for i in range(length)])


    def plot_accelerometer(self):
        fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(10, 8), sharex=True)

    def non_wear_accel_temp(self, mins1=3, mins2=4):

        # Checking for uninitialized values
        if self.accelerometer is None:
            raise Exception("Accelerometer has not been initialized")

        if self.thermometer is None:
            raise Exception("Thermometer has not been initialized")

        if len(self.accelerometer.svms) == 0:
            raise Exception("SVMS have not been yet calculated")

        flattened_svms = np.zeros(len(self.accelerometer.svms))

        for i in range(len(self.accelerometer.svms)):
            if self.accelerometer.svms[i] > 0.2:
                flattened_svms[i] = self.accelerometer.svms[i]

        start_array = []
        end_array = []
        curr_stat = False

        for i in range(len(flattened_svms)):
            if flattened_svms[i] == 0 and not curr_stat:
                start_array.append(i)
                curr_stat = True

            if flattened_svms[i] > 0 and curr_stat:
                end_array.append(i)
                curr_stat = False

        # Take out the first and last entries since there is a chance the sensor was not on the person
        start_array = start_array[1:-2]
        end_array = end_array[1:-1]

        new_start = []
        new_end = []
        for i in range(len(start_array) - 1):
            if end_array[i] - start_array[i] > mins1 * 60 * 300:
                new_start.append(start_array[i])
                new_end.append(end_array[i])
        print("After Duration check: %i gaps remaining" % len(new_start))

        # Overlapping Window Check
        pre_process_start = []
        pre_process_end = []
        for i in range(len(new_start) - 1):
            if new_end[i + 1] >= new_start[i]:
                pre_process_start.append(new_start[i])
                pre_process_end.append(new_end[i])
        print("After Overlapping Window Checks: %i gaps remaining" % len(pre_process_start))

        processed_start = []
        processed_end = []
        for i in range(len(pre_process_start) - 1):
            if pre_process_start[i + 1] - pre_process_end[i] > mins2 * 60 * 300:
                processed_start.append(pre_process_start[i])
                processed_end.append(pre_process_end[i])
        print("After Ending Window Check: %i gaps remaining" % len(processed_start))

        non_wear_start = []
        non_wear_end = []
        curr_temps = []

        for i in range(len(processed_start)):
            start_index = processed_start[i] // 300
            end_index = processed_end[i] // 300
            indices = np.array([j for j in range(start_index, end_index, 5)])
            curr_temps = np.array(self.thermometer.temperatures[start_index:end_index:5])
            m = (statistics.mean(curr_temps) * statistics.mean(indices) - statistics.mean(curr_temps * indices))

            if m > 20:
                non_wear_start.append(processed_start[i])
                non_wear_end.append(processed_end[i])

        self.non_wear_starts = non_wear_start
        self.non_wear_ends = non_wear_end
