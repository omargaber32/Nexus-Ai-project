from algorithms import alpha_beta, minimax, is_conflict_avoided
from state import deviation, State, Aircraft
from tabulate import tabulate
from copy import deepcopy
container = []
class Config:

    results = {
    'decision_sequence_first' : [],
    'decision_sequence_second' : [],
    'deviation_first':0,
    'deviation_second':0,
    'nodes_evaluated' : [],
    'is_conflict_avoided' : '',
    'value' : 0,
    'nodes_evaluated_minimax' : [],
    'conflicts' : 0,
    'num_of_alphabeta_nodes':0,
    'num_of_minimax_nodes':0,
    }

    def __init__(self, a_start,a_target, b_start , b_target,maximising = True,depth=6,alpha=float('-inf'),beta=float('inf')):
        
        self.a_start  = self.validate(a_start,  1, 10, "The start of first aircraft")
        self.a_target = self.validate(a_target, 1, 10, "The target of first aircraft")
        self.b_start  = self.validate(b_start,  1, 10, "The start of second aircraft")
        self.b_target = self.validate(b_target, 1, 10, "The target of first aircraft")
        self.depth    = self.validate(depth,    1,  6, "The depth")
        self.maximising = maximising
        self.alpha = alpha
        self.beta  = beta
        self.A = Aircraft(self.a_start,self.a_target)
        self.B = Aircraft(self.b_start,self.b_target)
        current_state = State(self.A, self.B)
        self.results['value'], self.path = alpha_beta(state=current_state, depth=self.depth, alpha=self.alpha, beta=self.beta, is_maximising=self.maximising, results=self.results)
        for state in self.path :
            self.results['decision_sequence_first'].append(state.current[0])
            self.results['decision_sequence_second'].append(state.current[1])
        minimax(state = current_state, depth = self.depth, is_maximising = self.maximising, results = self.results)
        deviation(current_state, self.results)
        is_conflict_avoided(self.results)
        self.outcomes(self.results)
        self.save_results(self.results)
        self.reset_results(self.results)

    def validate(self,val, min_val, max_val, name):
            if val < min_val:
                print(f"Warning: {name} = {val} is below minimum ({min_val}), set to {min_val}.")
                return min_val
            if val > max_val:
                print(f"Warning: {name} = {val} exceeds maximum ({max_val}), set to {max_val}.")
                return max_val
            return val

    def save_results(self,results):
        results['a_start'] = self.a_start
        results['a_target'] = self.a_target
        results['b_start'] = self.b_start
        results['b_target'] = self.b_target
        container.append(deepcopy(results))

    def reset_results(self,results):  
        results['conflicts'] = 0
        results['decision_sequence_first'] = []
        results['decision_sequence_second'] = []
        results['is_conflict_avoided'] = ''
        results['nodes_evaluated'] = []
        results['value'] = 0
        results['nodes_evaluated_minimax'] = []
        results['deviation_first'] = 0
        results['deviation_second'] = 0
    
    
    
    def outcomes(self,results):
        print(f"Decision sequence for the first plane: {results['decision_sequence_first']}")
        print(f"Decision sequence for the second plane: {results['decision_sequence_second']}")
        print(f"Is conflict avoided: {results['is_conflict_avoided']}")
        print(f"Deviation for the first plane: {results['deviation_first']}")
        print(f"Deviation for the second plane: {results['deviation_second']}")
        str_ab = str(results['nodes_evaluated'])
        str_mm = str(results['nodes_evaluated_minimax'])
        len_ab = results['num_of_alphabeta_nodes']=len(results['nodes_evaluated'])
        len_mm = results['num_of_minimax_nodes']=len(results['nodes_evaluated_minimax'])
        rows = [
            ["Nodes", str_ab[:33] + '..', str_mm[:33] + '..'],
            ["Count", len_ab, len_mm],
        ]
        headers = ["", "Nodes evaluated alphabeta", "Nodes evaluated minimax"]
        print(tabulate(rows, headers=headers, tablefmt="rounded_grid"))

def summary_table():
    field_map = {
    'decision_sequence_first'  : 'Path of A',
    'decision_sequence_second' : 'Path of B',
    'deviation_first'          : 'Deviation of A',
    'deviation_second'         : 'Deviation of B',
    'num_of_alphabeta_nodes'   : 'number of alphabeta nodes',
    'num_of_minimax_nodes'     : 'number of minimax nodes',
    'is_conflict_avoided'      : 'Is conflict avoided',
    }

    rows = [
        [label] + [c[key] for c in container]
        for key, label in field_map.items()
    ]

    headers = ["Field"] + [f"config[{i+1}]" for i in range(len(container))]

    print(tabulate(rows, headers=headers, tablefmt="rounded_grid"))
