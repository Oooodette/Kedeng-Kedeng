import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import pprint
import numpy as np
import math
import random


def visualize_stations_connections(stations_df, connections_df):
    """visualize all stations and their connections"""

    #create dictionaries from the dataframes
    stations_dict = {}

    for index, row in stations_df.iterrows():
        stations_dict[row['station']] = row['x'], row['y']

    connections_dict = {}
    for index, row in connections_df.iterrows():
        connections_dict.setdefault(row['station1'], []).append(row['station2'])

    #plot the stations from coordinates
    for station in stations_dict:
        x, y = stations_dict.get(station)
        plt.scatter(x=x, y=y, s=30, edgecolors='black', c='white')

        # #check and retrieve connections of station
        # if station in connections_dict:
        #     connected_stations = connections_dict[station]

        #     #plot the connections of the station
        #     for connected_station in connected_stations:
        #         x_conection, y_connection = stations_dict.get(connected_station)
        #         x_list = [x, x_conection]
        #         y_list = [y, y_connection]
        #         plt.plot(x_list, y_list, c='b', linestyle='--')
def plot_netherlands(datafile):
    """
    Create plot of country to plot train lines on.
    Args:
    - json file with geopandas data
    Returns:
    - country_plot(axes object): object containing country plot
    """
    # load data from file
    mapdf = gpd.read_file(datafile)

    # remove irrelevant columns
    dropnames = ['GID_1', 'GID_0', 'ISO_1', 'COUNTRY', 'VARNAME_1', 'NL_NAME_1', 'TYPE_1', 'ENGTYPE_1', 'CC_1',
        'HASC_1',]
    mapdf = mapdf.drop(dropnames, axis = 1)

    # plot country
    country_plot = mapdf.plot()
    
    return country_plot

def pick_train_color(trajectories): 
    for train in trajectories:
        #TODO: make sure two trains can't have the same color
        color = f'#{"%06x" % random.randint(0, 0xFFFFFF)}'
        train.color = color 

def get_coordinates(connection, stations):

    #TODO: make this better!!
    station1 = [station for station in  stations if station.name == connection.station1][0]
    station2 = [station for station in stations if station.name == connection.station2][0]
    x_cor = [station1.x_cor, station2.x_cor]
    y_cor = [station1.y_cor, station2.y_cor] 


    return x_cor, y_cor
def connection_set_maker(used_connections):

    connection_set =  set([connection for connection, is_used in used_connections.items() if is_used])

    return connection_set

def plot_connections(used_connections, trajectories, stations):
    
    pick_train_color(trajectories)
    # give every train their color
    connection_set = connection_set_maker(used_connections) 
  
    for connection in connection_set: 
        x_cor, y_cor = get_coordinates(connection, stations) 
        train_counter = 0
        for train in trajectories:
            if connection in train.route:

                # create shift if there is more than 1 train on this connection, so all lines are visible
                shift = train_counter * 0.001
                plt.plot([x + shift for x in x_cor], [y + shift for y in y_cor], c=train.color, linestyle='-', linewidth = 2)
                train_counter += 1

def plot_all(stations_df, connections_df, datafile, used_connections, trajectories, stations):
    plot_netherlands(datafile)
    plot_connections(used_connections, trajectories, stations)
    visualize_stations_connections(stations_df, connections_df)
    
    plt.show()
