from SensorScripts import *
import os
import numpy as np
import pandas as pd
from tqdm import tqdm


def export_nw_times(accel_path, temp_path):
    s = SensorScripts()
    s.read_accelerometer(accel_path)
    s.read_temperature(temp_path)
    zhou_df = s.zhou_nonwear(use_updated_alg=True)
    zhou_nw_starts = zhou_df.loc[zhou_df["Device Worn?"] == False].index.to_numpy()
    zhou_nw_ends = zhou_df["End Time"].loc[zhou_df["Device Worn?"] == False].to_numpy()
    zhou_accel_nw = zhou_df['is_accel_nw'].loc[zhou_df["Device Worn?"] == False].to_numpy()
    del zhou_df

    return zhou_nw_starts, zhou_nw_ends, zhou_accel_nw


def export_ga(data_pkg_dir):
    placeholder_txt = '(((PLACEHOLDER_SENSOR))))'

    accel_dir = os.path.join(data_pkg_dir, 'Accelerometer', 'DATAFILES')
    temp_dir = os.path.join(data_pkg_dir, 'Temperature', 'DATAFILES')

    # finds files with both temperature and accelerometer edf
    accel_files = [f.replace('ACCELEROMETER', placeholder_txt) for f in os.listdir(accel_dir) if f.lower().endswith('.edf')]
    temp_files = [f.replace('TEMPERATURE', placeholder_txt) for f in os.listdir(temp_dir) if f.lower().endswith('.edf')]
    u, c = np.unique(accel_files + temp_files, return_counts=True)
    edf_files = u[c > 1]

    export_dict = {'ID': [], 'start_time': [], 'end_time': [], 'location': [], 'duration': [], 'is_accel_nw': []}

    for f in tqdm(edf_files, desc='Reading and converting EDF Files', total=len(edf_files)):
        accel_path = os.path.join(accel_dir, f.replace(placeholder_txt, 'ACCELEROMETER'))
        temp_path = os.path.join(temp_dir, f.replace(placeholder_txt, 'TEMPERATURE'))
        location = f.split('.')[0].split('_')[-1]
        subject_id = f.split('.')[0].split('_')[2]

        start, end, is_accel_nw = export_nw_times(accel_path, temp_path)

        if not len(start) == len(end):
            raise Exception('Start and end lengths do not match for zhou_df')

        export_dict['ID'] += [subject_id] * len(start)
        export_dict['location'] += [location] * len(start)
        export_dict['start_time'].extend(start)
        export_dict['end_time'].extend(end)
        export_dict['duration'].extend(end - start)
        export_dict['is_accel_nw'].extend(is_accel_nw)

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


#df = export_ga('/Users/matt/Documents/coding/nimbal/data/test')
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 200)
df = pd.read_csv('NW_GA.csv')
df['start_time'] = pd.to_datetime(df['start_time'])
df['end_time'] = pd.to_datetime(df['end_time'])
df = group_nw_times(df)
print(df)
# df.to_csv('grouped_nw_GA_times.csv')
