# -*- coding: utf-8 -*-
"""
Set up a client using stravalib
"""
import json
import os
import pandas as pd
import webbrowser
import time
from stravalib.client import Client

def inititalise_stravalib_client():
    client_details_filename = 'client_details.json'
    access_token_filename = 'access_token.json'
    
    client = Client()
    
    access_token_does_exist = os.path.isfile(access_token_filename)
    access_token_doesnt_exist = not(access_token_does_exist)
    access_token_expired = True
    
    if access_token_does_exist:
         with open(access_token_filename, 'r') as f:
            token_response = json.load(f)
            token_response = json.loads(token_response)      
            token_expiry_time = token_response['expires_at']
            current_time = time.time()
            access_token_expired = current_time > token_expiry_time
        
    if access_token_doesnt_exist or access_token_expired:
        # Check if I have client details in a json:
        if os.path.isfile(client_details_filename):
            with open(client_details_filename, 'r') as f:
                client_details = json.load(f)
                client_details = json.loads(client_details)
        else:
            client_id = str(input('Enter your client ID: '))
            client_secret = str(input('Enter your client secret: '))
            client_details = {'client_id': client_id,
                              'client_secret': client_secret}
            # Save client details to file
            client_details_string = json.dumps(client_details)
            with open(client_details_filename, 'w+') as f:
                json.dump(client_details_string, f)
        
        # Read client details from file:
        with open(client_details_filename, 'r') as f:
            client_details = json.load(f)
            client_details = json.loads(client_details)
              
        client_id = client_details['client_id']
        client_secret = client_details['client_secret']
        scope = ['read', 'read_all', 'profile:read_all', 'profile:write', 'activity:read', 'activity:read_all', 'activity:write']
        authorize_url = client.authorization_url(client_id=client_id, redirect_uri='http://localhost:5000/authorized', scope=scope)
        
        # Open the authorization url
        print('Opening: ' + authorize_url)
        webbrowser.open(authorize_url)
        
        # Get code
        entered_code = str(input('Please enter code: '))
        
        # Exchange code for token:
        token_response = client.exchange_code_for_token(client_id=client_id, client_secret=client_secret, code=entered_code)
        # Save it to file so we can use it until it expires.
        access_token_string = json.dumps(token_response)
        with open(access_token_filename, 'w+') as f:
            json.dump(access_token_string, f)
    
    # Now we have a token_response dict either from file or from the
    # Strava API
    access_token = token_response['access_token']
    refresh_token = token_response['refresh_token']
       
    # Provide the access token and refresh token to the client:
    client.access_token = access_token
    client.refresh_token = refresh_token

    return client


def dump_activities_to_df(client):   
    df_overview = pd.DataFrame()
    activities = {}
    resolution = 'high'
    year = 2018
    types = ['time', 'altitude', 'heartrate', 'temp', 'distance', 'watts']

    for activity in client.get_activities(after='{}-12-01T00:00:00Z'.format(str(year)),
                                    before='{}-01-01T00:00:00Z'.format(str(year + 1))):
        streams = client.get_activity_streams(activity.id,
                                            types=types,
                                            series_type='time',
                                            resolution=resolution)
        for key, value in streams.items():
            streams[key] = value.data
    
        df_overview = df_overview.append(pd.DataFrame([{
            'Name': activity.name,
            'Date': activity.start_date,
            'Moving Time [min]': int(activity.moving_time.seconds / 60),
            'Distance [km]': round(activity.distance.num / 1000, 1),
            'Measurements': list(streams.keys())
        }], index=[activity.id]))
    
        activities[activity.id] = pd.DataFrame(streams)
    
    writer = pd.ExcelWriter('strava_export_{}.xlsx'.format(str(year)), engine='openpyxl')
    df_overview.to_excel(writer, "Overview")
    
    for activity_id, df in activities.items():
        df.to_excel(writer, ' '.join([str(df_overview.loc[activity_id]['Date'].date()),
        df_overview.loc[activity_id]['Name']])[:30])
    
    writer.save()



if __name__ == '__main__':
    client = inititalise_stravalib_client()
    athlete = client.get_athlete()
    print("Athlete: {}, \nResource state: {}".format(athlete.firstname+' '+athlete.lastname, athlete.resource_state))
    activities = client.get_activities()
    power_list = []
    streams_list = []
    types = ['time', 'latlng', 'distance', 'altitude', 'velocity_smooth', 'heartrate', 'cadence', 'watts', 'temp', 'moving', 'grade_smooth']
#    for activity in activities:
#        has_watts = (activity.device_watts is True)
#        if has_watts:
#            power_list.append(activity)
#            streams_list.append(client.get_activity_streams(activity.id, types=types))

    test_id = 923720941
    test_stream = client.get_activity_streams(test_id, types=types)
    
    a = pd.DataFrame()
    for key, value in test_stream.items():
        a[key] = value.data
        a.to_csv('./power_data/'+str(test_id)+'.csv')