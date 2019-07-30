# strava-data

1. Set up API access in Strava settings
2. Run activitites_to_csv.py to get Strava activities to local computer. You will be prompted for API access details from Step 1.
3. Run analyse_csv_power_files.py to analyse local csv power files
4. Run best_efforts_plot.py to produce a basic plot of all-time best efforts for cycling power vs duration 

# TODO
1. Implement a normalised power calc
2. Pull all streams for a popular segment e.g. Taupo and look at the power data etc
3. Make it so that other users don't need to set up their own Strava API details, i.e. run it through mine because I don't think you need resource state 3 to pull streams
