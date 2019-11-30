# ====================================================================================================
# DAVID DING
# NOVEMBER 29TH 2019
# PYTHON IMPLEMENTATION OF VAN HEES SLEEP DETECTION ALGORITHM WITHIN THE NIMBAL LAB
# ====================================================================================================


# ======================================== IMPORTS
from Files.Converters import *
from Sensor import *
from Subject import *
import statistics


class SleepIntervals:
    # ======================================== VARIABLE DECLARATION AND INITIALIZATION
    def __init__(self):
        self.S = Sensor()
        self.path = ""
        self.rolling_x = []
        self.rolling_y = []
        self.rolling_z = []
        self.angles = []
        self.avg_angles = []
        self.angles_diff = []
        
        self.window_len = 0


    def load_edf(self, path_to_accelerometer):
        self.path = path_to_accelerometer
        EDFToSensor(self.S, path_to_accelerometer, "", "", "", "")



    def VanHees(self):
        """
        Step 1 of the Van Hees Algorithm

        Returns:

        """
        self.window_len = self.S.accelerometer.frequency * 5

        # "where ax, ay, az are the median values of the three orthogonally positioned raw acceleration
        # sensors derived based on a rolling five second time window"
        for i in range(0, len(self.S.accelerometer.x) - self.window_len):
            self.rolling_x.append(statistics.median(self.S.accelerometer.x[i: i + self.window_len]))
            self.rolling_y.append(statistics.median(self.S.accelerometer.y[i: i + self.window_len]))
            self.rolling_z.append(statistics.median(self.S.accelerometer.z[i: i + self.window_len]))

        # "angle = tan^-1 (az / sqrt(ax^2 + ay^2)) * 180 / pi
        for i in range(len(self.rolling_x)):
            self.angles.append(math.atan(self.rolling_z[i] /
                                         math.sqrt(math.pow(self.rolling_x[i], 2) +
                                                   math.pow(self.rolling_y[i], 2))) * 180 / math.pi)

        # "Next, estimated arm angles were averaged per 5 second epoch"
        for i in range(0, len(self.angles), self.window_len):
            self.avg_angles.append(statistics.mean(self.angles[i:i + self.window_len]))

        # Change in angles to determine "periods of time during which there was non change larger than 5 degrees
        # over the least 5 minutes
        for i in range(0, len(self.avg_angles), self.window_len):
            self.angles_diff.append(self.avg_angles[i+1] - self.avg_angles[i])

        fig, (ax1, ax2, ax3) = plt.subplots(3, 1, sharex=True)

        ax1.plot(self.S.accelerometer.x)
        ax2.plot([self.window_len * i for i in range(len(self.avg_angles))], self.avg_angles)
        ax3.plot([self.window_len * i for i in range(len(self.angles_diff))], self.angles_diff)





