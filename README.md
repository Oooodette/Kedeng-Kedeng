# Kedeng-Kedeng, RailNL
Subject: Algoritmen en Heuristieken
People: Odette, Mette, Bas

### DESCRIPTION
Project to optimize the (simplified) railnetwork in the Netherlands.

The Dutch railnet of NL used in this project consists of a number of stations, and a (different) number of connections between stations.
A connection has a certain time it takes to travel by train from station 1 to station 2.
A trajectory is a sequence of stations, with a certain time that is calculated by adding all times of the connections between all stations in the trajectory.
A network is a combination of multiple trajectories that fulfill certain requirements. A network has a certain total time and score.

The score is calculated by the formula K = p * 10000 - (N*100 + min)
where:
p = fraction of connections that have been driven
T = number of trajectories in the network
min = total time of the network in minutes

The goal is the maximize the score of the network

Classes in this project:
- Station (attr: x_cor, y_cor, name)
- Connection (attr: station1, station2, time)
- Trajectory (attr: name, stations, time)
- Network (attr: used, quality_network, stations, connections)

The class Network reads in the data of the stations and connections.

Separately, algorithms are defined in the folder 'algorithms'.
These are all different algorithms and each have their own specifications

Algorithm specs;
- random_alg: random algorithm that creates trajectories in a random way, until all connections have been used.

- #algorithm2

#TODO: SPECIFY WHETHER CLASS NETWORK CALLS ALGORITHMS OR OTHER WAY AROUND

### INSTALLATIONS/LIBRARY IMPORTS
1) Python 3

Python libraries
1) Pandas as pd
2) Matplotlib.pyplot as plt
3) Random

### USAGE/EXAMPLES
