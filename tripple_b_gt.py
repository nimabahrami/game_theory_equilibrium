import itertools
import pprint
import sympy
import re


class Player:
    def __init__(self, name, strategies):
        self.name = name
        self.strategies = strategies
        self.strategies_space = []


class ExtensiveForm:
    # payoff_data structure:
    # {
    #   'p1': {'var_name': {'case1': val, ...}, ...},
    #   'p2': {'var_name': {'case1': val, ...}, ...}
    # }
    def __init__(self, nature, player1, player2, payoff_data, p1_function=None, p2_function=None):
        self.nature = nature
        self.player1 = player1
        self.player2 = player2
        self.payoff_data = payoff_data
        self.p1_function = p1_function
        self.p2_function = p2_function
        self.strategies_space = self.strategies_space_function()
        self.pure_strategies = self.generate_pure_strategies()

    def payoff(self, case):
        # Helper to sanitize variable names (replace spaces with underscores, lower case)
        def sanitize(name):
            return name.strip().lower().replace(" ", "_")

        # Helper to evaluate payoff for a player
        def evaluate_payoff(player_key, function_str):
            if not function_str:
                # Default: Summation of all variables
                total = 0
                if player_key in self.payoff_data:
                    for var_data in self.payoff_data[player_key].values():
                        total += var_data.get(case, 0)
                return total
            
            # Sanitize input: remove leading/trailing whitespace and lower case
            function_str = function_str.strip().lower()
            
            # Smart Sanitization: Replace spaces between words with underscores
            # This regex looks for a space that is preceded by a word char and followed by a word char
            # e.g. "national wealth" -> "national_wealth"
            # But "wealth + tax" -> "wealth + tax" (because + is not a word char)
            function_str = re.sub(r'(?<=[a-z0-9])\s+(?=[a-z0-9])', '_', function_str)
            
            try:
                # 1. Prepare symbol values for this case
                symbol_values = {}
                if player_key in self.payoff_data:
                    for var_name, var_data in self.payoff_data[player_key].items():
                        sanitized_name = sanitize(var_name)
                        symbol_values[sanitized_name] = var_data.get(case, 0)
                
                # 2. Parse the expression
                expr = sympy.sympify(function_str)
                
                # 3. VALIDATION: Check for undefined variables
                free_symbols = expr.free_symbols
                defined_vars = set(symbol_values.keys())
                
                undefined_vars = []
                for sym in free_symbols:
                    sym_name = str(sym)
                    if sym_name not in defined_vars:
                        undefined_vars.append(sym_name)
                
                if undefined_vars:
                    raise ValueError(f"Undefined variables in payoff function for {player_key}: {', '.join(undefined_vars)}")
                
                # 4. Substitute values
                result = expr.subs(symbol_values)
                
                return result
            except Exception as e:
                # Propagate the error so it can be shown to the user
                raise e

        p1_payoff = evaluate_payoff('p1', self.p1_function)
        p2_payoff = evaluate_payoff('p2', self.p2_function)
                
        return (p1_payoff, p2_payoff)

    def strategies_space_function(self):
        list_of_strategies_dict = []
        list_of_strategies = list(itertools.product(self.nature.strategies, self.player1.strategies, self.player2.strategies))
        cases = CaseBuilder(list_of_strategies, self.nature.strategies)
        

        for items in list_of_strategies:
            cases.case_definition(items)
            dict_of_strategies = {}
            dict_of_strategies[self.nature.name] = items[0]
            dict_of_strategies[self.player1.name] = items[1]
            dict_of_strategies[self.player2.name] = items[2]
            dict_of_strategies['case'] = cases.case
            dict_of_strategies['payoff'] = self.payoff(cases.case)
            list_of_strategies_dict.append(dict_of_strategies)
        return list_of_strategies_dict

    def generate_pure_strategies(self):
        # Player 1 strategies (conditional on Nature)
        # Nature has 2 strategies: stable, unstable
        # P1 has 2 strategies: intervene, not intervene
        # P1 pure strategy is a map: Nature State -> P1 Action
        p1_actions = self.player1.strategies
        nature_states = self.nature.strategies
        
        # Generate all mappings from Nature to P1
        # There are len(p1_actions) ** len(nature_states) = 2^2 = 4 strategies
        p1_pure_strategies = []
        for action_combo in itertools.product(p1_actions, repeat=len(nature_states)):
            strategy = {state: action for state, action in zip(nature_states, action_combo)}
            p1_pure_strategies.append(strategy)
            
        # Player 2 strategies (conditional on Player 1)
        # P1 has 2 actions: intervene, not intervene
        # P2 has 2 actions: relocate, not relocate
        # P2 pure strategy is a map: P1 Action -> P2 Action
        p2_actions = self.player2.strategies
        p1_possible_actions = self.player1.strategies # The actions P1 can take, which P2 observes
        
        # Generate all mappings from P1 Action to P2 Action
        # There are len(p2_actions) ** len(p1_possible_actions) = 2^2 = 4 strategies
        p2_pure_strategies = []
        for action_combo in itertools.product(p2_actions, repeat=len(p1_possible_actions)):
            strategy = {p1_action: p2_action for p1_action, p2_action in zip(p1_possible_actions, action_combo)}
            p2_pure_strategies.append(strategy)
            
        return {
            self.player1.name: p1_pure_strategies,
            self.player2.name: p2_pure_strategies
        }

class CaseBuilder:
    def __init__(self, strategies, nature_states):
        self.strategies_list = strategies
        self.case = None
        # Map dynamic states to logical 'stable'/'unstable' roles
        # Assuming index 0 is 'stable' (prob 1-ro in original, but wait...)
        # In original: nature=('stable', 'unstable'). Index 0=stable, Index 1=unstable.
        # In payoff logic: state_0 (index 0) was associated with (1-ro) term in my previous thought, 
        # BUT in user's formula: ro * unstable + (1-ro) * stable.
        # So index 0 (stable) -> (1-ro). Index 1 (unstable) -> ro.
        
        self.state_stable = nature_states[0]
        self.state_unstable = nature_states[1]

    def case_definition(self,plays):
        # plays[0] is nature state
        # plays[1] is regulator action
        # plays[2] is firm action
        
        nature_state = plays[0]
        regulator_action = plays[1]
        firm_action = plays[2]
        
        if firm_action == 'relocate' and regulator_action == 'intervene' and nature_state == self.state_unstable:
            self.case = 'case1'
        if firm_action == 'relocate' and regulator_action == 'not intervene' and nature_state == self.state_unstable:
            self.case = 'case2'
        if firm_action == 'relocate' and regulator_action == 'intervene' and nature_state == self.state_stable:
            self.case = 'case3'
        if firm_action == 'relocate' and regulator_action == 'not intervene' and nature_state == self.state_stable:
            self.case = 'case4'
        if firm_action == 'not relocate' and regulator_action == 'intervene' and nature_state == self.state_unstable:
            self.case = 'case5'
        if firm_action == 'not relocate' and regulator_action == 'not intervene' and nature_state == self.state_unstable:
            self.case = 'case6'
        if firm_action == 'not relocate' and regulator_action == 'intervene' and nature_state == self.state_stable:
            self.case = 'case7'
        if firm_action == 'not relocate' and regulator_action == 'not intervene' and nature_state == self.state_stable:
            self.case = 'case8'

class StrategicForm:
    def __init__(self, extensive_form):
        self.extensive_form = extensive_form
        self.strategic_form = []
        self.pure_strategies = extensive_form.pure_strategies

    def strategic_form_payoff_function(self):
        ro = sympy.symbols('ro')
        p1_strats = self.pure_strategies[self.extensive_form.player1.name]
        p2_strats = self.pure_strategies[self.extensive_form.player2.name]
        
        # Retrieve nature states dynamically
        nature_states = self.extensive_form.nature.strategies
        # Assume 2 states for now to map to ro and 1-ro
        # state_0 (index 0) corresponds to probability (1-ro) (e.g., stable)
        # state_1 (index 1) corresponds to probability ro (e.g., unstable)
        state_0 = nature_states[0]
        state_1 = nature_states[1]
        
        # Create a lookup for payoffs: (nature, p1, p2) -> payoff
        payoff_lookup = {}
        for s in self.extensive_form.strategies_space:
            key = (s[self.extensive_form.nature.name], s[self.extensive_form.player1.name], s[self.extensive_form.player2.name])
            payoff_lookup[key] = s['payoff']

        matrix = []
        for i, p1_s in enumerate(p1_strats):
            row = []
            for j, p2_s in enumerate(p2_strats):
                # Nature State 0 (prob 1-ro)
                n_0 = state_0
                a1_0 = p1_s[n_0]
                a2_0 = p2_s[a1_0]
                
                payoff_0 = payoff_lookup.get((n_0, a1_0, a2_0))
                
                # Nature State 1 (prob ro)
                n_1 = state_1
                a1_1 = p1_s[n_1]
                a2_1 = p2_s[a1_1]
                
                payoff_1 = payoff_lookup.get((n_1, a1_1, a2_1))
                
                # Payoffs: (P1(state_1), P1(state_0), P2(Expected))
                # Index 0 is P2 (Firm), Index 1 is P1 (Regulator)
                
                p1_payoff_1 = round(payoff_1[1], 2)
                p1_payoff_0 = round(payoff_0[1], 2)
                
                # Round coefficients for p2_expected_payoff
                # Expected = ro * payoff_1 + (1-ro) * payoff_0
                # = ro * payoff_1 + payoff_0 - ro * payoff_0
                # = ro * (payoff_1 - payoff_0) + payoff_0
                
                val_ro_term = payoff_1[0] # Payoff for state 1 (prob ro)
                val_const_term = payoff_0[0] # Payoff for state 0 (prob 1-ro)
                
                val_ro_coeff = round(val_ro_term - val_const_term, 2)
                val_const = round(val_const_term, 2)
                
                if val_ro_coeff == 0:
                    p2_expected_payoff = sympy.Float(val_const, 4)
                else:
                    c_ro = sympy.Float(val_ro_coeff, 4)
                    c_const = sympy.Float(val_const, 4)
                    p2_expected_payoff = c_ro * ro + c_const
                
                row.append(((p1_payoff_1, p1_payoff_0, p2_expected_payoff)))
            matrix.append(row)
        return matrix

    def find_nash_equilibria(self):
        ro = sympy.symbols('ro')
        matrix = self.strategic_form_payoff_function()
        equilibria = []
        
        p1_name = self.extensive_form.player1.name
        p2_name = self.extensive_form.player2.name
        
        p1_strats = self.pure_strategies[p1_name]
        p2_strats = self.pure_strategies[p2_name]
        
        # Matrix dimensions
        num_rows = len(matrix)
        num_cols = len(matrix[0])
        
        for i in range(num_rows):
            for j in range(num_cols):
                # Check if cell (i, j) can be a Nash Equilibrium
                
                conditions = []
                # Constraint: 0 <= ro <= 1
                conditions.append(ro >= 0)
                conditions.append(ro <= 1)
                
                # 1. P1 Condition (Row Player)
                # EU_P1(i, j) >= EU_P1(k, j) for all k != i
                # EU_P1 = ro * p1_state1 + (1-ro) * p1_state0
                # Note: In matrix cell, we stored (p1_payoff_1, p1_payoff_0, p2_expected_payoff)
                # So index 0 is state 1 (ro weight), index 1 is state 0 ((1-ro) weight)
                
                current_cell = matrix[i][j]
                p1_state1_curr = current_cell[0]
                p1_state0_curr = current_cell[1]
                eu_p1_curr = ro * p1_state1_curr + (1-ro) * p1_state0_curr
                
                for k in range(num_rows):
                    if k == i: continue
                    other_cell = matrix[k][j]
                    p1_state1_other = other_cell[0]
                    p1_state0_other = other_cell[1]
                    eu_p1_other = ro * p1_state1_other + (1-ro) * p1_state0_other
                    
                    conditions.append(eu_p1_curr >= eu_p1_other)
                
                # 2. P2 Condition (Column Player)
                # EU_P2(i, j) >= EU_P2(i, k) for all k != j
                # EU_P2 is already symbolic in matrix[i][j][2]
                
                eu_p2_curr = current_cell[2]
                
                for k in range(num_cols):
                    if k == j: continue
                    other_cell = matrix[i][k]
                    eu_p2_other = other_cell[2]
                    
                    conditions.append(eu_p2_curr >= eu_p2_other)
                
                # Solve for ro
                try:
                    # reduce_inequalities works well for systems of inequalities
                    solution = sympy.reduce_inequalities(conditions, ro)
                    
                    # Check if solution is not EmptySet (False)
                    if solution != False:
                        equilibria.append({
                            p1_name: p1_strats[i],
                            p2_name: p2_strats[j],
                            'ro_range': solution
                        })
                except Exception as e:
                    print(f"Error solving for cell ({i},{j}): {e}")
                    
        return equilibria


nature = Player('nature', ('stable', 'unstable'))
player1 = Player('regulator', ('intervene', 'not intervene'))
player2 = Player('trippleB', ('relocate', 'not relocate'))

payoff_data = {
    'p1': {
        'revenue_minus_cost': {'case1':75, 'case2':75, 'case3':75, 'case4':75, 'case5':65.66, 'case6':65.66, 'case7':65.66, 'case8':65.66},
        'carbon_tax': {'case1':0, 'case2':0, 'case3':0, 'case4':0, 'case5':-12, 'case6':-12, 'case7':-12, 'case8':-12},
        'risk': {'case1':-50, 'case2':-5, 'case3':-5, 'case4':0, 'case5':-4, 'case6':-4, 'case7':-4, 'case8':-4}
    },
    'p2': {
        'national_wealth': {'case1':45.42, 'case2':45.42, 'case3':45.42, 'case4':45.42, 'case5':33.93, 'case6':33.93, 'case7':33.93, 'case8':33.93},
        'technology_dependence': {'case1':-1, 'case2':-1, 'case3':-1, 'case4':-1, 'case5':1, 'case6':1, 'case7':1, 'case8':1},
        'reputation': {'case1':-4, 'case2':-3, 'case3':-2, 'case4':-1, 'case5':-4, 'case6':-3, 'case7':-2, 'case8':-1},
        'carbon_tax_p2': {'case1':23, 'case2':23, 'case3':23, 'case4':23, 'case5':0, 'case6':0, 'case7':0, 'case8':0}
    }
}

extensive_form = ExtensiveForm(nature, player1, player2, payoff_data)
pprint.pprint(extensive_form.strategies_space)
pure_strategies = extensive_form.generate_pure_strategies()
pprint.pprint(pure_strategies)

strategic_form = StrategicForm(extensive_form)
pprint.pprint(strategic_form.strategic_form_payoff_function())
pprint.pprint(strategic_form.find_nash_equilibria())

