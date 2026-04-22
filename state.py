class Aircraft:
    def __init__(self,start,target):
        self.current = start
        self.target = target
    

class State:
    def __init__(self, first_aircraft, second_aircraft, next_movements=None , value=None):
        self.current = [first_aircraft.current,second_aircraft.current]
        self.target = [first_aircraft.target,second_aircraft.target]
        self.next_movements = next_movements
        self.value = value

def is_conflict(state):
    if state.current[0]==state.current[1]:
        return True
    else:
        return False

def is_terminal(state):
    if is_conflict(state):
        return True

    if state.current[0] == state.target[0]:
        return True
    
    return False

def evaluate(state):
    if is_conflict(state) == True:
        return -10000

    A_position = state.current[0]
    B_position = state.current[1]

    A_target = state.target[0]
    B_target = state.target[1]

    A_distance = abs(A_position - A_target)
    B_distance = abs(B_position - B_target)

    final_score = -A_distance + B_distance

    return final_score

def get_next_movements(state_obj, is_maximising):
    next_movements = []
    current_a = state_obj.current[0]
    current_b = state_obj.current[1]
    
    moves = [-1, 0, 1] 

    if is_maximising:
        # Here comes the role of the first plane A
        for move in moves:
            next_a = current_a + move
            # Let's make sure that they are within the range of ten levels

            if 1 <= next_a <= 10:
                # We create a new object from the State for each movement
                new_aircraft_a = Aircraft(next_a, state_obj.target[0])
                new_state = State(new_aircraft_a, Aircraft(state_obj.current[1],state_obj.target[1]))
                next_movements.append(new_state)
    else:
        # Here comes the role of the Second plane B
        for move in moves:
            next_b = current_b + move
            # Let's make sure that they are within the range of ten levels

            if 1 <= next_b <= 10:
                # We create a new object from the State for each movement
                new_aircraft_b = Aircraft(next_b, state_obj.target[1])
                new_state = State(Aircraft(state_obj.current[0],state_obj.target[0]), new_aircraft_b)
                next_movements.append(new_state)
                
    return next_movements

def deviation(state,results):
    #total deviation = summation of ( Actual position - planned position ) 
    # the divation of A
    deviation_A = 0

    for plannedStep , actualStep in zip(setPlannedSteps(state.current[0],state.target[0]),results['decision_sequence_first']) : 
        temp = plannedStep -actualStep 
        if(temp > 0):
         deviation_A += temp
    
    # the divation of B
    deviation_B = 0

    for plannedStep , actualStep in zip(setPlannedSteps(state.current[1],state.target[1]),results['decision_sequence_second']) : 
        temp = plannedStep -actualStep
        if(temp > 0):  
            deviation_B += temp
    
    results['deviation_first'] = deviation_A
    results['deviation_second'] = deviation_B

def setPlannedSteps(s,t) :
    plannedList =[]

    if s <= t :
        update = 1
        stopCondition = t+1
    else :
        update = -1
        stopCondition = t-1
    
    for i in range(0,3) : 
        if update == 1 and s+update <= t or update == -1 and s+update >= t : 
            s+=update
        plannedList.append(s)
        plannedList.append(s)
        

    return plannedList 

