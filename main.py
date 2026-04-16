from algorithms import alpha_beta, is_conflict_avoided, best_sequence, minimax
from state import Aircraft ,State 
#config 0
A = Aircraft(8,5)
B = Aircraft(6,3)
initial_state = State(A,B)

results = {
    'conflicts' : 0,
    'decision_sequence_first' : [],
    'decision_sequence_second' : [],
    'is_conflict_avoided' : '',
    'nodes_evaluated' : 0,
    'eval' : 0
}
results['eval'],path=alpha_beta(initial_state, 6, float('-inf'), float('inf'), True, results)
for state in path :
    results['decision_sequence_first'].append(state.state[0])
    results['decision_sequence_second'].append(state.state[1])

is_conflict_avoided(results)

print("Welcom  to the ai project")