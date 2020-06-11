import pyedflib
import shutil
import os
from pathlib import Path
from tqdm import tqdm

def update_GA_to_OND06(data_pkg_dir, subplatform_code='GNAC'):
    location_mapping = { 'LA': 'LAnkle', 'RA': 'RAnkle', 'LW': 'LWrist', 'RW': 'RWrist', 'AA': 'Aid' }
    edf_files = list(Path(data_pkg_dir).rglob("*.[eE][dD][fF]"))
    for f in tqdm(edf_files,desc='Updating Files:', total=len(edf_files)):
        file_dir ,filename = os.path.split(f)
        filename, ext = filename.split('.')

        s_filename = filename.split('_')
        new_filename = '_'.join(s_filename[:3] + [subplatform_code,
                                        s_filename[-2].upper(),
                                        location_mapping[s_filename[-1]] if s_filename[-1] in location_mapping else s_filename[-1]]) + '.%s' % ext
        new_f = os.path.join(file_dir, new_filename)
        os.rename(f, new_f)
        update_GA_edf_header(new_f)
        


def update_GA_edf_header(edf_file, update_location=None):
    location_mapping = { b'LA': b'LAnkle', b'RA': b'RAnkle', b'LW': b'LWrist', b'RW': b'RWrist', b'AA': b'Aid' }

    with open(edf_file, "r+b") as f:
        header_info = f.read(256)

        # Update device location
        recording_additionals = header_info[88:168].rstrip().split(b' ')
        recording_additionals[-1] = location_mapping[recording_additionals[-1]] if recording_additionals[-1] in location_mapping else recording_additionals[-1]
        recording_additionals[-1] = update_location if update_location else recording_additionals[-1]
        new_recording_additional = b' '.join(recording_additionals).ljust(80)[:80]

        # Deletes visit number
        patient_info = header_info[8:88].rstrip().split(b' ')
        patient_info[-1] = b'X'
        new_patient_info = b' '.join(patient_info).ljust(80)[:80]

        header_info = header_info[:88] + new_recording_additional + header_info[168:]
        header_info = header_info[:8] + new_patient_info + header_info[88:]

        assert len(header_info) == 256

        f.seek(0)
        f.write(header_info)

update_GA_to_OND06(r'E:\nimbal\data\OND06\ProcessedEDF')