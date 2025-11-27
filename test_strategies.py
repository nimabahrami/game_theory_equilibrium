from tripple_b_gt import extensive_form

def test_strategies_space():
    # Initialize with dummy values
    game = extensive_form(0.5, 10, 5, "P1", "P2", "Nature")
    
    strategies = game.strategies_space()
    
    print(f"Total strategies: {len(strategies)}")
    for i, s in enumerate(strategies):
        print(f"{i+1}: {s}")
        
    assert len(strategies) == 8, f"Expected 8 strategies, got {len(strategies)}"
    
    # Check expected content
    # Nature: ('stable', 'unstable')
    # P1: ('intervene', 'not intervene')
    # P2: ('relocate', 'not relocate')
    
    expected_first = ('stable', 'intervene', 'relocate')
    assert strategies[0] == expected_first, f"Expected first strategy {expected_first}, got {strategies[0]}"
    
    print("Verification successful!")

def get_payoff_data():
    return {
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

def test_pure_strategies():
    from tripple_b_gt import Player, ExtensiveForm
    nature = Player('nature', ('stable', 'unstable'))
    player1 = Player('regulator', ('intervene', 'not intervene'))
    player2 = Player('firm', ('relocate', 'not relocate'))
    
    # Pass payoff data even if not strictly needed for pure strategies generation
    game = ExtensiveForm(nature, player1, player2, get_payoff_data())
    pure_strategies = game.generate_pure_strategies()
    
    print("\nTesting Pure Strategies Generation:")
    
    # Check Regulator strategies
    regulator_strats = pure_strategies['regulator']
    print(f"Regulator strategies count: {len(regulator_strats)}")
    assert len(regulator_strats) == 4
    # Example check: one strategy should be stable->intervene, unstable->intervene
    expected_p1 = {'stable': 'intervene', 'unstable': 'intervene'}
    assert expected_p1 in regulator_strats
    
    # Check Firm strategies
    firm_strats = pure_strategies['firm']
    print(f"Firm strategies count: {len(firm_strats)}")
    assert len(firm_strats) == 4
    # Example check: one strategy should be intervene->relocate, not intervene->relocate
    expected_p2 = {'intervene': 'relocate', 'not intervene': 'relocate'}
    assert expected_p2 in firm_strats
    
    print("Pure strategies verification successful!")

def test_payoff_matrix():
    from tripple_b_gt import Player, ExtensiveForm, StrategicForm
    import pprint
    
    nature = Player('nature', ('stable', 'unstable'))
    player1 = Player('regulator', ('intervene', 'not intervene'))
    player2 = Player('firm', ('relocate', 'not relocate'))
    
    game = ExtensiveForm(nature, player1, player2, get_payoff_data())
    pure_strategies = game.generate_pure_strategies()
    
    strategic_game = StrategicForm(game)
    matrix = strategic_game.strategic_form_payoff_function()
    
    print("\nTesting Payoff Matrix:")
    print("Matrix dimensions: {}x{}".format(len(matrix), len(matrix[0])))
    assert len(matrix) == 4
    assert len(matrix[0]) == 4
    
    print("Payoff Matrix Sample (0,0):")
    print(matrix[0][0])
    
    # Check that values are tuples of length 3
    assert isinstance(matrix[0][0], tuple)
    assert len(matrix[0][0]) == 3, f"Expected tuple length 3, got {len(matrix[0][0])}"
    
    # Check for sympy object in the 3rd element
    import sympy
    assert isinstance(matrix[0][0][2], (sympy.Basic, sympy.Expr, float, int)), "Expected sympy expression or number"
    
    print("Payoff matrix verification successful!")

def test_nash_equilibria():
    from tripple_b_gt import Player, ExtensiveForm, StrategicForm
    import pprint
    
    nature = Player('nature', ('StateA', 'StateB'))
    player1 = Player('regulator', ('intervene', 'not intervene'))
    player2 = Player('firm', ('relocate', 'not relocate'))
    
    # Need to update payoff data keys to match generic nature states if CaseBuilder uses them?
    # CaseBuilder maps nature states to 'case1', 'case2', etc. based on logic.
    # The payoff data is keyed by 'case1', 'case2'.
    # So as long as CaseBuilder correctly identifies the case, the payoff lookup works.
    # CaseBuilder uses self.state_stable/unstable.
    
    game = ExtensiveForm(nature, player1, player2, get_payoff_data())
    pure_strategies = game.generate_pure_strategies()
    
    strategic_game = StrategicForm(game)
    equilibria = strategic_game.find_nash_equilibria()
    
    print("\nTesting Nash Equilibria:")
    print(f"Found {len(equilibria)} potential equilibria.")
    
    p1_name = strategic_game.extensive_form.player1.name
    p2_name = strategic_game.extensive_form.player2.name
    
    for eq in equilibria:
        print(f"{p1_name} Strategy: {eq[p1_name]}")
        print(f"{p2_name} Strategy: {eq[p2_name]}")
        print(f"Valid ro range: {eq['ro_range']}")
        print("-" * 20)
        
    assert len(equilibria) > 0, "Expected at least one equilibrium"
    print("Nash Equilibria verification successful!")

if __name__ == "__main__":
    # test_strategies_space() 
    test_pure_strategies()
    test_payoff_matrix()
    test_nash_equilibria()
