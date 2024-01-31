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
- random_algo: 
    1) create an empty network
    2) pick a random start station 
    3) pick a random next connection from this station
    4) keep picking connections until maximum trajectory time is reached
    5) keep creating these random trajectories for a random amount of times between 0 and the maximum number of trajectories allowed


- greedy_algo: greedy algorithm that creates a network in a greedy way. The way decisions are made in the following way;
    1) startstation is chosen randomly
    2) connections are chosen based on a score that is assigned by looking forward
    3) trajectory length is maximized if possible
    4) trajectories are added if they increase the score of the network, if not, they are removed from the network. If the algorithm does not find a score-increasing trajectory within three tries, the algorithm stops.


 - hillclimber:
    1) start with a random network
    2) choose between three actions: add a trajectory, remove a trajectory or replace a trajectory
    3) perform this action and check whether score has improved
    4) if score did not improve, undo your previous action
    5) continue this loop for an 'attempts' number of iterations


 - evolution_algo: evolution algorithm that creates a network using multiple generations of networks and an evolution 
    1) start with 96 networks made with another algorithm, for example with the random algorithm
    2) divide the networks in groups of 8 
    3) from every group of 8, chose one network that will survive. 
    4) the survivor is chosen as follows: (source: www.wikipedia.com)
        - choose the best network from the tournament with probability 0.8
        - choose the second best network with probability 0.8*(1-0.8)
        - choose the third best network with probability 0.8*((1-0.8)^2)
        - and so on
    5) with this 12 survivors keep selecting two random network to create an offspring 
    6) an offspring is created as follows: 
        - add all the trajectories of the parents together 
        - for every amount of trajectories in a network, make a given amount of possible combinations of the trajectories 
        - change the trajectories of a network for every combination and calculate the score 
        - save the network with the best score 
    7) create 96 networks this way 
    8) these 96 networks are the new generation 
    9) repeat from step 2 with these 96 networks 
    10) do this for a given amount of generations 
    


#### Data and file structure

 * /code: bevat alle code van het project
    * /code/classes: contains the code of the classes used in the project (described above)
    * /code/experiments: contains all experiments that were done using the algorithms
    * /code/algorithms: contains the code of the algorithms used in this project (described above)
    * /code/visualize: contains the code for using the visualisation
 * /data: contains the datafiles necessary for running algorithms and datafiles for using the visualisation
 * /docs: contains a number of documents regarding statespace explaination, baseline algorithm and such 

#### Requirements
This project is written using Python 3.9;
requirements.txt contains all required packages to run this code succesfully. 
These can be installed using pip:
```
pip install -r requirements.txt
```

or using conda:
```
conda install --file requirements.txt
```

### Usage and examples
The code can be run by entering:

```
python main.py
```

To run the code, 5 input arguments are required:
- output: filepath for the output generated by a network
- visualize_output: filepath for the output of the visualization of the network
- area: specifies area network is created in (either holland or nederland)
- start_network: specifies which algorithm is used to create initial network (either greedy, hillclimber or random). 
- algorithm: specifies which algorithms is used for optimization of network (either hillclimber or evolution). 

All arguments are set to default setting. Manual changes can be made, for example by entering:

```
python main.py -sn random -algo evolution
```

All default settings and options per argument can be accessed by entering:

```
python main.py -h
```
NOTE: If hillclimber is chosen, an initial question is asked in the terminal. Enter either of the two presented options and the program will run.

If you want to run our experiments instead of one run, enter:

```
python main.py -exp
```
It will ask which experiment you want to run, enter: evolution, greedy, hillclimber or random.

### Authors:
 - Odette Bonnema
 - Mette van Splunteren
 - Bas Treur


