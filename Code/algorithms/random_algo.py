def create_station_list(self, current_station):
    # create empty list to later select next connection from
    all_connections = []

    # loop through your list of connections and look for a connection that has the current station as station 1 or 2
    for connection in self.connections:

    if connection.station1 == current_station or connection.station2 == current_station:

        # create list of all stations that have current station as station 1
        all_connections.append(connection)
        
    return all_connections

         
def create_trajectory(self):
        #TODO: Dit is een random algoritme, zet dit in mapje algoritme en roep hem aan. We willen geen algoritmes in de oplossing. 
        # pick a random station from the list of stations
        previous_connection = None
        position = random.randint(0, len(self.stations)-1)
        current_station = self.stations[position].name
        time = 0
        trajectory_stations = [current_station]

        # only add more connections if total time is below 120
        while time < 120:

            # create empty list to later select next connection from
            all_connections = []

            # loop through your list of connections and look for a connection that has the current station as station 1 or 2
            for connection in self.connections:
               
                if connection.station1 == current_station or connection.station2 == current_station:

                    # create list of all stations that have current station as station 1
                    all_connections.append(connection)
            
            # pick one of the connections with correct station
            new_connection = self.pick_valid_connection(all_connections, previous_connection, time) 
            
            # if valid connection is found, add it to the trajectory
            if new_connection != None:

                # pick correct station to move further with
                if current_station == new_connection.station1:
                    current_station = new_connection.station2
                    previous_station = new_connection.station1
                else: 
                    current_station = new_connection.station1
                    previous_station = new_connection.station2
                time += new_connection.time 
                trajectory_stations.append(current_station)
                new_connection.used = True
                previous_connection = new_connection 
         

            # if no valid connection is found, break the loop
            else:
                break
            
        new_trajectory = Trajectory('x', trajectory_stations, time) 
        return new_trajectory