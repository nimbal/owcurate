# Author:  Adam Vert
# Date:  January, 2020


# ======================================== IMPORTS ========================================
import numpy as np
from GENEActivFile import *
import pyedflib
import os


# ======================================== FUNCTION =========================================
def device_summary_metrics(path_to_edf, quiet=False):
    '''
    Extracts summary metrics from a device level .edf
    '''
    if not quiet: print("Creating Device Summary Metrics...")
    geneactivfile = pyedflib.EdfReader(path_to_edf)

    # Subject ID
    subjectID = geneactivfile.getPatientCode()
    if not quiet: print("Subject ID: ", subjectID)

    # Serial Number
    serial_number = geneactivfile.getEquipment()
    if not quiet: print("Serial Number: ", serial_number)

    # File Name
    file_name = os.path.basename(path_to_edf)
    file_name_split = file_name.split("_")
    if not quiet: print("File Name:", file_name)

    # Start DateTime
    start_datetime = geneactivfile.getStartdatetime()
    if not quiet: print("start time: ", start_datetime)

    # Collection Duration (in days)
    collection_duration = geneactivfile.getFileDuration() / 24 / 60 / 60
    if not quiet: print("Collection Duration: ", collection_duration)

    # Data Collection Site
    data_collection_site = file_name_split[1]
    if not quiet: print("data collection site: ", data_collection_site)

    # Patient Visit Number
    patient_visit_number = file_name_split[3]
    if not quiet: print("Patient Visit Number", patient_visit_number)

    # Device Location
    device_location = geneactivfile.getPatientName()
    if not quiet: print("device location:", device_location)

    # Frequencies
    frequencies = []
    for c in range(geneactivfile.signals_in_file):
        frequencies.append(geneactivfile.samplefrequency(c))
    accelerometer_frequency = frequencies[0]
    temperature_frequency = frequencies[3]
    light_frequency = frequencies[4]
    button_frequency = frequencies[5]
    if not quiet: print("Frequencies:", accelerometer_frequency, temperature_frequency, light_frequency, button_frequency)

    # Mean and STD Calculations
    x_accelerometer_data = geneactivfile.readSignal(0)
    y_accelerometer_data = geneactivfile.readSignal(1)
    z_accelerometer_data = geneactivfile.readSignal(2)
    magnitude_accelerometer_data = np.sqrt(x_accelerometer_data ** 2 + y_accelerometer_data ** 2 + z_accelerometer_data ** 2)
    temperature_data = geneactivfile.readSignal(3)
    light_data = geneactivfile.readSignal(4)
    button_data = geneactivfile.readSignal(5)

    x_accelerometer_mean = np.average(x_accelerometer_data)
    y_accelerometer_mean = np.average(y_accelerometer_data)
    z_accelerometer_mean = np.average(z_accelerometer_data)
    magnitude_accelerometer_mean = np.average(magnitude_accelerometer_data)
    temperature_mean = np.average(temperature_data)
    light_mean = np.average(light_data)
    button_mean = np.average(button_data)

    x_accelerometer_std = np.std(x_accelerometer_data)
    y_accelerometer_std = np.std(y_accelerometer_data)
    z_accelerometer_std = np.std(z_accelerometer_data)
    magnitude_accelerometer_std = np.std(magnitude_accelerometer_data)
    temperature_std = np.std(temperature_data)
    light_std = np.std(light_data)
    button_std = np.std(button_data)

    if not quiet: print("Mean Values")
    if not quiet: print("Accelerometer (x,y,z,magnitude): ", x_accelerometer_mean, y_accelerometer_mean, z_accelerometer_mean,
                        magnitude_accelerometer_mean)
    if not quiet: print("Temperature: ", temperature_mean)
    if not quiet: print("Light: ", light_mean)
    if not quiet: print("Button: ", button_mean)
    if not quiet: print("")

    if not quiet: print("STD Values")
    if not quiet: print("Accelerometer (x,y,z,magnitude): ", x_accelerometer_std, y_accelerometer_std, z_accelerometer_std,
                        magnitude_accelerometer_std)
    if not quiet: print("Temperature: ", temperature_std)
    if not quiet: print("Light: ", light_std)
    if not quiet: print("Button: ", button_std)
    if not quiet: print("")

    # Clock Drift
    clock_drift = float(geneactivfile.getRecordingAdditional())
    clock_drift_rate = float(clock_drift / geneactivfile.file_duration)
    if not quiet: print("clock drift (seconds): ", clock_drift)
    if not quiet: print("clock drift rate: ", clock_drift_rate)
    if not quiet: print("")

    device_summary_metrics_list = [subjectID, patient_visit_number,data_collection_site, serial_number, file_name, start_datetime, collection_duration,
                                   device_location, accelerometer_frequency, magnitude_accelerometer_mean, magnitude_accelerometer_std,
                                   x_accelerometer_mean,
                                   x_accelerometer_std, y_accelerometer_mean, y_accelerometer_std, z_accelerometer_mean, z_accelerometer_std,
                                   temperature_frequency, temperature_mean, temperature_std, light_frequency, light_mean, light_std, button_frequency,
                                   button_mean, button_std, clock_drift, clock_drift_rate]

    return device_summary_metrics_list


def accelerometer_summary_metrics(path_to_edf, quiet=False):
    '''
    Extracts summary metrics from an accelerometer .edf
    '''
    if not quiet: print("Creating Accelerometer Summary Metrics...")
    print(path_to_edf)
    geneactivfile = pyedflib.EdfReader(path_to_edf)

    # Subject ID
    subjectID = geneactivfile.getPatientCode()
    if not quiet: print("Subject ID: ", subjectID)

    # Serial Number
    serial_number = geneactivfile.getEquipment()
    if not quiet: print("Serial Number: ", serial_number)

    # File Name
    file_name = os.path.basename(path_to_edf)
    file_name_split = file_name.split("_")
    if not quiet: print("File Name:", file_name)

    # Start DateTime
    start_datetime = geneactivfile.getStartdatetime()
    if not quiet: print("start time: ", start_datetime)

    # Collection Duration (in days)
    collection_duration = geneactivfile.getFileDuration() / 24 / 60 / 60
    if not quiet: print("Collection Duration: ", collection_duration)

    # Data Collection Site
    data_collection_site = file_name_split[1]
    if not quiet: print("data collection site: ", data_collection_site)

    # Patient Visit Number
    patient_visit_number = file_name_split[3]
    if not quiet: print("Patient Visit Number", patient_visit_number)

    # Device Location
    device_location = geneactivfile.getPatientName()
    if not quiet: print("device location:", device_location)

    # Frequency
    accelerometer_frequency = geneactivfile.samplefrequency(0)
    if not quiet: print("Accelerometer Frequency:", accelerometer_frequency)

    # Mean and STD Calculations
    x_accelerometer_data = geneactivfile.readSignal(0)
    y_accelerometer_data = geneactivfile.readSignal(1)
    z_accelerometer_data = geneactivfile.readSignal(2)
    magnitude_accelerometer_data = np.sqrt(x_accelerometer_data ** 2 + y_accelerometer_data ** 2 + z_accelerometer_data ** 2)
    x_accelerometer_mean = np.average(x_accelerometer_data)
    y_accelerometer_mean = np.average(y_accelerometer_data)
    z_accelerometer_mean = np.average(z_accelerometer_data)
    magnitude_accelerometer_mean = np.average(magnitude_accelerometer_data)
    x_accelerometer_std = np.std(x_accelerometer_data)
    y_accelerometer_std = np.std(y_accelerometer_data)
    z_accelerometer_std = np.std(z_accelerometer_data)
    magnitude_accelerometer_std = np.std(magnitude_accelerometer_data)

    if not quiet: print("Mean Values")
    if not quiet: print("Accelerometer (x,y,z,magnitude): ", x_accelerometer_mean, y_accelerometer_mean, z_accelerometer_mean,
                        magnitude_accelerometer_mean)
    if not quiet: print("")

    if not quiet: print("STD Values")
    if not quiet: print("Accelerometer (x,y,z,magnitude): ", x_accelerometer_std, y_accelerometer_std, z_accelerometer_std,
                        magnitude_accelerometer_std)
    if not quiet: print("")

    # Clock Drift
    clock_drift = float(geneactivfile.getRecordingAdditional())
    clock_drift_rate = float(clock_drift / geneactivfile.file_duration)
    if not quiet: print("clock drift (seconds): ", clock_drift)
    if not quiet: print("clock drift rate: ", clock_drift_rate)
    if not quiet: print("")

    accelerometer_summary_metrics_list = [subjectID, patient_visit_number,data_collection_site, serial_number, file_name, start_datetime, collection_duration,
                                          device_location, accelerometer_frequency, magnitude_accelerometer_mean,
                                          magnitude_accelerometer_std, x_accelerometer_mean, x_accelerometer_std, y_accelerometer_mean,
                                          y_accelerometer_std,
                                          z_accelerometer_mean, z_accelerometer_std, clock_drift, clock_drift_rate]

    return accelerometer_summary_metrics_list


def temperature_summary_metrics(path_to_edf, quiet=False):
    '''
    Extracts summary metrics from a temperature .edf
    '''
    if not quiet: print("Creating Temperature Summary Metrics...")
    geneactivfile = pyedflib.EdfReader(path_to_edf)

    # Subject ID
    subjectID = geneactivfile.getPatientCode()
    if not quiet: print("Subject ID: ", subjectID)

    # Serial Number
    serial_number = geneactivfile.getEquipment()
    if not quiet: print("Serial Number: ", serial_number)

    # File Name
    file_name = os.path.basename(path_to_edf)
    file_name_split = file_name.split("_")
    if not quiet: print("File Name:", file_name)

    # Start DateTime
    start_datetime = geneactivfile.getStartdatetime()
    if not quiet: print("start time: ", start_datetime)

    # Collection Duration (in days)
    collection_duration = geneactivfile.getFileDuration() / 24 / 60 / 60
    if not quiet: print("Collection Duration: ", collection_duration)

    # Data Collection Site
    data_collection_site = file_name_split[1]
    if not quiet: print("data collection site: ", data_collection_site)

    # Patient Visit Number
    patient_visit_number = file_name_split[3]
    if not quiet: print("Patient Visit Number", patient_visit_number)

    # Device Location
    device_location = geneactivfile.getPatientName()
    if not quiet: print("device location:", device_location)

    # Frequency
    temperature_frequency = geneactivfile.samplefrequency(0)
    if not quiet: print("Temperature Frequency:", temperature_frequency)

    # Mean and STD Calculations
    temperature_data = geneactivfile.readSignal(0)
    temperature_mean = np.average(temperature_data)
    temperature_std = np.std(temperature_data)

    if not quiet: print("Mean Values")
    if not quiet: print("Temperature: ", temperature_mean)
    if not quiet: print("")

    if not quiet: print("STD Values")
    if not quiet: print("Temperature: ", temperature_std)
    if not quiet: print("")

    # Clock Drift
    clock_drift = float(geneactivfile.getRecordingAdditional())
    clock_drift_rate = float(clock_drift / geneactivfile.file_duration)
    if not quiet: print("clock drift (seconds): ", clock_drift)
    if not quiet: print("clock drift rate: ", clock_drift_rate)
    if not quiet: print("")

    temperature_summary_metrics_list = [subjectID, patient_visit_number, data_collection_site, serial_number, file_name, start_datetime, collection_duration, device_location, temperature_frequency, temperature_mean, temperature_std, clock_drift,
                                        clock_drift_rate]

    return temperature_summary_metrics_list


def light_summary_metrics(path_to_edf, quiet=False):
    '''
    Extracts summary metrics from a light .edf
    '''
    if not quiet: print("Creating Light Summary Metrics...")
    geneactivfile = pyedflib.EdfReader(path_to_edf)

    # Subject ID
    subjectID = geneactivfile.getPatientCode()
    if not quiet: print("Subject ID: ", subjectID)

    # Serial Number
    serial_number = geneactivfile.getEquipment()
    if not quiet: print("Serial Number: ", serial_number)

    # File Name
    file_name = os.path.basename(path_to_edf)
    file_name_split = file_name.split("_")
    if not quiet: print("File Name:", file_name)

    # Start DateTime
    start_datetime = geneactivfile.getStartdatetime()
    if not quiet: print("start time: ", start_datetime)

    # Collection Duration (in days)
    collection_duration = geneactivfile.getFileDuration() / 24 / 60 / 60
    if not quiet: print("Collection Duration: ", collection_duration)

    # Data Collection Site
    data_collection_site = file_name_split[1]
    if not quiet: print("data collection site: ", data_collection_site)

    # Patient Visit Number
    patient_visit_number = file_name_split[3]
    if not quiet: print("Patient Visit Number", patient_visit_number)

    # Device Location
    device_location = geneactivfile.getPatientName()
    if not quiet: print("device location:", device_location)

    # Frequency
    light_frequency = geneactivfile.samplefrequency(0)
    if not quiet: print("Light Frequency:", light_frequency)

    # Mean and STD Calculations
    light_data = geneactivfile.readSignal(0)
    light_mean = np.average(light_data)
    light_std = np.std(light_data)

    if not quiet: print("Mean Values")
    if not quiet: print("Light: ", light_mean)
    if not quiet: print("")

    if not quiet: print("STD Values")
    if not quiet: print("Light: ", light_std)
    if not quiet: print("")

    # Clock Drift
    clock_drift = float(geneactivfile.getRecordingAdditional())
    clock_drift_rate = float(clock_drift / geneactivfile.file_duration)
    if not quiet: print("clock drift (seconds): ", clock_drift)
    if not quiet: print("clock drift rate: ", clock_drift_rate)
    if not quiet: print("")

    light_summary_metrics_list = [subjectID, patient_visit_number, data_collection_site,serial_number, file_name, start_datetime, collection_duration, device_location,
                                  light_frequency, light_mean, light_std, clock_drift, clock_drift_rate]

    return light_summary_metrics_list


def button_summary_metrics(path_to_edf, quiet=False):
    '''
    Extracts summary metrics from a button .edf
    '''
    if not quiet: print("Creating Button Summary Metrics...")
    geneactivfile = pyedflib.EdfReader(path_to_edf)

    # Subject ID
    subjectID = geneactivfile.getPatientCode()
    if not quiet: print("Subject ID: ", subjectID)

    # Serial Number
    serial_number = geneactivfile.getEquipment()
    if not quiet: print("Serial Number: ", serial_number)

    # File Name
    file_name = os.path.basename(path_to_edf)
    file_name_split = file_name.split("_")
    if not quiet: print("File Name:", file_name)

    # Start DateTime
    start_datetime = geneactivfile.getStartdatetime()
    if not quiet: print("start time: ", start_datetime)

    # Collection Duration (in days)
    collection_duration = geneactivfile.getFileDuration() / 24 / 60 / 60
    if not quiet: print("Collection Duration: ", collection_duration)

    # Data Collection Site
    data_collection_site = file_name_split[1]
    if not quiet: print("data collection site: ", data_collection_site)

    # Patient Visit Number
    patient_visit_number = file_name_split[3]
    if not quiet: print("Patient Visit Number", patient_visit_number)

    # Device Location
    device_location = geneactivfile.getPatientName()
    print("device location:", device_location)

    # Frequency
    button_frequency = geneactivfile.samplefrequency(0)
    if not quiet: print("Button Frequency:", button_frequency)

    # Mean and STD Calculations
    button_data = geneactivfile.readSignal(0)
    button_mean = np.average(button_data)
    button_std = np.std(button_data)
    if not quiet: print("Mean Value")
    if not quiet: print("Button: ", button_mean)
    if not quiet: print("")

    if not quiet: print("STD Value")
    if not quiet: print("Button: ", button_std)
    if not quiet: print("")

    # Clock Drift
    clock_drift = float(geneactivfile.getRecordingAdditional())
    clock_drift_rate = float(clock_drift / geneactivfile.file_duration)
    if not quiet: print("clock drift (seconds): ", clock_drift)
    if not quiet: print("clock drift rate: ", clock_drift_rate)
    if not quiet: print("")

    button_summary_metrics_list = [subjectID, patient_visit_number, data_collection_site,serial_number, file_name, start_datetime, collection_duration,
                                   device_location, button_frequency, button_mean, button_std, clock_drift, clock_drift_rate]

    return button_summary_metrics_list
