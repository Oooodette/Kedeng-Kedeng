import pandas as pd
import matplotlib.pyplot as plt
import random as random

"""
Visualizing all stations in NL and their connections
Visualizing the trajectories from the lists of stations
"""

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
        plt.scatter(x=x, y=y, s=7, c='r')

        #check and retrieve connections of station
        if station in connections_dict:
            connected_stations = connections_dict[station]

            #plot the connections of the station
            for connected_station in connected_stations:
                x_conection, y_connection = stations_dict.get(connected_station)
                x_list = [x, x_conection]
                y_list = [y, y_connection]
                plt.plot(x_list, y_list, c='b', linestyle='-')


def visualise_trajectory(stations_df, connections_df, train, c):
    """visualize a single trajectory from a list of stations"""

    #create dictionaries from the dataframes
    stations_dict = {}
    for index, row in stations_df.iterrows():
        stations_dict[row['station']] = row['x'], row['y']

    x_list = []
    y_list = []

    # print(stations_dict)

    for station in train:
        x_list.append(stations_dict[station][0])
        y_list.append(stations_dict[station][1])

    #plot the trajectory
    plt.plot(x_list, y_list, c=c, linestyle='--')


def visualize_network(stations_df, connections_df, trajectories_file):
    """visualize all trajectories"""

    #convert the dataframe to dictionary

    trajectories_df = pd.read_csv(trajectories_file, skipfooter=1, engine='python')

    trajectories_dict = {}
    for index, row in trajectories_df.iterrows():
        value = (row['stations']).strip("[]").replace("'", "").split(", ")

        trajectories_dict[row['train']] = value

    #plot all stations and their connections
    image = visualize_stations_connections(stations_df, connections_df)

    #loop over all trains (trajectories) and generate random color
    for train in trajectories_dict:

        color = f'#{"%06x" % random.randint(0, 0xFFFFFF)}'

        trajectory = trajectories_dict[train]
        image = visualise_trajectory(stations_df, connections_df, trajectory, c=color)
































#
