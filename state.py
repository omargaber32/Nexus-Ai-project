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

def get_children(state_obj, is_maximising):
    children = []
    current_a = state_obj.state[0]
    current_b = state_obj.state[1]
    
    moves = [-1, 0, 1] 

    if is_maximising:
        # Here comes the role of the first plane A
        for move in moves:
            next_a = current_a + move
            # Let's make sure that they are within the range of ten levels

            if 1 <= next_a <= 10:
                # We create a new object from the State for each movement
                new_aircraft_a = Aircraft(next_a, state_obj.first_aircraft.target)
                new_state = State(new_aircraft_a, state_obj.second_aircraft)
                children.append(new_state)
    else:
        # Here comes the role of the Second plane B
        for move in moves:
            next_b = current_b + move
            # Let's make sure that they are within the range of ten levels

            if 1 <= next_b <= 10:
                # We create a new object from the State for each movement
                new_aircraft_b = Aircraft(next_b, state_obj.second_aircraft.target)
                new_state = State(state_obj.first_aircraft, new_aircraft_b)
                children.append(new_state)
                
    return children

def deviation(state,results):
    #total deviation = summation of ( Actual position - planned position ) 
    # the divation of A
    deviation_A = 0

    for plannedStep , actualStep in zip(setPlannedStepsInList(state.state[0],state.target[0]),results['decision_sequence_first']) : 
        temp = actualStep -plannedStep 
        deviation_A += temp
    
    # the divation of B
    deviation_B = 0

    for plannedStep , actualStep in zip(setPlannedStepsInList(state.state[1],state.target[1]),results['decision_sequence_second']) : 
        temp = actualStep -plannedStep  
        deviation_B += temp
    
    return [deviation_A,deviation_B]

def setPlannedStepsInList(s,t) :
    plannedList =[]

    if s <= t :
        update = 1
        stopCondition = t+1
    else :
        update = -1
        stopCondition = t-1
    
    for i in range(s,stopCondition,update) : 
        plannedList.append(i)

    return plannedList 

