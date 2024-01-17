from code.classes import Station, Connection, Trajectory, Network
from code.algorithms.random_algo import Random_algo
#from code.visualize import visualize as vis


if __name__ == "__main__":

    #difine criteria
    minimal_score = 0
    score = -1000
    it = 0
    nr_traj = 1000

    #looping until criteria are met
    while nr_traj > 7 or score < minimal_score:
        network = Network('data\ConnectiesHolland.csv', 'data\StationsHolland.csv', 7, 120)
        random_algo = Random_algo(network)

        # Create network from our data
        test_network = random_algo.create_network()
        score = test_network.get_score()
        nr_traj = len(test_network.trajectories)

        it += 1

    #printing #iterations, number of trajectories and score of the network
    print(it)
    print(nr_traj)
    print(score)

    #explicitly save the network that fulfills the criteria
    network.save_network()

    #visualize
    #vis.visualize_network(test_network.stations_df, test_network.connections_df, 'data\output.csv')
