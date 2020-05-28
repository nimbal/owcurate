import pyedflib
from pathlib import Path
import os

def bittium_folder_convert(input_dir, output_dir):
    # TODO: option to overwrites files

    # create dirs
    accel_dir = os.path.join(output_dir, "Accelerometer", "DATAFILES")
    accel_channels = [1 ,2 ,3]
    Path(accel_dir).mkdir(parents=True, exist_ok=True)

    ecg_dir = os.path.join(output_dir, "ECG", "DATAFILES")
    ecg_channels = [0]
    Path(ecg_dir).mkdir(parents=True, exist_ok=True)

    for f in os.listdir(input_dir):
        if not f.lower().endswith('.edf'):
            continue
        pyedflib.highlevel.drop_channels(f, edf_target=accel_dir,to_keep=accel_channels)
        pyedflib.highlevel.drop_channels(f, edf_target=ecg_dir,to_keep=ecg_channels)
