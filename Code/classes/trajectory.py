class Trajectory():
    """
    Class that creates a trajectory of train connections 

    Attributes:
    - name (int): the number of the trajectory, the first, second etc. 
    - stations (list): list of stations to check the connections each station has 
    - time (int): the total time of the trajectory 
    - route (list): list of the connections of the trajectory 
    """
    def __init__(self, name, stations, time):
        self.name = name
        self.stations = stations
        self.time = time
        self.route = []
