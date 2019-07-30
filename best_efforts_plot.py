# -*- coding: utf-8 -*-
"""
Plots best power efforts
"""
import json
import matplotlib.pyplot as plt

def plot_best_efforts_power_curve(best_efforts_json_file):
    """
    Args:
        best_efforts_json_file: Name of a json file 
            holding best efforts data (produce using
            analyse_csv_power_files.py)
    """
    
    with open(best_efforts_json_file, 'r') as f:
        best_efforts_dict = json.loads(json.load(f))
    
    x = list([float(i) for i in best_efforts_dict.keys()])
    y = list(best_efforts_dict.values())
    ax = plt.gca()
    ax.plot(x, y)
    #ax.scatter(x, y)
    ax.set_xscale('log')
    plt.title('Power vs duration, all-time best efforts')
    plt.xlabel('Duration (log(seconds))')
    plt.ylabel('Power (W)')
    plt.show()
   

if __name__ == '__main__':
    plot_best_efforts_power_curve('best_efforts.json')