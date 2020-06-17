import pyedflib
from pathlib import Path
from datetime import datetime
import pyedflib
import os


def bittium_folder_convert(input_dir, output_dir):
    # TODO: option to NOT overwrites files

    # create dirs
    accel_dir = os.path.join(output_dir, "Accelerometer", "DATAFILES")
    accel_channels = [1, 2, 3]
    Path(accel_dir).mkdir(parents=True, exist_ok=True)

    ecg_dir = os.path.join(output_dir, "ECG", "DATAFILES")
    ecg_channels = [0]
    Path(ecg_dir).mkdir(parents=True, exist_ok=True)

    for f in os.listdir(input_dir):
        if not f.lower().endswith('.edf'):
            continue

        f_path = os.path.join(input_dir, f)
        with open(f_path, "r+b") as read_file:
            header_info = read_file.read(256)

        print(f)
        ecg_target = os.path.join(ecg_dir, update_filename(f, 'ECG'))
        accel_target = os.path.join(accel_dir, update_filename(f, 'ACCELEROMETER'))
        pyedflib.highlevel.drop_channels(f_path, edf_target=accel_target, to_keep=accel_channels)
        pyedflib.highlevel.drop_channels(f_path, edf_target=ecg_target, to_keep=ecg_channels)

        update_header(accel_target, header_info)
        update_header(ecg_target, header_info)


def update_filename(filename, device):
    filename, ext = filename.split('.')[0], filename.split('.')[-1]
    s_filename = filename.split('_')
    subject = '_'.join(s_filename[:3])
    subplatform_code = 'BITF'

    filename_list = [subject, subplatform_code, device]
    if len(s_filename) == 8:
        filename_list.append(s_filename[-1])

    new_filename = '_'.join(filename_list)
    return '%s.%s' % (new_filename, ext)


def update_header(device_edf_filepath, header_info):
    header_info = header_info[:256]
    with open(device_edf_filepath, "r+b") as f:
        f.seek(0)
        f.write(header_info)


def create_filelist_csv(datapkg_dir):
    accel_dir = os.path.join(datapkg_dir, "Accelerometer", "DATAFILES")
    ecg_dir = os.path.join(datapkg_dir, "ECG", "DATAFILES")

    subjects = []
    visits = []
    sites = []
    dates = []
    device_locations = []
    filenames = []

    for f in os.listdir(accel_dir):
        if not f.lower().endswith('.edf'):
            continue
        edf_path = os.path.join(accel_dir, f)
        edf_header = pyedflib.highlevel.read_edf_header(edf_path)

        f_split = f.split('_')
        subjects.append('_'.join(f_split[:2]))
        visits.append(f_split[3])
        sites.append(f_split[1])
        dates.append(edf_header['startdate'].strftime("%Y%b%d").upper())
        devie_locations.append(f_split[-1])
        filenames.append(f)

    file_list_df = pd.DataFrame(
        {'SUBJECT': subjects,
         'VISIT': visits,
         'SITE': sites,
         'DATE': dates,
         'DEVICE_LOCATION': device_locations,
         'FILENAME': filenames
         })


def create_data_csv(datapkg_dir):
    # Accel and ecg dir have the same files subjects, so only looking at accel files
    accel_dir = os.path.join(datapkg_dir, "Accelerometer", "DATAFILES")
    ecg_dir = os.path.join(datapkg_dir, "ECG", "DATAFILES")

    subjects = []
    visits = []
    sites = []
    dates = []
    device_locations = []
    start_times = []
    collection_duration_datetime = []
    accelerometer_sample_rate = []
    ecg_sample_rate = []

    for f in os.listdir(accel_dir):
        if not f.lower().endswith('.edf'):
            continue
        accel_edf_path = os.path.join(accel_dir, f)
        ecg_edf_path = os.path.join(ecg_dir, f.replace('ACCELEROMETER', 'ECG'))
        accel_edf_header = pyedflib.highlevel.read_edf_header(accel_edf_path)
        ecg_edf_header = pyedflib.highlevel.read_edf_header(ecg_edf_path) if os.path.exists(ecg_edf_path) else None

        f_split = f.split('_')
        subjects.append('_'.join(f_split[:2]))
        visits.append(f_split[3])
        sites.append(f_split[1])
        dates.append(accel_edf_header['startdate'].strftime("%Y%b%d").upper())
        device_locations.append(f_split[-1])
        start_times.append(accel_edf_header['startdate'].strftime("%H:%M:%S"))

        duration = datetime.timedelta(seconds=accel_edf_header['Duration']())
        collection_duration_datetime.append(str(isodate.duration_isoformat(duration, 'P%dDT%HH%MM%SS')))
        accelerometer_sample_rate.append(accel_edf_header['sample_rate'] if accel_edf_header['sample_rate'] else 'N/A')
        ecg_sample_rate.append(ecg_edf_header['sample_rate'] if ecg_edf_header['sample_rate'] else 'N/A')

    summary_metrics_list = {"SUBJECT": subject,
                            "VISIT": patient_visit_number,
                            "SITE": data_collection_site,
                            "DATE": dates,
                            "DEVICE_LOCATION": device_locations,
                            # "DEVICE_ID": serial_number, # should be in the header
                            "START_TIME": start_times,
                            "COLLECTION_DURATION": collection_duration_datetime,
                            "ACCELEROMETER_SAMPLE_RATE": '{:.3f}'.format(accelerometer_sample_rate),
                            "ECG_SAMPLE_RATE": '{:.3f}'.format(ecg_sample_rate)}


input_dir = r'/Users/matt/Documents/coding/nimbal/data/bittium/raw'
output_dir = r'/Users/matt/Documents/coding/nimbal/data/bittium/processed'
bittium_folder_convert(input_dir, output_dir)
