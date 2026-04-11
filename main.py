from alpha_beta import alpha_beta
from minimax import minimax
from state import Aircraft ,State 
#config 0
A = Aircraft(8,5)
B = Aircraft(6,3)
initial_state = State(A,B)
first = alpha_beta(initial_state, 6, float('-inf'), float('inf'), True)
first_sequence_A= first['decision_sequence_first'] 
first_sequence_B = first['decision_sequence_second']
first_avoid_conflict = first['is_conflict_avoided'] 
first_evaluted_nodes = first['nodes_evaluated']

print("Welcom  to the ai project")