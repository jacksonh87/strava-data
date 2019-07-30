# -*- coding: utf-8 -*-
"""
Takes a folder of csv power files and returns the
all-time top power for the specified durations
"""
import json
import os
import pandas as pd

def analyse_csv_power_files():
    """
    Runs throughh every power csv file and calculates
    the best average power for every duration specified.
    Saved a csv containing a row specifying these, keyed
    by activity ID.
    Finds the all-time best efforts for every duration
    specified and returns these in a dictionary.
    """
    source_files_directory = './power_data/'

    results_dict = {}
    power_durations = [3, 4, 5, 10, 15, 30, 45, 60, 90,
                       120, 180, 240, 5*60, 6*60, 7*60,
                       8*60, 9*60, 10*60, 15*60, 20*60,
                       30*60, 40*60, 60*60, 90*60,
                       120*60] # these are in seconds

    for file in os.listdir(source_files_directory):
        csv_file_path = source_files_directory+file
        activity_id = file.strip('.csv')
        df = pd.read_csv(csv_file_path)
        if 'watts' in df.columns:
            results = []
            for duration in power_durations:
                df[duration] = df.watts.rolling(duration).mean().fillna(0.00)
                results.append(max(df[duration]))
            results_dict[activity_id] = results

    best_efforts_df = pd.DataFrame(results_dict).T
    best_efforts_df.columns = power_durations
    best_efforts_df.to_csv('best_power_efforts.csv')

    best_efforts_dict = {}
    best_efforts_ids_dict = {}

    for duration in power_durations:
        best_effort = best_efforts_df[best_efforts_df[duration] == best_efforts_df[duration].max()]
        best_efforts_dict[duration] = best_effort[duration][0]
        best_efforts_ids_dict[duration] = best_effort.index[0]

    best_efforts_json_string = json.dumps(best_efforts_dict)
    with open('best_efforts.json', 'w+') as f:
        json.dump(best_efforts_json_string, f)

    return best_efforts_dict, best_efforts_ids_dict, best_efforts_df

if __name__ == '__main__':
    best_efforts_dict, best_efforts_ids_dict, best_efforts_df = analyse_csv_power_files()
