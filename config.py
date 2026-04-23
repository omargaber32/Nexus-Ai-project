from algorithms import alpha_beta, minimax, is_conflict_avoided
from state import deviation, State, Aircraft
container = []
class Config:

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

    def __init__(self, a_start,a_target, b_start , b_target,maximising = True,depth=6,alpha=float('-inf'),beta=float('inf')):
        def validate (val):
            if val < 0: return 0
            if val > 10: return 10
            return val
        #add data validation
        self.a_start = a_start
        self.a_target = a_target
        self.b_start = b_start
        self.b_target = b_target
        self.maximising = maximising
        self.depth = depth
        self.alpha = alpha
        self.beta = beta
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
    
    def save_results(self,results):
        container.append(self.results)
    
    def outcomes(self,results):
        print(f"Decision sequence for the first plane: {results['decision_sequence_first']}")
        print(f"Decision sequence for the second plane: {results['decision_sequence_second']}")
        print(f"Is conflict avoided: {results['is_conflict_avoided']}")
        print(f"Deviation for the first plane: {results['deviation_first']}")
        print(f"Deviation for the second plane: {results['deviation_second']}")
        #Organize the output in a table format
        print("\n" + "="*70)
        print(f"{'Nodes evaluated alphabeta':<35} | {'Nodes evaluated minimax':<35}")
        print("-" * 70)
        #transfer the list of nodes evaluated to string and print only the first 33 characters followed by '...' to indicate that there are more nodes
        str_ab = str(results['nodes_evaluated'])
        str_mm = str(results['nodes_evaluated_minimax'])
        print(f"{str_ab[:33]+'..':<35} | {str_mm[:33]+'..':<35}")
        #print the lengthes of the nodes evaluated for both algorithms
        len_ab = len(results['nodes_evaluated'])
        len_mm = len(results['nodes_evaluated_minimax'])
        print(f"{'Count: ' + str(len_ab):<35} | {'Count: ' + str(len_mm):<35}")
        print("="*70 + "\n")
    
def summary_table():
    #Side titles
    row_names = [
        "Path of A",
        "Path of B",
        "Deviation of A",
        "Deviation of B",
        "Len(Nodes evaluated alphabeta)",
        "Is conflict avoided"
    ]
    #Count the elements which add to each config in the container
    num_attributes = 8
    col_width = 25
    header_width = 30
    # Calculate the number of the configs which in the container
    num_configs = len(container) 
    # Print the header
    header_row = f"{'Attribute':<{header_width}}"
    for i in range(num_configs):
        header_row += f"| {'Config ' + str(i+1):<{col_width}}"
    print("\n" + "=" * len(header_row))
    print(header_row)
    print("-" * len(header_row))
    # print rows via pull the values with index
    for i, name in enumerate(row_names):
        row_str = f"{name:<{header_width}}"
        for c_idx in range(num_configs):
            start_pos = c_idx * num_attributes
    #Determine the location of the value based on its order in results
    if name == "Path of A": val = container[start_pos + 1]
    elif name == "Path of B": val = container[start_pos + 2]
    elif name == "Deviation of A": val = container[start_pos + 8]
    elif name == "Deviation of B": val = container[start_pos + 7]
    elif name == "Len(Nodes evaluated alphabeta)": val = len(container[start_pos + 4])
    elif name == "Is conflict avoided": val = container[start_pos + 3]
    
    row_str += f"| {str(val)[:20]:<{col_width}}"
    print(row_str)

    print("=" * len(header_row) + "\n")
    
