from SensorScripts import *
import os
import numpy as np
import pandas as pd
from tqdm import tqdm

def export_nw_times(accel_path, temp_path):
    s = SensorScripts()
    s.read_accelerometer(accel_path)
    s.read_temperature(temp_path)
    zhou_df = s.zhou_nonwear()
    zhou_nw_starts = zhou_df.loc[zhou_df["Device Worn?"] == False].index.to_numpy()
    zhou_nw_ends = zhou_df["End Time"].loc[zhou_df["Device Worn?"] == False].to_numpy()
    del zhou_df

    return zhou_nw_starts, zhou_nw_ends

def export_ga(data_pkg_dir):
    placeholder_txt = '(((PLACEHOLDER_SENSOR))))'

    accel_dir = os.path.join(data_pkg_dir, 'Accelerometer', 'DATAFILES')
    temp_dir = os.path.join (data_pkg_dir, 'Temperature', 'DATAFILES')

    # finds files with both temperature and accelerometer edf
    accel_files = [ f.replace('Accelerometer', placeholder_txt) for f in os.listdir(accel_dir) if f.lower().endswith('.edf')]
    temp_files = [ f.replace('Temperature', placeholder_txt) for f in os.listdir(temp_dir) if f.lower().endswith('.edf')]
    u, c = np.unique(accel_files + temp_files, return_counts=True)
    edf_files = u[c > 1]

    export_dict = {'ID': [], 'start_time': [], 'end_time': [], 'location': [], 'duration': []}

    for f in tqdm(edf_files, desc='Reading and converting EDF Files', total=len(edf_files)):
        accel_path = os.path.join(accel_dir, f.replace(placeholder_txt, 'Accelerometer'))
        temp_path = os.path.join(temp_dir, f.replace(placeholder_txt, 'Temperature'))
        location = f.split('.')[0].split('_')[-1]
        subject_id = f.split('.')[0].split('_')[2]

        start, end = export_nw_times(accel_path, temp_path)

        if not len(start) == len(end):
            raise Exception('Start and end lengths do not match for zhou_df')

        export_dict['ID'] += [subject_id] * len(start)
        export_dict['location'] += [location] * len(start)
        export_dict['start_time'].extend(start)
        export_dict['end_time'].extend(end)
        export_dict['duration'].extend(end-start)


    df = pd.DataFrame(export_dict)
    return df

def group_nw_times(export_ga_df, group_time_sec=10, min_duration=300):
    df = export_ga_df
    # groups non-wear sections within 10 seconds of each other
    groups = ( (df['start_time']-df['end_time'].shift()) < np.timedelta64(group_time_sec, 's') )  & (df['ID'] == df['ID'].shift()) & (df['location'] == df['location'].shift()) 
    df['bout_nums'] = ( groups != groups.shift() ).cumsum()
    u, i, c = np.unique(df['bout_nums'], return_counts=True, return_index=True)
    df['bout_nums'][i[c == 1]] += 1
    df['bout_nums'] = (df['bout_nums'] != df['bout_nums'].shift() ).cumsum()


    export_dict = {'ID': [], 'start_time': [], 'end_time': [], 'location': [], 'duration': []}

    for name, group in df.groupby('bout_nums'):
        export_dict['ID'].append(group['ID'].iloc[0])
        export_dict['start_time'].append(group['start_time'].min())
        export_dict['end_time'].append(group['end_time'].max())
        export_dict['location'].append(group['location'].iloc[0])
        export_dict['duration'].append( (group['end_time'].max() - group['start_time'].min()) / np.timedelta64(1, 's') )

    export_df = pd.DataFrame(export_dict)
    export_df = export_df.loc[export_df['duration'] >= min_duration]
    return export_df


df = export_ga('/Users/matt/Documents/coding/nimbal/data/test')
df.to_csv('export_ga.csv')
df = group_nw_times(df)
df.to_csv('grouped_nw_GA_times.csv')
