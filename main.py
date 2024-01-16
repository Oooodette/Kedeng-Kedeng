from code.classes import Station, Connection, Trajectory, Network
from code.algorithms.random_algo import Random_algo
from code.visualize import visualize as vis



if __name__ == "__main__":
    network = Network('data\ConnectiesHolland.csv', 'data\StationsHolland.csv')
    random_algo = Random_algo(network)
    # Create network from our data
    test_network = random_algo.create_network()
    test_network.get_score()
    # test_network = network.Network('data\ConnectiesHolland.csv', 'data\StationsHolland.csv')

    # test_network.load_stations()
    # test_network.load_connections()

    # test_network.connections_used()
    # test_network.create_network()

    # test_network.get_score()

    # visualize
    vis.visualize_network(test_network.stations_df, test_network.connections_df, 'data\output.csv')
