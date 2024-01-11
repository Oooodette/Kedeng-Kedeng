import pandas as pd
import matplotlib.pyplot as plt

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


    #NECESSARY??
    # connections_dict = {}
    # for index, row in connections_df.iterrows():
    #     connections_dict.setdefault(row['station1'], []).append(row['station2'])
    #------------------------------


    #create lists of x and y coordinates of the trajectory
    x_list = []
    y_list = []

    for station in train:
        x_list.append(stations_dict[station][0])
        y_list.append(stations_dict[station][1])

    #plot the trajectory
    plt.plot(x_list, y_list, c=c, linestyle='--')


def visualize_network(stations_df, connections_df, trajectories_dict, traject_colors):
    """visualize all trajectories"""

    #convert the dataframe to dictionary
    trajectories_dict = {}
    for index, row in trajectories_df.iterrows():
        value = row['stations'].strip('[]').split(', ')
        trajectories_dict[row['train']] = value

    #plot all stations and their connections
    image = visualize_stations_connections(stations_df, connections_df)

    #loop over all trains (trajectories)
    color_i = 0
    for train in trajectories_dict:
        trajectory = trajectories_dict[train]
        image = visualise_trajectory(stations_df, connections_df, trajectory, c=traject_colors[color_i])
        color_i += 1


traject_colors = ['#ff8c00', '#228b22', '#b22222', '#9370db', '#bc8f8f',
                '#db7093', '#808080', '#6b8e23', '#00ffff', '#ff0000',
                '#00ff00', '#ffff00', '#40e0d0', '#ff00ff', '#c0c0c0',
                '#800000', '#00ff00', '#ffffff', '#ffd700', '#2f4f4f']


stations_df = pd.read_csv('StationsNationaal.csv')
connections_df = pd.read_csv('ConnectiesNationaal.csv')
trajectories_df = pd.read_csv('example_output.csv', skipfooter=1, engine='python')


visualize_network(stations_df, connections_df, trajectories_df, traject_colors)

plt.show()































#
