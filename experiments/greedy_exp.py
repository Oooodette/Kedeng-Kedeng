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
scores = []

connections_df = pd.read_csv('data\ConnectiesNationaal.csv')
stations_df = pd.read_csv('data\StationsNationaal.csv')

network = Network(connections_df, stations_df, max_trajectories_nl, max_trajectory_time_nl)

for i in range(10000):
    
