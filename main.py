from algorithms import alpha_beta, is_conflict_avoided, minimax
from state import Aircraft ,State, setPlannedSteps, deviation
#config 0
A = Aircraft(5,8)
B = Aircraft(6,3)
initial_state = State(A,B)

results = {
    'conflicts' : 0,
    'decision_sequence_first' : [],
    'decision_sequence_second' : [],
    'is_conflict_avoided' : '',
    'nodes_evaluated' : [],
    'value' : 0,
    'nodes_evaluated_minimax' : [],
    'deviation_first':0,
    'deviation_second':0
}
minimax(initial_state,6,True,results)
results['value'],path=alpha_beta(initial_state, 6, float('-inf'), float('inf'), True, results)
print(results['value'])
for state in path :
    results['decision_sequence_first'].append(state.current[0])
    results['decision_sequence_second'].append(state.current[1])
print(results['conflicts'])
print(results['nodes_evaluated'])
print(results['nodes_evaluated_minimax'])
print(results['decision_sequence_first'])
print(results['decision_sequence_second'])
deviation(state,results)
print(results['deviation_first'])
print(results['deviation_second'])
is_conflict_avoided(results)
print(results['is_conflict_avoided'])

print("Welcom  to the ai project")