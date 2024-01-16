from code.classes import Station, Connection, Trajectory, Network
from code.algorithms.random_algo import Random_algo
from code.visualize import visualize as vis


minimal_score = 8900

if __name__ == "__main__":
    score = -1000
    it = 0
    nr_traj = 1000

    while nr_traj > 20 or score < minimal_score:
        network = Network('data\ConnectiesHolland.csv', 'data\StationsHolland.csv')
        random_algo = Random_algo(network)

        # Create network from our data
        test_network = random_algo.create_network()
        score = test_network.get_score()
        nr_traj = len(test_network.trajectories)

        it += 1


    print(it)
    print(nr_traj)
    print(score)
    network.save_network()

    # visualize
    vis.visualize_network(test_network.stations_df, test_network.connections_df, 'data\output.csv')
