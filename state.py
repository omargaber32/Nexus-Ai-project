class Aircraft:
    def __init__(self,start,target):
        self.start = start
        self.target = target
    

class State:
    def __init__(self, first_aircraft, second_aircraft, children=None , value=None):
        self.state = [first_aircraft.start,second_aircraft.start]
        self.target = [first_aircraft.target,second_aircraft.target]
        self.children = children
        self.value = value

def is_conflict(state):
    return

def is_terminal(state):
    return

def evaluate(state):
    return

def get_children(state,is_maximising):
    return

def deviation(state):
    return