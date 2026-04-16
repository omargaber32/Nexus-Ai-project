from state import Aircraft, State, is_conflict ,is_terminal, evaluate, get_children, deviation
def alpha_beta(state , depth ,alpha , beta,is_maximising, results):
    
    if is_terminal(state) or depth == 0 :
        results['nodes_evaluated']+=1
        if is_conflict(state) :
            results['conflicts']+=1
        return evaluate(state) ,[]
    
    if is_maximising:
        max_eval = float('-inf')
        best_path=[]
        state.children = get_children(state,is_maximising)
        for child in state.children:
            child.value ,path = alpha_beta(child, depth-1, alpha, beta, False, results)
            if child.value > max_eval:
                max_eval = child.value
                best_path = [child]+path
            alpha = max(alpha, child.value)
            if beta <= alpha :
                break
        return max_eval, best_path

    if not is_maximising:
        min_eval = float('inf')
        best_path=[]
        state.children = get_children(state,is_maximising)
        for child in state.children:
            child.value ,path= alpha_beta(child, depth-1, alpha, beta, True, results)
            if child.value < min_eval:
                min_eval = child.value
                best_path = [child]+path
            beta = min(beta, child.value)
            if beta <= alpha :
                break
        return min_eval , best_path



def minimax(self,state , depth ,alpha , beta,is_maximising ):
    return
    
#should be moved later  
def is_conflict_avoided(results):
    if  results['eval'] != -10000 and results['conflicts'] == 0 :
        results['is_conflict_avoided'] = 'Conflict can not happen'
    if  results['eval'] == -10000 and results['conflicts'] > 0 :
        results['is_conflict_avoided'] = 'Conflict happened'
    if  results['eval'] != -10000 and results['conflicts'] > 0 :
        results['is_conflict_avoided'] = 'Conflict avoided'