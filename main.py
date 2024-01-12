from code.classes import stations, connection, trajectory, network
# from code.algorithms import
# from code.algorithms import
from code.visualize import visualize as vis

if __name__ == "__main__":
    map_name = "nl"

    # Create network from our data
    test_network = Network('data\ConnectiesHolland.csv', 'data\StationsHolland.csv')


    test_network.create_stations()
    test_network.create_connections()
    test_network.create_network()

    # show score of this network
    test_network.get_score()

    # visualize
    vis.visualize_network('data/StationsNationaal.csv', 'data/ConnectiesNationaal.csv', 'output.csv')
