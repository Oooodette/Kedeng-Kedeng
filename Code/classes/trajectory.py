class Trajectory():
    """
    Class that creates a trajectory of train connections 

    Attributes:
    - name (int): the number of the trajectory, the first, second etc. 
    - stations (list): list of stations to check the connections each station has 
    - time (int): the total time of the trajectory 
    - route (list): list of the connections of the trajectory 
    - color (str): starts of as None, but is assigned a color during visualize
    """
    def __init__(self, name, stations, route, time):
        self.name = name
        self.stations = stations
        self.time = time
        self.route = route
        self.color = None

    def __hash__(self):
        return hash(str(self))
    
    def __repr__(self):
        return str(self.stations) 
