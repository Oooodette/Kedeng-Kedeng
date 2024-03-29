import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import pprint
import numpy as np
import math
import random
from matplotlib.pyplot import cm

def visualize_stations_connections(stations_df, connections_df,ax):
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
        ax.scatter(x=x, y=y, s=25, edgecolors='black', c='white', zorder = 10)

        #check and retrieve connections of station
        if station in connections_dict:
            connected_stations = connections_dict[station]

            #plot the connections of the station
            for connected_station in connected_stations:
                x_conection, y_connection = stations_dict.get(connected_station)
                x_list = [x, x_conection]
                y_list = [y, y_connection]
                plt.plot(x_list, y_list, c='black', linewidth = 0.5, linestyle='dotted')

    return ax

def plot_netherlands(datafile,ax):
    """
    Create plot of country to plot train lines on.
    Args:
    - json file with geopandas data
    Returns:
    - country_plot(axes object): object containing country plot
    """
    # load data from file
    mapdf = gpd.read_file(datafile, index = False)

    # remove irrelevant columns and rows containing lakes)
    dropnames = ['GID_1', 'GID_0', 'ISO_1', 'COUNTRY', 'VARNAME_1', 'NL_NAME_1', 'TYPE_1', 'ENGTYPE_1', 'CC_1',
        'HASC_1']
    droplakes = [5,12]
    mapdf = mapdf.drop(dropnames, axis=1)
    mapdf = mapdf.drop(droplakes, axis=0)

    # plot country
    country_plot = mapdf.plot(ax=ax, facecolor = 'lightgrey', edgecolor = 'black') 
    
    return country_plot

def pick_train_color(trajectories): 
    """
    Give every trajectory its own color.

    Args: 
    - trajectories(list): list of trajectories made by a network. 
    """

    # Use the first 20 colors
    # create distinct colors for every trajectory
    color = cm.rainbow(np.linspace(0, 1, len(trajectories)))
    counter = 0
    for train in trajectories:
        train.color = color[counter]
        counter += 1

def get_coordinates(connection, stations):
    """
    Retrieve coordinates of stations of a certain connection.
    Args: 
    - connection(instance of connection class): the connection of which you need the stations coordinates
    - stations(list): list of all stations available for this network
    Returns: 
    - x_cor(list): list of x coordinates where [0] is coordinate of station 1 and [1] is coordinate of station 2
    - y_cor(list): list of y coordinates where [0] is coordinate of station 1 and [1] is coordinate of station 2
    """

    #TODO: make this better!!
    station1 = [station for station in  stations if station.name == connection.station1][0]
    station2 = [station for station in stations if station.name == connection.station2][0]
    x_cor = [station1.x_cor, station2.x_cor]
    y_cor = [station1.y_cor, station2.y_cor] 

    return x_cor, y_cor
def connection_list_maker(used_connections):
    """
    Select all connections that were used for a network.
    Args:
    - used_connection(dict): dictionary where keys are connections and values are booleans that signify whether the connection
      was used in this network.
    Returns:
    - connection_set(set): set containing all used connections for this network.
    """
    connection_list = [connection for connection, value in used_connections.items() if value != 0]

    return connection_list

def plot_connections(used_connections, trajectories, stations, ax):
    """"
    Plot all connections that were used in a network. Connections that are used in multiple trajectories are plotted next to each other.
    Every trajectory has its own color.
    Args: 
    - used_connections(dict): dictionary where keys are connections and values are booleans that signify whether the connection
      was used in this network
    - trajectories(list): list of instaces of trajectory class, containing all trajectories that were created by a network
    - stations(list): list of all stations in a network. 
    """
    # give every trajectory a unique color
    pick_train_color(trajectories)
    
    # get a set of all connections that were used in the network
    connection_set = connection_list_maker(used_connections) 
    
    # loop over all used connections
    for connection in connection_set: 
        x_cor, y_cor = get_coordinates(connection, stations) 
        train_counter = 0

        # loop over all trajectories and check if a trajectory uses this connection.
        trains = []
        for train in trajectories:
            if connection in train.route:
                train_counter += 1
                trains.append(train)
                offset_counter = 0 
        # loop through trains that run over this connection. Every train gets assigned it's color and linestyle (so position of dashes 
        # the line) is adapted to number of trains. 
        for train in trains:
            ax.plot(x_cor,y_cor, c=train.color, linestyle=(offset_counter*2, (2, train_counter*2- 2)), linewidth = 3)
            offset_counter += 1
        train_counter += 1
    return ax

def plot_all(stations_df, connections_df, datafile, used_connections, trajectories, stations, vis_output):
    fig, ax = plt.subplots()
    
    plot_netherlands(datafile,ax)
    ax = plot_connections(used_connections, trajectories, stations, ax)
    ax = visualize_stations_connections(stations_df, connections_df, ax)
    plt.savefig(vis_output, dpi=500)
    plt.show()
