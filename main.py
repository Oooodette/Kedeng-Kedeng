from Code.classes import stations, connection, trajectory, network
# from code.algorithms import 
# from code.algorithms import 
from Code.visualize import visualize as vis


if __name__ == "__main__":

    # Create network from our data
    test_network = network.Network('data\ConnectiesHolland.csv', 'data\StationsHolland.csv') 
    test_network.load_stations() 
    test_network.load_connections()
    test_network.create_network()

    # show score of this network
    test_network.get_score()
    
    vis.visualize_network(test_network.stations_df, test_network.connections_df,'data\output.csv')
 