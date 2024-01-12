class Connection():
    def __init__(self, time, station1, station2):
        self.time = time
        self.station1 = station1
        self.station2 = station2
        self.used= False #TODO: Deze informatie (over de staat van je oplossing) kan beter in network gezet worden.  
