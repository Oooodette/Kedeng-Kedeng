
def calc_statespace(max_traject_time, max_traject_num):
    """calculate statespace with given assumptions"""

    statespace = 0
    for i in range(max_traject_time):
        
        nr_connections_trajectory = (i/5)
        n = 3
        r = nr_connections_trajectory
        nr_stations = 22

        nr_of_trajectories_total = (n**r) * nr_stations

        for j in range(max_traject_num):
            num_combinations = j * nr_of_trajectories_total
            statespace += num_combinations

    print(statespace)

calc_statespace(120, 7)
