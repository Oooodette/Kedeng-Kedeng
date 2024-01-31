from code.classes import Station, Connection, Trajectory, Network
from code.algorithms.random_algo import Random_algo
from code.algorithms.greedy_algo import Greedy_algo
from code.visualize import new_visualize as vis
import pandas as pd
import matplotlib.pyplot as plt


#defining parameters for different datasets
max_trajectories_holland = 7
max_trajectory_time_holland = 120
max_trajectories_nl = 20
max_trajectory_time_nl = 180
score = 0

#initializing scores list to plot 
scores = []
nrs_trajectories = []
fractions = []


#reading in data
connections_df = pd.read_csv('data\ConnectiesNationaal.csv')
stations_df = pd.read_csv('data\StationsNationaal.csv')

#create empty network
network = Network(connections_df, stations_df, max_trajectories_nl, max_trajectory_time_nl)
final_network = None

#create 10000 networks
for i in range(10000):
    random_network = Random_algo(network)
    test_network = random_network.create_network()

    nrs_trajectories.append(len(test_network.trajectories))
    used_connections = [connection for connection, value in test_network.used.items() if value != 0]
    fraction = (len(used_connections)) / len(test_network.connections)
    
    new_score = test_network.get_score()
    scores.append(new_score)
    fractions.append(fraction)

    if new_score > score:
        final_network = test_network
        score = new_score

#determining the fraction of driven connections
used_connections = [connection for connection, value in final_network.used.items() if value != 0]
fraction = (len(used_connections)) / len(final_network.connections)

print(f'Best network has score {final_network.get_score()}')
print(f'Best network has {len(final_network.trajectories)} trajectories')
print(f'Best network has fraction {fraction}')

print(f'Average score is ')
plt.hist(scores, bins=1000)
plt.xlim(0, 10000)
plt.show()

