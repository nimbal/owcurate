from SensorScripts import *
import os
import numpy as np
import pandas as pd
from tqdm import tqdm
from pathlib import Path
import matplotlib.pyplot as plt
import datetime


def export_nw_times(accel_path, temp_path):
    s = SensorScripts()
    s.read_accelerometer(accel_path)
    s.read_temperature(temp_path)
    zhou_df = s.zhou_nonwear(use_updated_alg=True)
    zhou_df = zhou_df.loc[zhou_df["Device Worn?"] == False]
    zhou_df['start_time'] = zhou_df.index.to_numpy()
    zhou_df['end_time'] = zhou_df["End Time"].to_numpy()
    return zhou_df


def export_ga(data_pkg_dir):
    placeholder_txt = '(((PLACEHOLDER_SENSOR))))'

    accel_dir = os.path.join(data_pkg_dir, 'Accelerometer', 'DATAFILES')
    temp_dir = os.path.join(data_pkg_dir, 'Temperature', 'DATAFILES')

    # finds files with both temperature and accelerometer edf
    accel_files = [f.replace('ACCELEROMETER', placeholder_txt) for f in os.listdir(accel_dir) if f.lower().endswith('.edf')]
    temp_files = [f.replace('TEMPERATURE', placeholder_txt) for f in os.listdir(temp_dir) if f.lower().endswith('.edf')]
    u, c = np.unique(accel_files + temp_files, return_counts=True)
    edf_files = u[c > 1]

    export_dict = {'ID': [], 'start_time': [], 'end_time': [], 'location': [], 'duration': []}

    for f in tqdm(edf_files, desc='Reading and converting EDF Files', total=len(edf_files)):
        accel_path = os.path.join(accel_dir, f.replace(placeholder_txt, 'ACCELEROMETER'))
        temp_path = os.path.join(temp_dir, f.replace(placeholder_txt, 'TEMPERATURE'))
        location = f.split('.')[0].split('_')[-1]
        subject_id = f.split('.')[0].split('_')[2]

        zhou_df = export_nw_times(accel_path, temp_path)
        start = zhou_df['start_time']
        end = zhou_df['end_time']

        if not len(start) == len(end):
            raise Exception('Start and end lengths do not match for zhou_df')

        export_dict['ID'] += [subject_id] * len(start)
        export_dict['location'] += [location] * len(start)
        export_dict['start_time'].extend(start)
        export_dict['end_time'].extend(end)

        export_dict['duration'].extend(end - start)

    df = pd.DataFrame(export_dict)
    return df


def group_nw_times(export_ga_df, group_time_sec=10, min_duration=300):
    df = export_ga_df
    # groups non-wear sections within 10 seconds of each other
    df['groups'] = ((df['start_time'] - df['end_time'].shift()) < np.timedelta64(group_time_sec, 's')) & (df['ID'] == df['ID'].shift()) & (df['location'] == df['location'].shift())
    df['nw_nums'] = (((df['groups'].shift(-1) == True) & (df['groups'] == False)) |
                     ((df['groups'].shift() == True) & (df['groups'] == False))).cumsum()

    export_dict = {'ID': [], 'start_time': [], 'end_time': [], 'location': [], 'duration': []}

    for name, group in df.groupby('nw_nums'):
        # skips nw_nums that shouldn't be grouped together
        if not group['groups'].any():
            continue
        export_dict['ID'].append(group['ID'].iloc[0])
        export_dict['start_time'].append(group['start_time'].min())
        export_dict['end_time'].append(group['end_time'].max())
        export_dict['location'].append(group['location'].iloc[0])
        export_dict['duration'].append((group['end_time'].max() - group['start_time'].min()) / np.timedelta64(1, 's'))

    export_df = pd.DataFrame(export_dict)
    export_df = export_df.loc[export_df['duration'] >= min_duration]
    return export_df


def find_overlapping_nw_times(df):
    export_dict = {'ID': [], 'start_time': [], 'end_time': [], 'location': [], 'duration': []}
    df['start_time'] = pd.to_datetime(df['start_time'])
    df['end_time'] = pd.to_datetime(df['end_time'])
    for subj_id, subject_df in df.groupby('ID'):
        subject_df = subject_df.sort_values(by=['start_time'], ignore_index=True)
        subject_df['overlaps'] = subject_df['start_time'] < subject_df['end_time'].shift()
        subject_df['intersect_id'] = (((subject_df['overlaps'].shift(-1) == True) & (subject_df['overlaps'] == False)) |
                                      ((subject_df['overlaps'].shift() == True) & (subject_df['overlaps'] == False))).cumsum()

        for intersect_id, intersect in subject_df.groupby('intersect_id'):
            if not intersect['overlaps'].any():
                continue
            intersect = intersect.drop_duplicates(subset=['location'], keep='first')
            export_dict['ID'].append(intersect['ID'].iloc[0])
            export_dict['start_time'].append(intersect['start_time'].max())
            export_dict['end_time'].append(intersect['end_time'].min())
            export_dict['location'].append(sorted(intersect['location'].to_numpy()))
            export_dict['duration'].append((intersect['end_time'].min() - intersect['start_time'].max()) / np.timedelta64(1, 's'))

    export_df = pd.DataFrame(export_dict)
    return export_df


def read_test_data(folder):
    num_files = [0, 1, 2, 3, 4, 5, 6, 7, 9]
    final_subjects = []
    final_starts = []
    final_ends = []
    mean_std = []
    is_accel_nw = []

    for i in num_files:
        subject = 'Test%d' % i
        accel_edf = os.path.join(folder, '%s_Accelerometer.EDF' % subject)
        temp_edf = os.path.join(folder, "%s_Temperature.EDF" % subject)
        logs = os.path.join(folder, '%s.csv')
        zhou_df = export_nw_times(accel_edf, temp_edf)

        final_starts.extend(zhou_df['start_time'])
        final_ends.extend(zhou_df['end_time'])
        final_subjects.extend([subject] * zhou_df.shape[0])
        mean_std.extend(np.mean(zhou_df[['x-std', 'y-std', 'z-std']], axis=1))
        is_accel_nw.extend(zhou_df['is_accel_nw'])

    df = pd.DataFrame({'ID': final_subjects, 'start_time': final_starts, 'end_time': final_ends, 'location': ['N/A'] * len(final_starts), 'mean_std': mean_std, 'is_accel_nw': is_accel_nw})
    df.to_csv('test_data.csv')
    df = group_nw_times(df, min_duration=60)
    df.to_csv('grouped_test_data.csv')


def plot_nonwear(accel_path, temp_path, non_wear_csv=None):
    zhou_df = export_nw_times(accel_path, temp_path)

    accel = pyedflib.EdfReader(accel_path)
    axis = 1
    freq = accel.getSampleFrequency(axis)
    data = accel.readSignal(axis)
    start_time = accel.getStartdatetime() + datetime.timedelta(0)
    end_time = start_time + datetime.timedelta(0, accel.getFileDuration())
    accel.close()

    if non_wear_csv is not None:
        df = pd.read_csv(non_wear_csv)
        df['start_time'] = pd.to_datetime(df['start_time'])
        df['end_time'] = pd.to_datetime(df['end_time'])
        df = df.loc[(df['start_time'] >= start_time) & (df['end_time'] < end_time) & (df['ID'] == 'Test2')]

    timestamps = np.asarray(pd.date_range(start_time, end_time, periods=zhou_df.shape[0]))

    ax1 = plt.subplot(211)
    ax1.set_title('Moving Average Standard Deviation')
    plt.plot(timestamps, np.mean([zhou_df['x-std'], zhou_df['y-std'], zhou_df['z-std']], axis=0))

    if non_wear_csv is not None:
        for i, row in df.iterrows():
            plt.axvspan(row['start_time'], row['end_time'], facecolor='b', alpha=0.5)

    ax2 = plt.subplot(212, sharex=ax1)
    ax2.set_title('Moving Average Temperature')
    plt.plot(timestamps, zhou_df['Temperature Moving Average'])

    if non_wear_csv is not None:
        for i, row in df.iterrows():
            plt.axvspan(row['start_time'], row['end_time'], facecolor='b', alpha=0.5)
    plt.show()


def find_dp(path, timestamp_str, length, axis=1):
    """
    Gets start and end time based on a timestamp and length(# data points)
    """
    accel_file = pyedflib.EdfReader(path)
    time_delta = pd.to_timedelta(
        1 / accel_file.getSampleFrequency(axis), unit='s')
    start = int((pd.to_datetime(timestamp_str) -
                 accel_file.getStartdatetime()) / time_delta)
    end = int(start + pd.to_timedelta(length, unit='s') / time_delta)
    accel_file.close()
    return start, end


def export_nonwear(accel_path, temp_path, non_wear_csv, subj_id=None):
    raw_data = {'accel_x': [], 'accel_y': [], 'accel_z': [], 'temp': []}

    # read accelerometer
    accel = pyedflib.EdfReader(accel_path)
    accel_freq = accel.samplefrequency(0)
    accel_start = accel.getStartdatetime()
    accel_end = accel_start + datetime.timedelta(0, accel.getFileDuration())
    raw_data['accel_x'].extend(accel.readSignal(0))
    raw_data['accel_y'].extend(accel.readSignal(1))
    raw_data['accel_z'].extend(accel.readSignal(2))
    assert len(set([len(raw_data['accel_x']), len(raw_data['accel_y']), len(raw_data['accel_z'])])) <= 1  # check if all lists are equal lengths
    accel.close()

    # read temperature
    temp = pyedflib.EdfReader(temp_path)
    temp_freq = temp.getNSamples()[0] / temp.getFileDuration()
    temp_start = temp.getStartdatetime()
    temp_sig = list(np.repeat(temp.readSignal(0), int(accel_freq / temp_freq)))
    pad_temp_sig = (temp_sig + [np.nan] * len(raw_data['accel_x']))[:len(raw_data['accel_x'])]
    raw_data['temp'].extend(pad_temp_sig)
    temp.close()
    assert len(raw_data['temp']) == len(raw_data['accel_x'])
    assert accel_start == temp_start
    # get subject id
    if subj_id is None:
        subj_id = int(os.path.basename(accel_path).split("_")[2])

    # reads nonwear into a dataframe
    df = pd.read_csv(non_wear_csv)
    df['start_time'] = pd.to_datetime(df['start_time'])
    df['end_time'] = pd.to_datetime(df['end_time'])
    df['plot_num'] = df.index
    df = df.loc[(df['start_time'] >= accel_start) & (df['end_time'] < accel_end) & (df['ID'] == subj_id)]

    timestamps = np.asarray(pd.date_range(accel_start, accel_end, periods=len(raw_data['accel_x'])))
    raw_data_df = pd.DataFrame(raw_data)

    for i, nw_row in tqdm(df.iterrows(), total=df.shape[0]):
        pad_time_sec = 300
        pad_nw_start = accel_start if (nw_row['start_time'] - datetime.timedelta(seconds=pad_time_sec)) < accel_start else (nw_row['start_time'] - datetime.timedelta(minutes=5))
        pad_nw_end = accel_end if (nw_row['end_time'] + datetime.timedelta(seconds=pad_time_sec)) > accel_end else (nw_row['end_time'] + datetime.timedelta(minutes=5))

        pad_start_i = int((pad_nw_start - accel_start).total_seconds() * accel_freq)
        pad_end_i = int(pad_start_i + (pad_nw_end - pad_nw_start).total_seconds() * accel_freq)

        start_i = int((nw_row['start_time'] - accel_start).total_seconds() * accel_freq)
        end_i = int(start_i + (nw_row['end_time'] - nw_row['start_time']).total_seconds() * accel_freq)

        fig, [ax1, ax2, ax3, ax4] = plt.subplots(4, 1, sharex=True)
        ax1.set_title('Accel X')
        ax1.plot(timestamps[pad_start_i:start_i], raw_data['accel_x'][pad_start_i:start_i], 'r-', label='padded signal')
        ax1.plot(timestamps[start_i:end_i], raw_data['accel_x'][start_i:end_i], 'b-', label='non wear signal')
        ax1.legend(loc='upper left')
        ax1.plot(timestamps[end_i:pad_end_i], raw_data['accel_x'][end_i:pad_end_i], 'r-', label='padded signal')
        ax2.set_title('Accel Y')
        ax2.plot(timestamps[pad_start_i:start_i], raw_data['accel_y'][pad_start_i:start_i], 'r-', label='padded signal')
        ax2.plot(timestamps[start_i:end_i], raw_data['accel_y'][start_i:end_i], 'b-', label='non wear signal')
        ax2.plot(timestamps[end_i:pad_end_i], raw_data['accel_y'][end_i:pad_end_i], 'r-', label='padded signal')
        ax3.set_title('Accel Z')
        ax3.plot(timestamps[pad_start_i:start_i], raw_data['accel_z'][pad_start_i:start_i], 'r-', label='padded signal')
        ax3.plot(timestamps[start_i:end_i], raw_data['accel_z'][start_i:end_i], 'b-', label='non wear signal')
        ax3.plot(timestamps[end_i:pad_end_i], raw_data['accel_z'][end_i:pad_end_i], 'r-', label='padded signal')
        ax4.set_title('Temp')
        ax4.plot(timestamps[pad_start_i:start_i], raw_data['temp'][pad_start_i:start_i], 'r-', label='padded signal')
        ax4.plot(timestamps[start_i:end_i], raw_data['temp'][start_i:end_i], 'b-', label='non wear signal')
        ax4.plot(timestamps[end_i:pad_end_i], raw_data['temp'][end_i:pad_end_i], 'r-', label='padded signal')

        title = 'OND06_SBH_%d_PLOT%d' % (subj_id, i)
        folder = 'non_wear_data'
        Path(folder).mkdir(parents=True, exist_ok=True)
        fig.savefig(os.path.join(folder, '%s.png' % title))
        raw_data_df.iloc[start_i:end_i].to_csv(os.path.join(folder, '%s.csv' % title), index=False)
        plt.close(fig)


accel_path = r'/Volumes/Gateway/data/OND06_SBH_1039_GNAC_ACCELEROMETER_LAnkle.edf'
temp_path = r'/Volumes/Gateway/data/OND06_SBH_1039_GNAC_TEMPERATURE_LAnkle.edf'
nw_csv = r'/Users/matthewwong/Documents/coding/nimbal/owcurate/SensorScripts/grouped_nw_GA_times.csv'
export_nonwear(accel_path, temp_path, nw_csv)

"""
# df = export_ga('/Users/matt/Documents/coding/nimbal/data/test')
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 200)
df = pd.read_csv('NW_GA.csv')
df['start_time'] = pd.to_datetime(df['start_time'])
df['end_time'] = pd.to_datetime(df['end_time'])
df = group_nw_times(df)
print(df)
# df.to_csv('grouped_nw_GA_times.csv')
"""
