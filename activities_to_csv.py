# -*- coding: utf-8 -*-
"""
Take a stravalib client and get all the activities that have power data
into csv files
"""
import os
import pandas as pd
from client_setup import inititalise_stravalib_client

def client_power_data_to_csv(client):
    
    athlete = client.get_athlete()
    print("Athlete: {}, \nResource state: {}".format(athlete.firstname+' '+athlete.lastname, athlete.resource_state))
    activities = client.get_activities()
    types = ['time', 'latlng', 'distance', 'altitude', 'velocity_smooth', 'heartrate', 'cadence', 'watts', 'temp', 'moving', 'grade_smooth']

    for activity in activities:
        activity_id = activity.id
        csv_save_path = './power_data/'+str(activity_id)+'.csv'
        if os.path.isfile(csv_save_path):
            print(activity_id)
            continue
        has_watts = (activity.device_watts is True)
        if has_watts:
            activity_stream = client.get_activity_streams(activity_id, types=types)
            activity_data_frame = pd.DataFrame()
            for key, value in activity_stream.items():
                activity_data_frame[key] = value.data
            activity_data_frame.to_csv(csv_save_path)
        
if __name__ == '__main__':
    client = inititalise_stravalib_client()
    client_power_data_to_csv(client)

