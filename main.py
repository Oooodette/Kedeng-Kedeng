from code.classes import Station, Connection, Trajectory, Network
from code.algorithms.random_algo import Random_algo
from code.visualize import visualize as vis



if __name__ == "__main__":
    network = Network('data\ConnectiesNationaal.csv', 'data\StationsNationaal.csv')
    random_algo = Random_algo(network)
    # Create network from our data
    test_network = random_algo.create_network()
    test_network.get_score()

    # visualize
    vis.visualize_network(test_network.stations_df, test_network.connections_df, 'data\output.csv')
