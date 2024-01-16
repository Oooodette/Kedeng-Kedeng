# Kedeng-Kedeng, RailNL
##### Subject: Algoritmen en Heuristieken
##### People: Odette, Mette, Bas

### Description
Project to optimize the (simplified) railnetwork in the Netherlands.

#### General description and goal
The Dutch railnet of NL used in this project consists of a number of stations, and a (different) number of connections between stations.
A connection has a certain time it takes to travel by train from station 1 to station 2.
A trajectory is a sequence of stations, with a certain time that is calculated by adding all times of the connections between all stations in the trajectory.
A network is a combination of multiple trajectories that fulfill certain requirements. A network has a certain total time and score.

The score is calculated by the formula K = p * 10000 - (N*100 + min where:
- p = fraction of connections that have been driven
- T = number of trajectories in the network
- min = total time of the network in minutes

The goal is the maximize the score of the network.

#### Subcases
There are two subcases with different constraints;
1) North and South Holland
 - maximal trajectory time is 120 minutes
 - maximal number of trajectories is 7

2) Netherlands
 - maximal trajectory time is 180 minutes
 - maximal number of trajectories is 20

#### Classes 
Classes in this project:
- Station (attr: x_cor, y_cor, name)
- Connection (attr: station1, station2, time)
- Trajectory (attr: name, stations, time)
- Network (attr: used, quality_network, stations, connections)

#### Algorithms
Algorithms are also classes, seperately defined in the folder 'algorithms'. 
These are all different algorithms and each have their own specifications.

Specifications of certain algorithms;
- random_alg: random algorithm that creates trajectories in a random    way, until all connections have been used.

- .....


#### Data- and file structure
The class Network reads in the data of the stations and connections from csv-files.



A specific algorithm calls on the Network class (and in the Network class on Station, Connection, Trajectory) and returns a certain (optimized) network of trajectories.


### Installations and python libraries to import
1) Python 3

Python libraries
1) Pandas as pd
2) Matplotlib.pyplot as plt
3) Random

### Usage and examples

