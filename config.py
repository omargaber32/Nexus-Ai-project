class config:
    container = []

    results = {
    'conflicts' : 0,
    'decision_sequence_first' : [],
    'decision_sequence_second' : [],
    'is_conflict_avoided' : '',
    'nodes_evaluated' : [],
    'eval' : 0,
    'nodes_evaluated_minimax' : [],
    'deviation_first':0,
    'deviation_second':0
    }

    def __init__(self, a_start,a_target, b_start , b_target,maximising = True,depth=6,alpha=float('-inf'),beta=float('inf')):
        #add data validation
        self.a_start = a_start
        self.a_target = a_target
        self.b_start = b_start
        self.b_target = b_target
        self.maximising = maximising
        self.depth = depth
        self.alpha = alpha
        self.beta = beta
        self.outcomes(self.results)
        self.save_results(self.results)
        self.reset_results(self.results)


    def reset_results(results):
        return
    
    def save_results(results):
        return
    
    def outcomes(results):
        return
    
    def summary_table(container):
        return
    
