from code.classes import stations, connection, trajectory, network
# from code.algorithms import
from code.algorithms import random_algo
from code.visualize import visualize as vis



if __name__ == "__main__":

    # Create network from our data
    test_network = random_algo.create_network('data\ConnectiesHolland.csv', 'data\StationsHolland.csv')
    # test_network = network.Network('data\ConnectiesHolland.csv', 'data\StationsHolland.csv')

    # test_network.load_stations()
    # test_network.load_connections()

    # test_network.connections_used()
    # test_network.create_network()

    # test_network.get_score()

    # # visualize
    # vis.visualize_network(test_network.stations_df, test_network.connections_df, 'data\output.csv')
