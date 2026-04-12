from state import Aircraft, State, is_conflict ,is_terminal, evaluate, get_children, deviation
def alpha_beta(state , depth ,alpha , beta,is_maximising, results):
    
    if is_terminal(state) or depth == 0 :
        results['nodes_evaluated']+=1
        if is_conflict(state) :
            results['conflicts']+=1
        return evaluate(state)
    
    if is_maximising:
        max_eval = float('-inf')
        state.children = get_children(state,is_maximising)
        for child in state.children:
            child.value = alpha_beta(child, depth-1, alpha, beta, False, results)
            max_eval = max(max_eval, child.value)
            alpha = max(alpha, child.value)
            if beta <= alpha :
                break
        return max_eval

    if not is_maximising:
        min_eval = float('inf')
        state.children = get_children(state,is_maximising)
        for child in state.children:
            child.value = alpha_beta(child, depth-1, alpha, beta, True, results)
            min_eval = min(min_eval, child.value)
            beta = min(beta, child.value)
            if beta <= alpha :
                break
        return min_eval
    

#should be moved later  
def is_conflict_avoided(results):
    if  results['eval'] != -10000 and results['conflicts'] == 0 :
        results['is_conflict_avoided'] = 'Conflict can not happen'
    if  results['eval'] == -10000 and results['conflicts'] > 0 :
        results['is_conflict_avoided'] = 'Conflict happened'
    if  results['eval'] != -10000 and results['conflicts'] > 0 :
        results['is_conflict_avoided'] = 'Conflict avoided'