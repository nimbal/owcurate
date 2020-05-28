import pyedflib
from pathlib import Path
import os

def bittium_folder_convert(input_dir, output_dir):
    # TODO: option to NOT overwrites files

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
        f_path = os.path.join(input_dir, f)
        pyedflib.highlevel.drop_channels(f_path, edf_target=os.path.join(accel_dir, f), to_keep=accel_channels)
        pyedflib.highlevel.drop_channels(f_path, edf_target=os.path.join(ecg_dir, f), to_keep=ecg_channels)

input_dir=r'E:\nimbal\data\OND06\raw_bittium_1039'
output_dir=r'E:\nimbal\data\OND06\processed_bittium_1039'
bittium_folder_convert(input_dir, output_dir)