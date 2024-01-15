class Station():
    """
    Class that creates a station instance 

    Attributes:
    - name (string): the name of the station 
    - x_cor (float): the x coordinate of the stations location 
    - y_cor (float): the y coordinate of the stations location 
    """
    def __init__(self, name, x_cor, y_cor):
        self.name = name
        self.x_cor = x_cor
        self.y_cor = y_cor
