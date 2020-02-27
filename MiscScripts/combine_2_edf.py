# Adam Vert
# Feb 2020


############################# Imports ##########################################################################################################
import os

import pyedflib
import numpy as np
import pandas as pd
from scipy import signal
import datetime


################################################################################################################################################
def combine_edf(path1, path2, output_path):
    '''

    Args:
        path1: Full path to EDF1
        path2: Full path to EDF2
        output_path: Full path to where you want the combined edf outputted

    Returns:
        An edf with the data points and time stamps combined from EDF1 and EDF2

    Notes:
        Both files must have the same sample rate and
    '''
    #  Read EDF's
    edf_a = pyedflib.EdfReader(path1)
    edf_b = pyedflib.EdfReader(path2)

    #  Find order of EDF's
    if edf_a.getStartdatetime() < edf_b.getStartdatetime():
        edf_1 = edf_a
        edf_2 = edf_b
    else:
        edf_1 = edf_b
        edf_2 = edf_a

    #  Get Durations
    edf_1_duration = edf_1.getFileDuration()
    edf_2_duration = edf_2.getFileDuration()

    # Get Signal Headers
    sig_labels_1 = edf_1.getSignalLabels()
    sig_labels_2 = edf_2.getSignalLabels()
    if not np.array_equal(sig_labels_1, sig_labels_2):
        print(sig_labels_1)
        print(sig_labels_2)
        print("ERROR: FILES HAVE DIFFERENT SIGNALS")
        return

    # Get Signal values
    data1 = []
    data2 = []
    for n in range(len(sig_labels_1)):
        data1.append(edf_1.readSignal(n))
        data2.append(edf_2.readSignal(n))

    data1 = np.array(data1)
    data2 = np.array(data2)

    # Get Frequencies
    freq_1 = edf_1.getSampleFrequencies()
    freq_2 = edf_2.getSampleFrequencies()

    if not np.array_equal(freq_1, freq_2):
        for n in range(len(freq_1)):
            if freq_1[n] > freq_2[n]:
                freq_1[n] = freq_2[n]
                data1[n] = signal.resample(data1[n], edf_1_duration * freq_2[n])
            elif freq_2[n] > freq_1[n]:
                freq_1[n] = freq_2[n]
                len(data2[n])
                data2[n] = signal.resample(data2[n], edf_2_duration * freq_1[n])
                len(data2[n])

    #  Calculate end times
    edf_1_endtime = edf_1.getStartdatetime() + datetime.timedelta(seconds=edf_1_duration)
    edf_2_endtime = edf_2.getStartdatetime() + datetime.timedelta(seconds=edf_2_duration)

    #  Get time difference
    print((edf_2_endtime - edf_1.getStartdatetime()).total_seconds())
    time_diff = edf_2.getStartdatetime() - edf_1_endtime
    time_diff = time_diff.seconds
    if edf_2.getStartdatetime() < edf_1_endtime: #  If end time over lap with start time, return
        print("ERROR, SAMPLES OVERLAP")
        return

    #  Make data set
    data_final = data1
    for n in range(len(freq_1)):
        data_final[n] = np.append(data_final[n],[0]*(time_diff*freq_1[n]))
        data_final[n] = np.append(data_final[n], data2[n])

    print(edf_a.getHeader())
    print(edf_a.getSignalHeaders())

    # Write EDF
    header = edf_a.getHeader()
    signal_headers = edf_a.getSignalHeaders()
    pyedflib.highlevel.write_edf(edf_file = os.path.join(output_path,"combined_edf.edf"), signals = data_final, signal_headers=signal_headers, header=header, digital=False)



#combine_edf(r"C:\Users\ahvert\PycharmProjects\owcurate\Data Files DO NOT PUSH\Chris Data\Accelerometer\DATAFILES\OND01_WTL_Chris_00_GENEActiv_Accelerometer_LWrist.edf",r"C:\Users\ahvert\PycharmProjects\owcurate\Data Files DO NOT PUSH\Chris Data\Accelerometer\DATAFILES\OND01_WTL_Chris_00_GENEActiv_Accelerometer_RWrist.edf",r"C:\Users\ahvert\PycharmProjects\owcurate\Data Files DO NOT PUSH")
#combine_edf(r"C:\Users\ahvert\PycharmProjects\owcurate\Data Files DO NOT PUSH\OND07_WTL_3029_01_BF\09-06-10.EDF",r"C:\Users\ahvert\PycharmProjects\owcurate\Data Files DO NOT PUSH\OND07_WTL_3029_01_BF\14-01-18.EDF",r"C:\Users\ahvert\PycharmProjects\owcurate\Data Files DO NOT PUSH")
#combine_edf(r"O:\Data\OND07\Raw data\Bittium\OND07_WTL_3027_01_BF\10-09-38.EDF",r"O:\Data\OND07\Raw data\Bittium\OND07_WTL_3027_01_BF\12-09-17.EDF",r"O:\Student_Projects\Kyle Weber")