# ======================================== IMPORTS
from Subject import *
from Files.Converters import *
import peakutils
from scipy.signal import butter, filtfilt
import matplotlib
import pandas as pd
import numpy as np
import sklearn
from sklearn.neighbors import KNeighborsClassifier
import tensorflow as tf
import keras
from keras.models import Sequential
from keras import layers
from sklearn import preprocessing, linear_model

# ================================================================================================
# ======================================== PREPARING DATA ========================================
# ================================================================================================
matplotlib.use("MacOSX")


# ======================================== DEFINITIONS

# ==================== Various methods for easily using filters
def bandpass_filter(dataset, lowcut, highcut, frequency, filter_order):
    # Filter characteristics
    nyquist_freq = 0.5 * frequency
    low = lowcut / nyquist_freq
    high = highcut / nyquist_freq
    b, a = butter(filter_order, [low, high], btype="band")
    y = filtfilt(b, a, dataset)
    return y


def lowpass_filter(dataset, lowcut, signal_freq, filter_order):
    """Method that creates bandpass filter to ECG data."""
    # Filter characteristics
    nyquist_freq = 0.5 * signal_freq
    low = lowcut / nyquist_freq
    b, a = butter(filter_order, low, btype="low")
    y = filtfilt(b, a, dataset)
    return y


def highpass_filter(dataset, highcut, signal_freq, filter_order):
    """Method that creates bandpass filter to ECG data."""
    # Filter characteristics
    nyquist_freq = 0.5 * signal_freq
    high = highcut / nyquist_freq
    b, a = butter(filter_order, high, btype="high")
    y = filtfilt(b, a, dataset)
    return y


# ======================================== VARIABLE DECLARATION AND INITIALIZATION

# LA, RA, LW, RW are Sensor Type objects
LA = Sensor()
RA = Sensor()
LW = Sensor()
RW = Sensor()

EDFToSensor(LA, "/Users/nimbal/Documents/KIN471/Walking/Left_Ankle/Accelerometer.EDF", "", "/Users/nimbal/Documents/KIN471/Walking/Left_Ankle/Thermometer.EDF", "/Users/nimbal/Documents/KIN471/Walking/Left_Ankle/Light.EDF", "/Users/nimbal/Documents/KIN471/Walking/Left_Ankle/Button.EDF")
EDFToSensor(RA, "/Users/nimbal/Documents/KIN471/Walking/Right_Ankle/Accelerometer.EDF", "", "/Users/nimbal/Documents/KIN471/Walking/Right_Ankle/Thermometer.EDF", "/Users/nimbal/Documents/KIN471/Walking/Right_Ankle/Light.EDF", "/Users/nimbal/Documents/KIN471/Walking/Right_Ankle/Button.EDF")
EDFToSensor(LW, "/Users/nimbal/Documents/KIN471/Walking/Left_Wrist/Accelerometer.EDF", "", "/Users/nimbal/Documents/KIN471/Walking/Left_Wrist/Thermometer.EDF", "/Users/nimbal/Documents/KIN471/Walking/Left_Wrist/Light.EDF", "/Users/nimbal/Documents/KIN471/Walking/Left_Wrist/Button.EDF")
EDFToSensor(RW, "/Users/nimbal/Documents/KIN471/Walking/Right_Wrist/Accelerometer.EDF", "", "/Users/nimbal/Documents/KIN471/Walking/Right_Wrist/Thermometer.EDF", "/Users/nimbal/Documents/KIN471/Walking/Right_Wrist/Light.EDF", "/Users/nimbal/Documents/KIN471/Walking/Right_Wrist/Button.EDF")

# LA_times, RA_times, LW_times, RW_times are arrays of times, used for indexes
LA_times = LA.generate_times(75, len(LA.accelerometer.x))
RA_times = RA.generate_times(75, len(RA.accelerometer.x))
LW_times = LW.generate_times(75, len(LW.accelerometer.x))
RW_times = RW.generate_times(75, len(RW.accelerometer.x))

# ======================================== WINDOWS TO USE FOR STARTING AND ENDING TIMES
starttimes = [datetime.datetime(year=2019, month=11, day=12, hour=14, minute=42),
              datetime.datetime(year=2019, month=11, day=12, hour=14, minute=53),
              datetime.datetime(year=2019, month=11, day=12, hour=15, minute=12),
              datetime.datetime(year=2019, month=11, day=12, hour=15, minute=26),
              datetime.datetime(year=2019, month=11, day=12, hour=15, minute=39),
              datetime.datetime(year=2019, month=11, day=12, hour=16, minute=3)]

endtimes = [datetime.datetime(year=2019, month=11, day=12, hour=14, minute=48),
            datetime.datetime(year=2019, month=11, day=12, hour=14, minute=58),
            datetime.datetime(year=2019, month=11, day=12, hour=15, minute=24),
            datetime.datetime(year=2019, month=11, day=12, hour=15, minute=32),
            datetime.datetime(year=2019, month=11, day=12, hour=15, minute=52),
            datetime.datetime(year=2019, month=11, day=12, hour=16, minute=12)]

starttimes_nonwalk = [datetime.datetime(year=2019, month=11, day=12, hour=14, minute=42),
                      datetime.datetime(year=2019, month=11, day=12, hour=14, minute=52),
                      datetime.datetime(year=2019, month=11, day=12, hour=15, minute=11),
                      datetime.datetime(year=2019, month=11, day=12, hour=15, minute=25),
                      datetime.datetime(year=2019, month=11, day=12, hour=15, minute=37),
                      datetime.datetime(year=2019, month=11, day=12, hour=16, minute=0)]

endtimes_nonwalk = [datetime.datetime(year=2019, month=11, day=12, hour=14, minute=49),
                    datetime.datetime(year=2019, month=11, day=12, hour=14, minute=59),
                    datetime.datetime(year=2019, month=11, day=12, hour=15, minute=24),
                    datetime.datetime(year=2019, month=11, day=12, hour=15, minute=33),
                    datetime.datetime(year=2019, month=11, day=12, hour=15, minute=53),
                    datetime.datetime(year=2019, month=11, day=12, hour=16, minute=12)]


# ======================================== Processing Starting Times
wrist_x = []
wrist_y = []
wrist_z = []

ankle_x = []
ankle_y = []
ankle_z = []


for i in range(len(starttimes)):
    ankle_x.extend(LA.accelerometer.x[np.where(LA_times == starttimes[i])[0][0]:np.where(LA_times == endtimes[i])[0][0]])
    ankle_y.extend(LA.accelerometer.y[np.where(LA_times == starttimes[i])[0][0]:np.where(LA_times == endtimes[i])[0][0]])
    ankle_z.extend(LA.accelerometer.z[np.where(LA_times == starttimes[i])[0][0]:np.where(LA_times == endtimes[i])[0][0]])

    ankle_x.extend(RA.accelerometer.x[np.where(RA_times == starttimes[i])[0][0]:np.where(RA_times == endtimes[i])[0][0]])
    ankle_y.extend(RA.accelerometer.y[np.where(RA_times == starttimes[i])[0][0]:np.where(RA_times == endtimes[i])[0][0]])
    ankle_z.extend(RA.accelerometer.z[np.where(RA_times == starttimes[i])[0][0]:np.where(RA_times == endtimes[i])[0][0]])

    wrist_x.extend(LW.accelerometer.x[np.where(LW_times == starttimes[i])[0][0]:np.where(LW_times == endtimes[i])[0][0]])
    wrist_y.extend(LW.accelerometer.y[np.where(LW_times == starttimes[i])[0][0]:np.where(LW_times == endtimes[i])[0][0]])
    wrist_z.extend(LW.accelerometer.z[np.where(LW_times == starttimes[i])[0][0]:np.where(LW_times == endtimes[i])[0][0]])

    wrist_x.extend(RW.accelerometer.x[np.where(RW_times == starttimes[i])[0][0]:np.where(RW_times == endtimes[i])[0][0]])
    wrist_y.extend(RW.accelerometer.y[np.where(RW_times == starttimes[i])[0][0]:np.where(RW_times == endtimes[i])[0][0]])
    wrist_z.extend(RW.accelerometer.z[np.where(RW_times == starttimes[i])[0][0]:np.where(RW_times == endtimes[i])[0][0]])


Wrist_X = []
Wrist_y = []

Ankle_X = []
Ankle_y = []

for i in range(0, len(wrist_x) - 300, 150):
    Wrist_X.append(np.array([
        wrist_x[i:i+300],
        wrist_y[i:i+300],
        wrist_z[i:i+300]
    ]).swapaxes(0, 1))
    Wrist_y.append(1)

    Ankle_X.append(np.array([
        ankle_x[i:i+300],
        ankle_y[i:i+300],
        ankle_z[i:i+300]
    ]).swapaxes(0, 1))
    Ankle_y.append(1)


# ======================================== PROCESSING NON_WEAR_TIMES
wrist_x = []
wrist_y = []
wrist_z = []

ankle_x = []
ankle_y = []
ankle_z = []

for i in range(len(starttimes_nonwalk) - 1):
    ankle_x.extend(LA.accelerometer.x[np.where(LA_times == endtimes_nonwalk[i])[0][0]:np.where(LA_times == starttimes_nonwalk[i + 1])[0][0]])
    ankle_y.extend(LA.accelerometer.y[np.where(LA_times == endtimes_nonwalk[i])[0][0]:np.where(LA_times == starttimes_nonwalk[i + 1])[0][0]])
    ankle_z.extend(LA.accelerometer.z[np.where(LA_times == endtimes_nonwalk[i])[0][0]:np.where(LA_times == starttimes_nonwalk[i + 1])[0][0]])

    ankle_x.extend(RA.accelerometer.x[np.where(RA_times == endtimes_nonwalk[i])[0][0]:np.where(RA_times == starttimes_nonwalk[i + 1])[0][0]])
    ankle_y.extend(RA.accelerometer.y[np.where(RA_times == endtimes_nonwalk[i])[0][0]:np.where(RA_times == starttimes_nonwalk[i + 1])[0][0]])
    ankle_z.extend(RA.accelerometer.z[np.where(RA_times == endtimes_nonwalk[i])[0][0]:np.where(RA_times == starttimes_nonwalk[i + 1])[0][0]])

    wrist_x.extend(LW.accelerometer.x[np.where(LW_times == endtimes_nonwalk[i])[0][0]:np.where(LW_times == starttimes_nonwalk[i + 1])[0][0]])
    wrist_y.extend(LW.accelerometer.y[np.where(LW_times == endtimes_nonwalk[i])[0][0]:np.where(LW_times == starttimes_nonwalk[i + 1])[0][0]])
    wrist_z.extend(LW.accelerometer.z[np.where(LW_times == endtimes_nonwalk[i])[0][0]:np.where(LW_times == starttimes_nonwalk[i + 1])[0][0]])

    wrist_x.extend(RW.accelerometer.x[np.where(RW_times == endtimes_nonwalk[i])[0][0]:np.where(RW_times == starttimes_nonwalk[i + 1])[0][0]])
    wrist_y.extend(RW.accelerometer.y[np.where(RW_times == endtimes_nonwalk[i])[0][0]:np.where(RW_times == starttimes_nonwalk[i + 1])[0][0]])
    wrist_z.extend(RW.accelerometer.z[np.where(RW_times == endtimes_nonwalk[i])[0][0]:np.where(RW_times == starttimes_nonwalk[i + 1])[0][0]])


for i in range(0, len(wrist_x) - 300, 150):
    Wrist_X.append(np.array([
        np.array(wrist_x[i:i+300]),
        np.array(wrist_y[i:i+300]),
        np.array(wrist_z[i:i+300])
    ]).swapaxes(0, 1))
    Wrist_y.append(0)

    Ankle_X.append(np.array([
        np.array(ankle_x[i:i+300]),
        np.array(ankle_y[i:i+300]),
        np.array(ankle_z[i:i+300])
    ]).swapaxes(0, 1))
    Ankle_y.append(0)


Wrist_X = np.array(Wrist_X)
Wrist_y = np.array(Wrist_y)

Ankle_X = np.array(Ankle_X)
Ankle_y = np.array(Ankle_y)


# ======================================== UNCOMMENT TO USE WRIST DATA
# X_train, X_test, y_train, y_test = sklearn.model_selection.train_test_split(Wrist_X, Wrist_y, test_size=0.3)

# ======================================== UNCOMMENT TO USE ANKLE DATA
X_train, X_test, y_train, y_test = sklearn.model_selection.train_test_split(Ankle_X, Ankle_y, test_size=0.3)


# ======================================== MAKING THE MODEL

model = keras.Sequential([
    keras.layers.Flatten(input_shape=(300, 3)),
    keras.layers.Dense(128, activation='relu'),
    keras.layers.Dense(10, activation='softmax')
])


model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])


# ======================================== TRAINING THE MODEL
model.fit(X_train, y_train, epochs=10)




# ======================================== TESTING THE MODEL
test_loss, test_acc = model.evaluate(X_test, y_test, verbose=2)
print(test_acc)

predictions = model.predict(X_test)

for i in range(0, len(X_test), 100):
    fig, ax = plt.subplots()
    ax.plot(X_test[i])
    fig.suptitle("Predicted: %i   Actual: %i" % (np.argmax(predictions[i]), y_test[i]))


# ======================================== VALIDATING MODEL USING SAMPLE DATA

SAMPLE_DATA = []
for i in range(0, len(LA.accelerometer.x) - 300, 300):
    SAMPLE_DATA.append(np.array([
        np.array(LA.accelerometer.x[i:i+300]),
        np.array(LA.accelerometer.y[i:i+300]),
        np.array(LA.accelerometer.z[i:i+300])
    ]).swapaxes(0, 1))

SAMPLE_DATA = np.array(SAMPLE_DATA)








