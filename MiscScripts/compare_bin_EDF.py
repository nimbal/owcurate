# Author:  Adam Vert
# Date:  February, 2020


# ======================================== IMPORTS ========================================
import pandas as pd
from Files.GENEActivFile import *
import numpy as np
import os
import pyedflib
import datetime


# ======================================== FUNCTION =========================================
def bin_edf_compare(bin_file, edf_file, sensor):
    pd.set_option('display.max_columns', 500)
    pd.set_option('display.width', 1000)
    # Read Bin File
    geneactivfile = GENEActivFile(bin_file)
    geneactivfile.read(correct_drift=True)
    # Read EDF File
    edf_file = pyedflib.EdfReader(edf_file)
    remove_n_points = round(geneactivfile.data["sample_rate"] * (1000000 - geneactivfile.file_info["start_time"].microsecond) / 1000000)

    if sensor == 'accelerometer':
        edf_x = edf_file.readSignal(0)
        edf_y = edf_file.readSignal(1)
        edf_z = edf_file.readSignal(2)

        bin_x = geneactivfile.data["x"][remove_n_points:]
        bin_y = geneactivfile.data["y"][remove_n_points:]
        bin_z = geneactivfile.data["z"][remove_n_points:]

        print("edf:",len(edf_x), "bin:",len(bin_x))
        print(edf_x)
        print(bin_x)
        if len(edf_x) != len(bin_x) :  #EdfWriter adds signals to make the final signal equal 1 second, this removes those extra signals so it is comparable with the .bin data
            extra_edf_data_len_x = edf_file.getSampleFrequency(0)-(len(bin_x) % edf_file.getSampleFrequency(0))
            edf_x = edf_x[:-extra_edf_data_len_x]
            extra_edf_data_len_y = edf_file.getSampleFrequency(1)-(len(bin_y) % edf_file.getSampleFrequency(1))
            edf_y = edf_y[:-extra_edf_data_len_y]
            extra_edf_data_len_z = edf_file.getSampleFrequency(2)-(len(bin_z) % edf_file.getSampleFrequency(2))
            edf_z = edf_z[:-extra_edf_data_len_z]
        print("edf:",len(edf_x), "bin:",len(bin_x))
        df = pd.DataFrame({"edf_x": edf_x, "bin_x": bin_x, "edf_y": edf_y, "bin_y": bin_y, "edf_z": edf_z, "bin_z": bin_z})
        df['Difference_x'] = abs(df['edf_x'] - df['bin_x'])
        df['Difference_y'] = abs(df['edf_y'] - df['bin_y'])
        df['Difference_z'] = abs(df['edf_z'] - df['bin_z'])
        print(df)
        print("")

        print("x_avg_diff: ", np.average(df['Difference_x']))
        print("y_avg_diff: ", np.average(df['Difference_y']))
        print("z_avg_diff: ", np.average(df['Difference_z']))

        print("")
        print("x_max_diff: ", np.max(df['Difference_x']))
        print("y_max_diff: ", np.max(df['Difference_y']))
        print("z_max_diff: ", np.max(df['Difference_z']))


    if sensor == 'temperature':
        edf_temperature = edf_file.readSignal(0)

        bin_temperature = geneactivfile.data["temperature"]

    if sensor == 'light':
        edf_temperature = edf_file.readSignal(0)

        bin_temperature = geneactivfile.data["light"][remove_n_points:]

    if sensor == 'button':
        edf_temperature = edf_file.readSignal(0)

        bin_temperature = geneactivfile.data["button"][remove_n_points:]

    if sensor == 'device':
        edf_x = edf_file.readSignal(0)
        edf_y = edf_file.readSignal(1)
        edf_z = edf_file.readSignal(2)

        bin_x = geneactivfile.data["x"][remove_n_points:]
        bin_y = geneactivfile.data["y"][remove_n_points:]
        bin_z = geneactivfile.data["z"][remove_n_points:]

        edf_temperature = edf_file.readSignal(0)
        bin_temperature = geneactivfile.data["temperature"]

        edf_temperature = edf_file.readSignal(0)
        bin_temperature = geneactivfile.data["light"][remove_n_points:]

        edf_temperature = edf_file.readSignal(0)
        bin_temperature = geneactivfile.data["button"][remove_n_points:]



bin_edf_compare(r"C:\Users\ahvert\PycharmProjects\owcurate\Data Files DO NOT PUSH\Chris Data\OND01_WTL_Chris_1_GA_LAnkle.bin",
                r"C:\Users\ahvert\PycharmProjects\owcurate\Data Files DO NOT PUSH\Chris Data\Accelerometer\DATAFILES\OND01_WTL_Chris_1_GENEActiv_Accelerometer_LAnkle.edf",
                "accelerometer")
bin_edf_compare("O:\Data\OND05\Raw device data\GENEActiv\OND05_SWP_1006_01_GA_LAnkle.bin",r"C:\Users\ahvert\Desktop\OND05_GENEActiv Test\Accelerometer\DATAFILES\OND05_SWP_1006_01_GENEActiv_Accelerometer_LAnkle.edf", "accelerometer")

def edf_integrity_check(edf_path, binary_path):
    """
    to verify that the data in the edf and bin files are the same
    """

    geneactivfile = GENEActivFile(binary_path)
    geneactivfile.read()

    # get EDF data
    edf_data = pyedflib.EdfReader(edf_path)
    clock_drift = edf_data.getRecordingAdditional()
    body_location = edf_data.getPatientName()
    extraction_time = edf_data.getPatientAdditional()
    subject_id = edf_data.getPatientCode()
    serial_num = edf_data.getEquipment()
    start_date = edf_data.getStartdatetime()
    print("Clock Drift: ", clock_drift)
    print("Body Location: ", body_location)
    print("Extraction Time: ", extraction_time)
    print("Subject ID: ", subject_id)
    print("Serial Number: ", serial_num)
    print("Start Date: ", start_date)


    print("")
    print("")

    # Get binary file data
    bin_clock_drift = geneactivfile.file_info["clock_drift"]
    bin_body_location = geneactivfile.file_info["device_location"]
    bin_extraction_time = geneactivfile.file_info["extract_time"]
    bin_subject_id = geneactivfile.file_info["subject_id"]
    bin_serial_num = geneactivfile.file_info["serial_num"]
    bin_start_date = geneactivfile.file_info["start_time"]
    print("Bin Clock Drift: ", bin_clock_drift)
    print("Bin Body Location: ", bin_body_location)
    print("Bin Extraction Time: ", bin_extraction_time)
    print("Bin Subject ID: ", bin_subject_id)
    print("Bin Serial Number: ", bin_serial_num)
    print("Bin Start Date: ", bin_start_date)

    # Compare data
    bad_match = 0
    if str(clock_drift) != str(bin_clock_drift):
        print("**WARNING, clock_drift VALUES DON'T MATCH")
        print("EDF CLOCK DRIFT: ", clock_drift)
        print("BIN CLOCK DRIFT: ", bin_clock_drift)
        bad_match += 1

    if str(body_location) != str(bin_body_location.replace("_", " ")):
        print("**WARNING, body_location VALUES DON'T MATCH")
        print("EDF BODY LOCATION: ", body_location)
        print("BIN BODY LOCATION: ", bin_body_location)
        bad_match += 1

    if str(extraction_time) != str(bin_extraction_time):
        print("**WARNING, extraction_time VALUES DON'T MATCH")
        print("EDF EXTRACTION TIME: ", extraction_time)
        print("BIN EXTRACTION TIME: ", bin_extraction_time)
        bad_match += 1

    if str(subject_id) != str(bin_subject_id):
        print("**WARNING, subject_id VALUES DON'T MATCH")
        print("EDF SUBJECT ID: ", subject_id)
        print("BIN SUBJECT ID: ", bin_subject_id)
        bad_match += 1

    if str(serial_num) != str(bin_serial_num):
        print("**WARNING, serial_num VALUES DON'T MATCH")
        print("EDF SERIAL NUMBER: ", subject_id)
        print("BIN SERIAL NUMBER: ", bin_subject_id)
        bad_match += 1

    if str(start_date + datetime.timedelta(0,0.5)) != str(bin_start_date):
        print("**WARNING, start_date VALUES DON'T MATCH")
        print("EDF START DATE: ", start_date)
        print("BIN START DATE: ", bin_start_date)
        bad_match += 1

    if bad_match ==0: print("NO ERRORS")


    print("Test Complete with ", bad_match, "bad matches.")
