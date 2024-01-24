class Hillclimber():
    """
    Class Hillclimber: algorithm that keeps randomly changing a small part of a network until score doesn't improve anymore;
        Attributes:
        - network: an instance of the Network class that was created beforehand.
        - attempts: amount of times hillclimber tries to improve the score until stopping.

        Methods:
        - improving: determine whether current change improves total network score
        - add: add new trajectory to network while score is improving
        - replace: replace existing trajectory with new trajectory while score is improving
    """
    
    def __init__(self, network, attempts):
        self.network = network 
        self.attempts = attempts

    def improving(self, previous_score):
        
        if self.network.get_score() > previous_score:
            return True
        else:
            return False
        
    def add(self):

        previous_score = 0
        # while score is improving, add more trajectories
        add_count = 0
        while add_count < self.attempts:
            #TODO: create greedy trajectory 
            self.network.add_trajectory
            if not self.improving(previous_score):
                #TODO: remove trajectory
                add_count += 1

    def replace(self):
        replace_count = 0
        previous_score = 0 

        while replace_count < self.attempts:
            #TODO: save trajectory before removing in case it doesn't improve score 
            self.network.remove_trajectory()

            #TODO: create greedy trajectory
            self.network.add_trajectory
            if not self.improving(previous_score):

    def change_network(self, method = 'add'):
        
        self.network.add_trajectory


    def run(self):
        count = 0
        #TODO: calculate score
        while count < self.attempts:
            self.change_network()
            count = 
        self.add()
        self.replace()



     

