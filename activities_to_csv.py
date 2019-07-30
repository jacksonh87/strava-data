# -*- coding: utf-8 -*-
"""
Take a stravalib client and get all the activities that have power data
into csv files
"""
import os
import pandas as pd
from client_setup import inititalise_stravalib_client

def athlete_activities_to_csv(client, activity_type):
    """
    Saves activities from the athlete associated
    with the client.

    client:         a client set up using stravalib
    activity_type:  'all' to save all activities
                    'power' to save cycling activities
                        with power data
                    'running' to save run activities
    """
    athlete = client.get_athlete()
    print("Athlete: {}, \nResource state: {}".format(athlete.firstname+' '+athlete.lastname, athlete.resource_state))
    activities = client.get_activities()
    types = ['time', 'latlng', 'distance', 'altitude', 'velocity_smooth', 'heartrate', 'cadence', 'watts', 'temp', 'moving', 'grade_smooth']

    for activity in activities:
        activity_id = activity.id
        if activity_type == 'all':
            save_activity = True
            save_dir = './all_activities/'
        elif activity_type == 'power':
            save_activity = (activity.device_watts is True)
            save_dir = './power_data/'
        elif activity_type == 'running':
            save_activity = (activity.type == 'Run')
            save_dir = './running_data/'
        csv_save_path = save_dir+str(activity_id)+'.csv'
        if os.path.isfile(csv_save_path):
            continue # i.e. skip if file exists already
        if save_activity:
            activity_stream = client.get_activity_streams(activity_id, types=types)
            activity_data_frame = pd.DataFrame()
            if hasattr(activity_stream, 'items'):
                for key, value in activity_stream.items():
                    activity_data_frame[key] = value.data
                activity_data_frame.to_csv(csv_save_path)

if __name__ == '__main__':
    client = inititalise_stravalib_client()
    athlete_activities_to_csv(client, 'all')

