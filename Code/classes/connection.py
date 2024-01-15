class Connection():
    """ 
    Class that creates a train connection instance between two stations 

    Attributes:
    - time (int): the time it takes to drive the connection 
    - station1 (string): the first station of the connection 
    - station2 (string): the second station of the connection 
    """
    def __init__(self, time, station1, station2):
        self.time = time
        self.station1 = station1
        self.station2 = station2
