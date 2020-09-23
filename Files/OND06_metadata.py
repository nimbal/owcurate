import pyedflib
import datetime
import isodate
import pandas as pd
import os


def create_filelist_csv(datapkg_dir):

    accel_dir = os.path.join(datapkg_dir, "Accelerometer", "DATAFILES")
    ecg_dir = os.path.join(datapkg_dir, "ECG", "DATAFILES")

    sensor_dirs = [accel_dir, ecg_dir]

    for sensor_dir in sensor_dirs:
        subjects = []
        visits = []
        sites = []
        dates = []
        # fileparts = []
        filenames = []
        filelist = [f for f in os.listdir(sensor_dir) if f.lower().endswith('.edf')]
        filenum = 0
        
        for f in filelist:
            
            filenum = filenum + 1
            print("File", filenum, "of", len(filelist))
            
            edf_path = os.path.join(sensor_dir, f)
            edf_header = pyedflib.highlevel.read_edf_header(edf_path)

            f_name = os.path.splitext(f)[0]
            f_split = f_name.split('_')
            subjects.append('_'.join(f_split[:3]))
            visits.append('01')
            sites.append(f_split[1])
            dates.append(edf_header['startdate'].strftime("%Y%b%d").upper())
            # fileparts.append(f_split[5] if len(f_split) > 5 else '')
            filenames.append(f)

        file_list_df = pd.DataFrame(
            {'SUBJECT': subjects,
             'VISIT': visits,
             'SITE': sites,
             'DATE': dates,
             # 'FILEPART': fileparts,
             'FILENAME': filenames
             })

        file_list_df = file_list_df.sort_values(by=["SUBJECT", "VISIT", "FILENAME"], ignore_index=True)
        filelist_path = os.path.join(sensor_dir, 'OND06_ALL_01_SNSR_BITF_%s_2020MAY31_FILELIST.csv' % sensor_dir.split(os.sep)[-2].upper())
        file_list_df.to_csv(filelist_path, index=False)


def create_data_csv(datapkg_dir):

    # Accel and ecg dir have the same files subjects, so only looking at accel files
    accel_dir = os.path.join(datapkg_dir, "Accelerometer", "DATAFILES")
    ecg_dir = os.path.join(datapkg_dir, "ECG", "DATAFILES")

    filelist = [file.replace('ACCELEROMETER', 'PLACEHOLDER').replace('ECG', 'PLACEHOLDER') for file in (os.listdir(accel_dir) + os.listdir(ecg_dir)) if file.lower().endswith('.edf')]
    filelist = list(set(filelist))
    filelist = [f for f in filelist if f.lower().endswith('.edf')]

    subjects = []
    visits = []
    sites = []
    dates = []
    fileparts = []
    device_ids = []
    start_times = []
    collection_duration_datetime = []
    accelerometer_sample_rate = []
    ecg_sample_rate = []

    filenum = 0

    for f in filelist:

        filenum = filenum + 1
        print("File", filenum, "of", len(filelist))

        accel_edf_path = os.path.join(accel_dir, f.replace('PLACEHOLDER', 'ACCELEROMETER'))
        ecg_edf_path = os.path.join(ecg_dir, f.replace('PLACEHOLDER', 'ECG'))
        accel_edf_header = pyedflib.highlevel.read_edf_header(accel_edf_path) if os.path.exists(accel_edf_path) else None
        ecg_edf_header = pyedflib.highlevel.read_edf_header(ecg_edf_path) if os.path.exists(ecg_edf_path) else None

        header = accel_edf_header if accel_edf_header else ecg_edf_header

        f_name = os.path.splitext(f)[0]
        f_split = f_name.split('_')
        subjects.append('_'.join(f_split[:3]))
        visits.append('01')
        sites.append(f_split[1])
        dates.append(header['startdate'].strftime("%Y%b%d").upper())
        fileparts.append(f_split[5] if len(f_split) > 5 else '')
        start_times.append(header['startdate'].strftime("%H:%M:%S"))
        device_ids.append(accel_edf_header['equipment'].split(' ')[1])

        duration = datetime.timedelta(seconds=header['Duration'])
        collection_duration_datetime.append(str(isodate.duration_isoformat(duration, 'P%dDT%HH%MM%SS')))
        accelerometer_sample_rate.append(accel_edf_header['SignalHeaders'][0]['sample_rate'] if accel_edf_header else 'N/A')
        ecg_sample_rate.append(ecg_edf_header['SignalHeaders'][0]['sample_rate'] if ecg_edf_header else 'N/A')

    summary_metrics_list = pd.DataFrame({"SUBJECT": subjects,
                                         "VISIT": visits,
                                         "SITE": sites,
                                         "DATE": dates,
                                         "FILEPART": fileparts,
                                         "DEVICE_ID": device_ids,  # should be in the header
                                         "START_TIME": start_times,
                                         "COLLECTION_DURATION": collection_duration_datetime,
                                         "ACCELEROMETER_SAMPLE_RATE": accelerometer_sample_rate,
                                         "ECG_SAMPLE_RATE": ecg_sample_rate})

    summary_metrics_list = summary_metrics_list.sort_values(by=["SUBJECT", "VISIT", "FILEPART"], ignore_index=True)
    summary_path = os.path.join(datapkg_dir, 'OND06_ALL_01_SNSR_BITF_2020MAY31_DATA.csv')
    summary_metrics_list.to_csv(summary_path, index=False)
