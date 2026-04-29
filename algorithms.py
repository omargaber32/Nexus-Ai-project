from state import Aircraft, State, is_conflict ,is_terminal, evaluate, get_next_movements, deviation
def alpha_beta(state , depth ,alpha , beta,is_maximising, results):
    
    if is_terminal(state) or depth == 0 :
        results['nodes_evaluated'].append(state.current)
        if is_conflict(state) :
            results['conflicts']+=1
        return evaluate(state) ,[]
    
    if is_maximising:
        best_value = float('-inf')
        best_path=[]
        state.next_movements = get_next_movements(state,is_maximising)
        for next_movement in state.next_movements:
            next_movement.value ,path = alpha_beta(next_movement, depth-1, alpha, beta, False, results)
            if next_movement.value > best_value:
                best_value = next_movement.value
                best_path = [next_movement]+path
            alpha = max(alpha, next_movement.value)
            if beta <= alpha :
                break
        return best_value, best_path

    if not is_maximising:
        min_value = float('inf')
        best_path = []
        state.next_movements = get_next_movements(state,is_maximising)
        for next_movement in state.next_movements:
            next_movement.value ,path= alpha_beta(next_movement, depth-1, alpha, beta, True, results)
            if next_movement.value < min_value:
                min_value = next_movement.value
                best_path = [next_movement]+path
            beta = min(beta, next_movement.value)
            if beta <= alpha :
                break
        return min_value , best_path



def minimax(state , depth ,is_maximising ,results):

    if is_terminal(state) or depth == 0 :
        results['nodes_evaluated_minimax'].append(state.current)
        return evaluate(state)
    
    if is_maximising :
        best_value = float('-inf')
        state.next_movements = get_next_movements(state,True)
        
        for next_movement in state.next_movements :
            eval = minimax(next_movement,depth-1,False,results)
            best_value = max(best_value,eval)
        return best_value
    else :
        min_value = float('inf')
        state.next_movements = get_next_movements(state,False)

        for next_movement in state.next_movements :
            eval = minimax(next_movement,depth-1,True,results)
            min_value = min(min_value,eval)
        return min_value

    
#should be moved later  
def is_conflict_avoided(results):
    if  results['conflicts'] == 0 :
        results['is_conflict_avoided'] = 'Conflict can not happen'
    if  results['value'] == -10000  :
        results['is_conflict_avoided'] = 'Conflict happened'
    if  results['value'] != -10000 and results['conflicts'] > 0 :
        results['is_conflict_avoided'] = 'Conflict avoided'