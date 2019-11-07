import math
import matplotlib.pyplot as plt


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
        fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(10, 8), sharex=True)
        ax1.plot(self.x, linewidth=0.5)
        ax2.plot(self.y, linewidth=0.5)
        ax3.plot(self.z, linewidth=0.5)
