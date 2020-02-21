# Author:  Adam Vert
# Date:  January, 2020


# ======================================== IMPORTS ========================================
import pandas as pd
from ga_to_edf import *
from summary_metrics import *
import os
import pyedflib
import datetime
import numpy as np

# ======================================== FUNCTION =========================================
def folder_convert(input_dir, output_dir, device_edf=False, correct_drift=True, overwrite=False, quiet=False):
    """
    The folder_convert function takes a folder of GENEActiv files and converts them all to an edf file type following a predetermined folder structure

    Args:
        input_dir: string
            Path to directory with all the binary GENEActive files
        output_dir: string
            Path to head directory where you want all the EDF files to go ([OND05]_[GENEActiv] in Folder structure example)
        device_edf: Bool
            Do you want the function to create a device wide EDF file that stores all 5 sensors in one EDF file
        correct_drift: Bool
            Should the function correct the clock drift on the incoming data?
        overwrite: Bool
            Do you want to redo the conversion on data that has previously been converted?
        quiet: Bool
            Silence the print function?

    Examples: (change input and output paths)
        folder_convert("C:\\PATH\\TO\\INPUT\\FOLDER", "C:\\PATH\\TO\\OUTPUT\\FOLDER\\OND05_GENEActiv", correct_drift=True, overwrite = False, quiet = False)

    Returns:
        - EDF Files for all
        - A csv file list for each of the 4 parameters (Accelerometer, Temperature, Light, Button)

    """

    # Creating list of accelerometer files already converted
    accelerometer_dir = os.path.join(output_dir, "Accelerometer", "DATAFILES")
    if os.path.exists(accelerometer_dir):
        accelerometer_edf_files = [f for f in os.listdir(accelerometer_dir) if f.endswith('.edf')]
        accelerometer_files_used = [f[:-4].replace("_GENEActiv_", "_GA_").replace("_Accelerometer_","_").replace("_A_","_01_").replace("_B_","_02_") for f in accelerometer_edf_files]
    else:
        if not quiet: print("Creating Proper Directories for Accelerometer Files...")
        os.makedirs(accelerometer_dir)
        accelerometer_files_used = []

    # Creating list of Temperature files already converted
    temperature_dir = os.path.join(output_dir, "Temperature", "DATAFILES")
    if os.path.exists(temperature_dir):
        temperature_edf_files = [f for f in os.listdir(temperature_dir) if f.endswith('.edf')]
        temperature_files_used = [f[:-4].replace("_GENEActiv_", "_GA_").replace("_Temperature_","_").replace("_A_","_01_").replace("_B_","_02_") for f in temperature_edf_files]
    else:
        if not quiet: print("Creating Proper Directories for Temperature Files...")
        os.makedirs(temperature_dir)
        temperature_files_used = []

    # Creating list of Light files already converted
    light_dir = os.path.join(output_dir, "Light", "DATAFILES")
    if os.path.exists(light_dir):
        light_edf_files = [f for f in os.listdir(light_dir) if f.endswith('.edf')]
        light_files_used = [f[:-4].replace("_GENEActiv_", "_GA_").replace("_Light_","_").replace("_A_","_01_").replace("_B_","_02_") for f in light_edf_files]
    else:
        if not quiet: print("Creating Proper Directories for Light Files...")
        os.makedirs(light_dir)
        light_files_used = []

    # Creating list of Button files already converted
    button_dir = os.path.join(output_dir, "Button", "DATAFILES")
    if os.path.exists(button_dir):
        button_edf_files = [f for f in os.listdir(button_dir) if f.endswith('.edf')]
        button_files_used = [f[:-4].replace("_GENEActiv_", "_GA_").replace("_Button_","_").replace("_A_","_01_").replace("_B_","_02_") for f in button_edf_files]
    else:
        if not quiet: print("Creating Proper Directories for Button Files...")
        os.makedirs(button_dir)
        button_files_used = []
    # Creating input files list
    input_dir = os.path.abspath(input_dir)
    if not quiet: print("input dir:",input_dir)
    input_files = [f[:-4] for f in (os.listdir(input_dir)) if f.endswith('.bin')]
    if not quiet: print("input_files = ", input_files)

    if device_edf:
        device_dir = os.path.join(output_dir, "Device", "DATAFILES")
        if not os.path.exists(device_dir):
            if not quiet: print("Creating Proper Directories for Device Files...")
            os.makedirs(device_dir)
    else:
        device_dir = ""

    # Converting Files
    if not overwrite:
        new_accelerometer_files = [f for f in input_files if f not in accelerometer_files_used]
        new_temperature_files = [f for f in input_files if f not in temperature_files_used]
        new_light_files = [f for f in input_files if f not in light_files_used]
        new_button_files = [f for f in input_files if f not in button_files_used]
        new_files = np.unique(new_accelerometer_files + new_temperature_files + new_light_files + new_button_files)
        if not quiet: print("new_files to be converted: ", new_files)

        # Convert new input files to edf
        for x in new_files:
            if not quiet: print("--------------------------------------------------------------------------------------------------------------------")
            if not quiet: print("Converting " + x + ".bin...")
            ga_to_edf(input_dir + "\\" + x + ".bin", accelerometer_dir, temperature_dir, light_dir, button_dir, device_dir, device_edf,
                      correct_drift=correct_drift, quiet=quiet)

    if overwrite:
        overwrite_accelerometer_files = [f for f in input_files if f in accelerometer_files_used]
        overwrite_temperature_files = [f for f in input_files if f in temperature_files_used]
        overwrite_light_files = [f for f in input_files if f in light_files_used]
        overwrite_button_files = [f for f in input_files if f in button_files_used]
        overwrite_files = np.unique(overwrite_accelerometer_files + overwrite_temperature_files + overwrite_light_files + overwrite_button_files)
        if not quiet: print("Files that will be overwritten: ", overwrite_files)
        for x in input_files:
            if not quiet: print("--------------------------------------------------------------------------------------------------------------------")
            if not quiet: print("Converting " + x + ".bin...")
            ga_to_edf(input_dir + "\\" + x + ".bin", accelerometer_dir, temperature_dir, light_dir, button_dir, device_dir, device_edf,
                      correct_drift=correct_drift, quiet=quiet)

    if not quiet: print("Conversion Complete")

    # Create Summary Metrics and File Lists
    csv_file_list(output_dir, quiet=quiet)
    summary_metrics_csv(output_dir, quiet=quiet)




def summary_metrics_csv(path_to_head_dir, quiet = False):
    accelerometer_file_list = [f.replace("_Accelerometer_","_") for f in os.listdir(os.path.join(path_to_head_dir,"Accelerometer","DATAFILES")) if f.endswith('.edf')]
    temperature_file_list = [f.replace("_Temperature_","_") for f in os.listdir(os.path.join(path_to_head_dir,"Temperature","DATAFILES")) if f.endswith('.edf')]
    light_file_list = [f.replace("_Light_","_") for f in os.listdir(os.path.join(path_to_head_dir,"Light","DATAFILES")) if f.endswith('.edf')]
    button_file_list = [f.replace("_Button_","_") for f in os.listdir(os.path.join(path_to_head_dir,"Button","DATAFILES")) if f.endswith('.edf')]
    file_list = np.unique(accelerometer_file_list + temperature_file_list + light_file_list + button_file_list)

    data_dicts_list = []

    for file in file_list:
        accelerometer_exists = True
        temperature_exists = True
        light_exists = True
        button_exists = True
        if file not in accelerometer_file_list:
            accelerometer_exists = False
            print("WARNING ", file, " NOT IN ACCELEROMETER FOLDER")
        if file not in temperature_file_list:
            temperature_exists = False
            print("WARNING ", file, " NOT IN TEMPERATURE FOLDER")
        if file not in light_file_list:
            light_exists = False
            print("WARNING ", file, " NOT IN LIGHT FOLDER")
        if file not in button_file_list:
            button_exists = False
            print("WARNING ", file, " NOT IN BUTTON FOLDER")
        data_dicts_list.append(summary_metrics(path_to_head_dir, file, accelerometer_exists, temperature_exists, light_exists, button_exists, quiet=quiet))

    data = {}
    for k in data_dicts_list[0].keys():
        data[k] = tuple(data[k] for data in data_dicts_list)

    df = pd.DataFrame(data)

    filename = "OND05_ALL_00_GENEActiv_" + datetime.datetime.now().strftime("%Y%b%d").upper() + "_DATA.csv"
    full_path = os.path.join(path_to_head_dir, filename)

    df.to_csv(full_path, mode="w", index=False)




def csv_file_list(path_to_head_dir, quiet=False):
    # Given a path to a head directory, creates a file list for each sensor
    accelerometer_path = os.path.join(path_to_head_dir,"Accelerometer","DATAFILES")
    temperature_path = os.path.join(path_to_head_dir,"Temperature","DATAFILES")
    light_path = os.path.join(path_to_head_dir,"Light","DATAFILES")
    button_path = os.path.join(path_to_head_dir,"Button","DATAFILES")

    sensor_paths = {"Accelerometer":accelerometer_path,
                    "Temperature":temperature_path,
                    "Light":light_path,
                    "Button":button_path}

    for key in sensor_paths:
        dir_path = sensor_paths[key]
        if not quiet: print("Creating Filelist for", dir_path)
        dir_path = os.path.abspath(dir_path)
        file_list = [f for f in os.listdir(dir_path) if f.endswith('.edf')]

        #Create lists for each column of dataframe
        subjects = []
        visits = []
        dates = []
        sizes = []
        device_locations = []

        for file in file_list:
            #Read EDF
            path_to_file = os.path.join(dir_path, file)
            geneactivfile = pyedflib.EdfReader(path_to_file)

            # File Name
            file_split = file.split("_")

            # Subject
            subject = file_split[0] + "_" + file_split[1] + "_" + file_split[2]
            subjects.append(subject)

            # Patient Visit Number
            patient_visit_number = file_split[3]
            visits.append(patient_visit_number)

            # Date
            start_date = datetime.datetime.strftime(geneactivfile.getStartdatetime(), "%Y%b%d").upper()
            dates.append(start_date)

            # Site
            site = file_split[1]

            # Device Location
            device_locations.append(geneactivfile.getRecordingAdditional())

        file_list_df = pd.DataFrame(
            {'SUBJECT': subjects,
             'VISIT': visits,
             'SITE': site,
             'DATE': dates,
             'DEVICE_LOCATION': device_locations,
             'FILENAME': file_list
             })

        file_name = "OND05_ALL_00_GENEActiv_"+ key +"_"+datetime.datetime.now().strftime("%Y%b%d").upper()+"_FILELIST.csv"
        full_path = os.path.join(dir_path, file_name)
        file_list_df.to_csv(full_path, mode="w", index = False)

