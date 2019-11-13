import math
import matplotlib.pyplot as plt
from scipy.signal import butter,lfilter


class Accelerometer:
    def __init__(self):
        self.frequency = None
        self.start_time = None
        self.x = None
        self.y = None
        self.z = None
        self.n_samples = None
        self.svms = []

    def calculate_svms(self):
        for i in range(len(self.x)):
            self.svms.append(math.sqrt(math.pow(self.x[i], 2) + math.pow(self.y[i], 2) + math.pow(self.z[i], 2)) - 1)

    def plot_triaxial(self):
        """
        Plots the data for easy visual inspection

        Returns:

        """
        fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(10, 8), sharex=True)
        ax1.plot(self.x, linewidth=0.5)
        ax2.plot(self.y, linewidth=0.5)
        ax3.plot(self.z, linewidth=0.5)

    def find_steps(self):
        """
        Finds all steps (at index of "step registration")
        Steps to filtering for step detection are:
        1. Differentiate with respect to 3rd next index
        2. Bandpass filter with boundaries (low=15, high=25, order=3)
        3. Full wave rectify (Absolute value)
        4. Lowpass filter with (low=3, order=3)

        Step detection itself consists of:
        1. TODO: Running peakutils on sliding window
        2. TODO: Find overlapping gaps and

        Returns:
        list of indices
        """
        def bandpass_filter(dataset, lowcut, highcut, filter_order):
            """
            Method that filters data with bandpass filter

            Args:
                dataset: numpy.ndarray
                    Array of samples to be filtered
                lowcut: float
                    Lowcut frequency
                highcut: float
                    Highcut frequency
                filter_order: int
                    Order fo the filter to be applied

            Returns: numpy.ndarray
                Filtered array
            """
            # Filter characteristics
            nyquist_freq = 0.5 * self.frequency
            low = lowcut / nyquist_freq
            high = highcut / nyquist_freq
            b, a = butter(filter_order, [low, high], btype="band")
            y = lfilter(b, a, dataset)
            return y

        def lowpass_filter(dataset, lowcut, signal_freq, filter_order):
            """Method that creates bandpass filter to ECG data."""
            # Filter characteristics
            nyquist_freq = 0.5 * signal_freq
            low = lowcut / nyquist_freq
            b, a = butter(filter_order, low, btype="low")
            y = lfilter(b, a, dataset)
            return y






