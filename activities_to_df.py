# -*- coding: utf-8 -*-
"""

"""
import pandas as pd

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
