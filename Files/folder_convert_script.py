# Author:  Adam Vert
# Date:  January, 2020


# ======================================== IMPORTS ========================================
import numpy as np
import pandas as pd
import csv
import os
import sys
from ga_to_edf import ga_to_edf


# ======================================== FUNCTION =========================================
def folder_convert(input_dir, output_dir, correct_drift=True, overwrite=False, quiet=False):
    """
    The folder_convert function takes a folder of GENEActiv files and converts them all to an edf file type following the predetermined folder structure

    Args:
        input_dir: string
            Path to directory with all the binary GENEActive files
        output_dir: string
            Path to head directory where you want all the EDF files to go ([ONDO5]_[GENEActiv] in Folder structure example)
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
        - A csv file list for each of the 4 parameters (Accel, Tenmp, Light, Button)

    """
    # Creating list of accel files already converted
    accel_dir = os.path.join(output_dir, "Accel", "DATAFILES")
    if os.path.exists(accel_dir):
        accel_edf_files = [f for f in os.listdir(accel_dir) if f.endswith('.EDF')]
        accel_files_used = [f[:-10].replace("_GENEActiv_", "_GA_") for f in accel_edf_files]
        if not quiet: print("accel_files_used  = ", accel_files_used)
    else:
        if not quiet: print("Creating Proper Directories for Accel Files...")
        os.makedirs(accel_dir)
        accel_files_used = []

    # Creating list of Temp files already converted
    temp_dir = os.path.join(output_dir, "Temp", "DATAFILES")
    if os.path.exists(temp_dir):
        temp_edf_files = [f for f in os.listdir(temp_dir) if f.endswith('.EDF')]
        temp_files_used = [f[:-9].replace("_GENEActiv_", "_GA_") for f in temp_edf_files]
        if not quiet: print("temp_files_used   = ", temp_files_used)
    else:
        if not quiet: print("Creating Proper Directories for Temp Files...")
        os.makedirs(temp_dir)
        temp_files_used = []

    # Creating list of Light files already converted
    light_dir = os.path.join(output_dir, "Light", "DATAFILES")
    if os.path.exists(light_dir):
        light_edf_files = [f for f in os.listdir(light_dir) if f.endswith('.EDF')]
        light_files_used = [f[:-10].replace("_GENEActiv_", "_GA_") for f in light_edf_files]
        if not quiet: print("light_files_used  = ", light_files_used)
    else:
        if not quiet: print("Creating Proper Directories for Light Files...")
        os.makedirs(light_dir)
        light_files_used = []

    # Creating list of Button files already converted
    button_dir = os.path.join(output_dir, "Button", "DATAFILES")
    if os.path.exists(button_dir):
        button_edf_files = [f for f in os.listdir(button_dir) if f.endswith('.EDF')]
        button_files_used = [f[:-11].replace("_GENEActiv_", "_GA_") for f in button_edf_files]
        if not quiet: print("button_files_used = ", button_files_used)
    else:
        if not quiet: print("Creating Proper Directories for Button Files...")
        os.makedirs(button_dir)
        button_files_used = []

    # Creating input files list
    input_dir = os.path.abspath(input_dir)
    if not quiet: print(input_dir)
    input_files = [f[:-4] for f in (os.listdir(input_dir)) if f.endswith('.bin')]
    if not quiet: print("input_files       = ", input_files)

    # Converting Files
    if not overwrite:
        new_accel_files = [f for f in input_files if f not in accel_files_used]
        new_temp_files = [f for f in input_files if f not in temp_files_used]
        new_light_files = [f for f in input_files if f not in light_files_used]
        new_button_files = [f for f in input_files if f not in button_files_used]
        new_files = np.unique(new_accel_files + new_temp_files + new_light_files + new_button_files)
        if not quiet: print("new_files = ", new_files)

        # Convert new input files to edf
        for x in new_files:
            if not quiet: print("Converting " + x + ".bin" + "...")
            ga_to_edf(input_dir + "\\" + x + ".bin", accel_dir, temp_dir, light_dir, button_dir, correct_drift=correct_drift, quiet=quiet)

    if overwrite:
        overwrite_accel_files = [f for f in input_files if f in accel_files_used]
        overwrite_temp_files = [f for f in input_files if f in temp_files_used]
        overwrite_light_files = [f for f in input_files if f in light_files_used]
        overwrite_button_files = [f for f in input_files if f in button_files_used]
        overwrite_files = np.unique(overwrite_accel_files + overwrite_temp_files + overwrite_light_files + overwrite_button_files)
        if not quiet: print("Files that will be overwritten: ", overwrite_files)
        for x in input_files:
            ga_to_edf(input_dir + "\\" + x + ".bin", accel_dir, temp_dir, light_dir, button_dir, correct_drift=correct_drift, quiet=quiet)

    if not quiet: print("Conversion Complete")

    # CSV File List
    for x in [accel_dir, temp_dir, light_dir, button_dir]:
        csv_file_list(x, "OND05_GENEActiv_FILELIST.csv", quiet = quiet)


def csv_file_list(dir_path, file_name, quiet=False):
    if not quiet: print("Creating Filelist for", dir_path)
    dir_path = os.path.abspath(dir_path)
    file_list = [f for f in os.listdir(dir_path) if f.endswith('.EDF')]
    file_df = pd.DataFrame(file_list)
    full_path = os.path.join(dir_path, file_name)
    file_df.to_csv(full_path, header=["File_names"], mode="w")
