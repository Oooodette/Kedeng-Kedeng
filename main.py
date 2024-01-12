from Code.classes import stations, connection, trajectory, network
# from code.algorithms import 
# from code.algorithms import 
# from Code.visualize import visualize as vis
import pandas as pd #TODO: This should not be here

if __name__ == "__main__":
    map_name = "nl"

    # Create network from our data
    test_network = network.Network('data\ConnectiesHolland.csv', 'data\StationsHolland.csv') 
    test_network.load_stations() 
    test_network.load_connections()
    test_network.create_network()

    # show score of this network
    test_network.get_score()
    
    # # visualize 
    # trajectories_df = pd.read_csv('output.csv', skipfooter=1, engine='python') # TODO: This should probably be a function?
    # colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd',
    #     '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf',
    #     '#ff0000', '#00ff00', '#0000ff', '#ffff00', '#00ffff',
    #     '#ff00ff', '#c0c0c0', '#800000', '#008000', '#000080',
    #     '#ffffff', '#000000', '#ff69b4', '#8a2be2', '#a52a2a',
    #     '#deb887', '#5f9ea0', '#7fff00', '#d2691e', '#ff4500',
    #     '#da70d6', '#ffd700', '#00fa9a', '#1e90ff', '#dda0dd',
    #     '#008080', '#ff6347', '#40e0d0', '#ee82ee', '#f0e68c',
    #     '#dda0dd', '#ff4500', '#8b4513', '#4682b4', '#20b2aa',
    #     '#f4a460', '#7b68ee', '#98fb98', '#d2b48c', '#5f9ea0'] # TODO: This should not be here
    # vis.visualize_network(test_network.stations_df, test_network.connections_df, trajectories_df, colors)