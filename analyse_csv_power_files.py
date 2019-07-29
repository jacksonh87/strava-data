# -*- coding: utf-8 -*-
"""
Takes a folder of csv power files and returns the 
all-time top power for ten seconds, one minure, 
five minutes, ten minutes, twenty minutes, forty 
minutes and sixty minutes
"""
import os
import pandas as pd
import webbrowser

def analyse_csv_power_files():
    source_files_directory = './power_data/'
    
    results_dict = {}
    for file in os.listdir(source_files_directory):
        csv_file_path = source_files_directory+file
        activity_id = file.strip('.csv')
        df = pd.read_csv(csv_file_path)
        if 'watts' in df.columns:
            df['ten_sec_power'] = df.watts.rolling(10).mean().fillna(0.00)
            df['one_min_power'] = df.watts.rolling(60).mean().fillna(0.00)
            df['five_min_power'] = df.watts.rolling(5*60).mean().fillna(0.00)
            df['ten_min_power'] = df.watts.rolling(10*60).mean().fillna(0.00)
            df['twenty_min_power'] = df.watts.rolling(20*60).mean().fillna(0.00)
            df['forty_min_power'] = df.watts.rolling(40*60).mean().fillna(0.00)
            df['sixty_min_power'] = df.watts.rolling(60*60).mean().fillna(0.00)
            results_dict[activity_id] = [max(df.ten_sec_power), max(df.one_min_power), max(df.five_min_power), max(df.ten_min_power), max(df.twenty_min_power), max(df.forty_min_power), max(df.sixty_min_power)]
    
    best_efforts_df = pd.DataFrame(results_dict).T
    best_efforts_df.columns = ['ten_sec_power', 
                               'one_min_power', 
                               'five_min_power', 
                               'ten_min_power',
                               'twenty_min_power',
                               'forty_min_power',
                               'sixty_min_power']
    
    best_efforts_df.to_csv('best_power_efforts.csv')
    
    best_ten_sec = best_efforts_df[best_efforts_df.ten_sec_power==best_efforts_df.ten_sec_power.max()]
    best_one_min = best_efforts_df[best_efforts_df.one_min_power==best_efforts_df.one_min_power.max()]
    best_five_min = best_efforts_df[best_efforts_df.five_min_power==best_efforts_df.five_min_power.max()]
    best_ten_min = best_efforts_df[best_efforts_df.ten_min_power==best_efforts_df.ten_min_power.max()]
    best_twenty_min = best_efforts_df[best_efforts_df.twenty_min_power==best_efforts_df.twenty_min_power.max()]
    best_forty_min = best_efforts_df[best_efforts_df.forty_min_power==best_efforts_df.forty_min_power.max()]
    best_sixty_min = best_efforts_df[best_efforts_df.sixty_min_power==best_efforts_df.sixty_min_power.max()]
    
    print('Best 10 second power: '+ str(round(best_efforts_df.ten_sec_power.max()))+ ' in activity: '+str(best_ten_sec.index[0]))
    print('Best 1 minute power: '+ str(round(best_efforts_df.one_min_power.max()))+ ' in activity: '+str(best_one_min.index[0]))
    print('Best 5 minute power: '+ str(round(best_efforts_df.five_min_power.max()))+ ' in activity: '+str(best_five_min.index[0]))
    print('Best 10 minute power: '+ str(round(best_efforts_df.ten_min_power.max()))+ ' in activity: '+str(best_ten_min.index[0]))
    print('Best 20 minute power: '+ str(round(best_efforts_df.twenty_min_power.max()))+ ' in activity: '+str(best_twenty_min.index[0]))
    print('Best 40 minute power: '+ str(round(best_efforts_df.forty_min_power.max()))+ ' in activity: '+str(best_forty_min.index[0]))
    print('Best 60 minute power: '+ str(round(best_efforts_df.sixty_min_power.max()))+ ' in activity: '+str(best_sixty_min.index[0]))
    
    #webbrowser.open_new_tab('https://www.strava.com/activities/'+str(best_ten_sec.index[0]))
    #webbrowser.open_new_tab('https://www.strava.com/activities/'+str(best_one_min.index[0]))
    #webbrowser.open_new_tab('https://www.strava.com/activities/'+str(best_five_min.index[0]))
    #webbrowser.open_new_tab('https://www.strava.com/activities/'+str(best_ten_min.index[0]))
    #webbrowser.open_new_tab('https://www.strava.com/activities/'+str(best_twenty_min.index[0]))
    #webbrowser.open_new_tab('https://www.strava.com/activities/'+str(best_forty_min.index[0]))
    #webbrowser.open_new_tab('https://www.strava.com/activities/'+str(best_sixty_min.index[0]))
    
if __name__ == '__main__':
    analyse_csv_power_files()