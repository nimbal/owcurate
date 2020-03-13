# Created by Kyle Weber

from datetime import datetime
import numpy as np
import math


class EpochAccel:

    def __init__(self, raw_data=None, epoch_len=15):

        self.epoch_len = epoch_len

        self.svm = []
        self.timestamps = None

        self.epoch_from_raw(raw_data=raw_data)

        # Loads epoched data from existing file
        if self.from_processed:
            self.epoch_from_processed()

    def epoch_from_raw(self, raw_data):

        # Calculates epochs if from_processed is False
        print("\n" + "Epoching using raw data...")

        self.timestamps = raw_data.timestamps[::self.epoch_len * raw_data.sample_rate]

        try:
            vm = raw_data.vm
        except AttributeError:
            # Calculates gravity-subtracted vector magnitude
            raw_data.vm = [round(abs(math.sqrt(math.pow(raw_data.x[i], 2) + math.pow(raw_data.y[i], 2) +
                                               math.pow(raw_data.z[i], 2)) - 1), 5) for i in range(len(raw_data.x))]

        # Calculates activity counts
        for i in range(0, len(raw_data.vm), int(raw_data.sample_rate * self.epoch_len)):

            if i + self.epoch_len * raw_data.sample_rate > len(raw_data.vm):
                break

            vm_sum = sum(raw_data.vm[i:i + self.epoch_len * raw_data.sample_rate])

            # Bug handling: when we combine multiple EDF files they are zero-padded
            # When vector magnitude is calculated, it is 1
            # Any epoch where the values were all the epoch length * sampling rate (i.e. a VM of 1 for each data point)
            # becomes 0
            if vm_sum == self.epoch_len * raw_data.sample_rate:
                vm_sum = 0

            self.svm.append(round(vm_sum, 5))

        print("Epoching complete.")