# Kedeng-Kedeng; RailNL
#### Subject: Algoritmen en Heuristieken

### Description
Project to optimize the (simplified) railnetwork in the Netherlands.

#### General description and goal
The Dutch railnet of NL used in this project consists of a number of stations, and a (different) number of connections between stations.
A connection has a certain time it takes to travel by train from station 1 to station 2.
A trajectory is a sequence of stations, with a certain time that is calculated by adding all times of the connections between all stations in the trajectory.
A network is a combination of multiple trajectories that fulfill certain requirements. A network has a certain total time and most importantly, score.

Score formula: K = p * 10000 - (T*100 + min)
- p = fraction of connections that have been driven
- T = number of trajectories in the network
- min = total time of the network in minutes
  
 __The goals is to maximize the score__ 

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
- Network (attr: stations, connections, max_trajectories, max_trajectory_time, trajectories, quality_network, used, available_connections)

#### Algorithms
Specifications of certain algorithms;
- random_alg: random algorithm that creates a network in a random way, until all connections have been used. For a trajectory the startstation and connections are randomly chosen. Trajectory length is set to the max. The network will get a random number of trajectories.

- greedy_algo: greedy algorithm that creates a network in a greedy way. The way decisions are made in the following way;
    1) startstation is chosen randomly
    2) connections are chosen based on a score that is assigned by looking forward
    3) trajectory length is maximized if possible
    4) trajectories are added if they increase the score of the network, if not, they are removed from the network. If the algorithm does not find a score-increasing trajectory within three tries, the algorithm stops.


 - hillclimber:


 - evolution_algo:

#### Data and file structure

 * /code: bevat alle code van het project
    * /code/classes: contains the code of the classes used in the project (described above)
    * /code/algorithms: contains the code of the algorithms used in this project (described above)
    * /code/visualize: contains the code for using the visualisation
 * /data: contains the datafiles necessary for running algorithms and datafiles for using the visualisation
 * /docs: contains a number of documents regarding statespace explaination, baseline algorithm and such 


#### Requirements
This project is written using Python 3.9;
In requirements.txt are all required packages to run this code succesfully. 
These can be installed using pip:
```
pip install -r requirements.txt
```

or using conda:
```
conda install --file requirements.txt
```

### Usage and examples



### Authors:
 - Odette Bonnema
 - Mette van Splunteren
 - Bas Treur


