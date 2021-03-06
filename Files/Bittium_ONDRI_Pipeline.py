import pyedflib
from pathlib import Path
import datetime
import isodate
import pandas as pd
import numpy as np
import os
from tqdm import tqdm


class Bittium_ONDRI_Pipeline():
    """
    Converts Raw Bittium files into DATA Packages following BrainCODE standards
    """

    def __init__(self, input_dir, output_dir):
        # TODO: option to NOT overwrites files

        # create dirs
        accel_dir = os.path.join(output_dir, "Accelerometer", "DATAFILES")
        accel_channels = [1, 2, 3]
        Path(accel_dir).mkdir(parents=True, exist_ok=True)

        ecg_dir = os.path.join(output_dir, "ECG", "DATAFILES")
        ecg_channels = [0]
        Path(ecg_dir).mkdir(parents=True, exist_ok=True)

        for f in tqdm(os.listdir(input_dir), total=len(os.listdir(input_dir))):
            if not f.lower().endswith('.edf'):
                continue

            f_path = os.path.join(input_dir, f)
            with open(f_path, "r+b") as read_file:
                header_info = read_file.read(256)

            ecg_target = os.path.join(ecg_dir, self.update_filename(f, 'ECG'))
            accel_target = os.path.join(accel_dir, self.update_filename(f, 'ACCELEROMETER'))
            pyedflib.highlevel.drop_channels(f_path, edf_target=accel_target, to_keep=accel_channels)
            pyedflib.highlevel.drop_channels(f_path, edf_target=ecg_target, to_keep=ecg_channels)

            self.update_header(accel_target, header_info)
            self.update_header(ecg_target, header_info)

            self.update_accel_signal_header(accel_target)
            self.update_ecg_signal_header(ecg_target)

        self.create_filelist_csv(output_dir)
        self.create_data_csv(output_dir)

    @staticmethod
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

    @staticmethod
    def update_header(device_edf_filepath, header_info):
        header_info = header_info[:256]

        with open(device_edf_filepath, "r+b") as f:
            output_header = f.read(256)

            subject = '_'.join(os.path.split(device_edf_filepath)[1].split('_')[:3])
            patient_info = str.encode(' '.join([subject, 'X', 'X', 'X', 'X']).ljust(80)[:80])

            start_date = header_info[88:168].rstrip().split(b' ')[1]
            recording_additional = header_info[88:168].rstrip().split(b' ')[-1]
            equipment = b'Bittium_' + dict([x.split(b'=') for x in recording_additional.split(b'_')])[b'SER']
            recording_info = b' '.join([b'Startdate', start_date, b'X', b'X', equipment, b'X']).ljust(80)[:80]
            reserved = b'EDF+C'.ljust(44)[:44]

            header_info = header_info[:8] + patient_info + header_info[88:]  # updates patient info
            header_info = header_info[:88] + recording_info + header_info[168:]  # updates recording additional
            header_info = header_info[:184] + output_header[184:192] + header_info[192:]  # updates counted bytes in headers
            header_info = header_info[:192] + reserved + header_info[236:]  # updates reserved
            header_info = header_info[:248] + output_header[-8:]  # updates number of channels

            f.seek(0)
            f.write(header_info)

    @staticmethod
    def update_accel_signal_header(device_edf_filepath):
        with open(device_edf_filepath, "r+b") as f:
            output_header = f.read(256)
            num_signals = int(output_header[-4:])

            signal_label = b'Accelerometer x'.ljust(16) + b'Accelerometer y'.ljust(16) + b'Accelerometer z'.ljust(16)
            f.seek(256)
            f.write(signal_label)

            transducer_type = b'accelerometer'.ljust(80) + b'accelerometer'.ljust(80) + b'accelerometer'.ljust(80)
            f.seek(256 + 16 * num_signals)
            f.write(transducer_type)

    @staticmethod
    def update_ecg_signal_header(device_edf_filepath):
        with open(device_edf_filepath, "r+b") as f:
            output_header = f.read(256)
            num_signals = int(output_header[-4:])

            transducer_type = b'FastFix electrode'.ljust(80)
            f.seek(256 + 16 * num_signals)
            f.write(transducer_type)

    @staticmethod
    def create_filelist_csv(datapkg_dir):
        accel_dir = os.path.join(datapkg_dir, "Accelerometer", "DATAFILES")
        ecg_dir = os.path.join(datapkg_dir, "ECG", "DATAFILES")

        sensor_dirs = [accel_dir, ecg_dir]

        for sensor_dir in sensor_dirs:
            subjects = []
            visits = []
            sites = []
            dates = []
            filenames = []
            for f in os.listdir(sensor_dir):
                if not f.lower().endswith('.edf'):
                    continue
                edf_path = os.path.join(sensor_dir, f)
                edf_header = pyedflib.highlevel.read_edf_header(edf_path)

                f_split = f.split('_')
                subjects.append('_'.join(f_split[:3]))
                visits.append('01')
                sites.append(f_split[1])
                dates.append(edf_header['startdate'].strftime("%Y%b%d").upper())
                filenames.append(f)

            file_list_df = pd.DataFrame(
                {'SUBJECT': subjects,
                 'VISIT': visits,
                 'SITE': sites,
                 'DATE': dates,
                 'FILENAME': filenames
                 })
            file_list_df = file_list_df.sort_values(by=["SUBJECT"], ignore_index=True)
            filelist_path = os.path.join(sensor_dir, 'OND06_ALL_01_SNSR_BITF_%s_2020MAY31_FILELIST.csv' % sensor_dir.split(os.sep)[-2].upper())
            file_list_df.to_csv(filelist_path, index=False)

    @staticmethod
    def create_data_csv(datapkg_dir):
        # Accel and ecg dir have the same files subjects, so only looking at accel files
        accel_dir = os.path.join(datapkg_dir, "Accelerometer", "DATAFILES")
        ecg_dir = os.path.join(datapkg_dir, "ECG", "DATAFILES")

        filelist = [file.replace('ACCELEROMETER', 'PLACEHOLDER').replace('ECG', 'PLACEHOLDER') for file in (os.listdir(accel_dir) + os.listdir(ecg_dir)) if file.lower().endswith('.edf')]
        filelist = list(set(filelist))
        subjects = []
        visits = []
        sites = []
        dates = []
        device_ids = []
        start_times = []
        collection_duration_datetime = []
        accelerometer_sample_rate = []
        ecg_sample_rate = []

        for f in filelist:
            if not f.lower().endswith('.edf'):
                continue
            accel_edf_path = os.path.join(accel_dir, f.replace('PLACEHOLDER', 'ACCELEROMETER'))
            ecg_edf_path = os.path.join(ecg_dir, f.replace('PLACEHOLDER', 'ECG'))
            accel_edf_header = pyedflib.highlevel.read_edf_header(accel_edf_path) if os.path.exists(accel_edf_path) else None
            ecg_edf_header = pyedflib.highlevel.read_edf_header(ecg_edf_path) if os.path.exists(ecg_edf_path) else None

            header = accel_edf_header if accel_edf_header else ecg_edf_header

            f_split = f.split('_')
            subjects.append('_'.join(f_split[:3]))
            visits.append('01')
            sites.append(f_split[1])
            dates.append(header['startdate'].strftime("%Y%b%d").upper())
            start_times.append(header['startdate'].strftime("%H:%M:%S"))
            device_ids.append(accel_edf_header['equipment'])

            duration = datetime.timedelta(seconds=header['Duration']())
            collection_duration_datetime.append(str(isodate.duration_isoformat(duration, 'P%dDT%HH%MM%SS')))
            accelerometer_sample_rate.append(accel_edf_header['SignalHeaders'][0]['sample_rate'] if accel_edf_header else 'N/A')
            ecg_sample_rate.append(ecg_edf_header['SignalHeaders'][0]['sample_rate'] if ecg_edf_header else 'N/A')

        summary_metrics_list = pd.DataFrame({"SUBJECT": subjects,
                                             "VISIT": visits,
                                             "SITE": sites,
                                             "DATE": dates,
                                             "DEVICE_ID": device_ids,  # should be in the header
                                             "START_TIME": start_times,
                                             "COLLECTION_DURATION": collection_duration_datetime,
                                             "ACCELEROMETER_SAMPLE_RATE": accelerometer_sample_rate,
                                             "ECG_SAMPLE_RATE": ecg_sample_rate})
        summary_metrics_list = summary_metrics_list.sort_values(by=["SUBJECT"], ignore_index=True)
        summary_path = os.path.join(datapkg_dir, 'OND06_ALL_01_SNSR_BITF_2020MAY31_DATA.csv')
        summary_metrics_list.to_csv(summary_path, index=False)

    @staticmethod
    def merge_files(edf_path1, edf_path2):
        # checks if headers of both files are the same
        file1 = pyedflib.EdfReader(edf_path1)
        file2 = pyedflib.EdfReader(edf_path2)
        assert file1.getPatientCode() == file2.getPatientCode()
        assert file1.getSignalHeaders() == file2.getSignalHeaders()

        first = file1 if file1.getStartdatetime() < file2.getStartdatetime() else file2
        second = file1 if not file1.getStartdatetime() < file2.getStartdatetime() else file2
        num_sigs = first.signals_in_file

        new_edf = pyedflib.EdfWriter('test.edf', num_sigs)
        new_edf.setHeader(first.getHeader())

        samples = []

        for i in range(num_sigs):
            dp_between = ((first.getStartdatetime() + datetime.timedelta(seconds=first.getFileDuration())) - second.getStartdatetime()) * first.getSampleFrequency(i)
            begin = first.readSignal(i)
            fill = np.array([0] * dp_between)
            end = second.readSignal(i)
            new_channel = np.concatenate([begin, fill, end])

            samples.append(new_channel)
            new_edf.setSignalHeader(first.getSignalHeader(i))

        new_edf.writeSamples(samples)
        new_edf.close()
