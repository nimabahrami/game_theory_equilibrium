from tripple_b_gt import Player, ExtensiveForm


def test_robust_payoff():
    # Setup
    nature = Player('nature', ('stable', 'unstable'))
    p1 = Player('p1', ('A', 'B'))
    p2 = Player('p2', ('X', 'Y'))
    
    # Payoff Data
    payoff_data = {
        'p1': {
            'Revenue': {'case1': 100, 'case2': 100, 'case3': 100, 'case4': 100, 'case5': 50, 'case6': 50, 'case7': 50, 'case8': 50},
            'Cost': {'case1': 20, 'case2': 20, 'case3': 20, 'case4': 20, 'case5': 10, 'case6': 10, 'case7': 10, 'case8': 10}
        },
        'p2': {}
    }
    
    # Test 1: Undefined Variable
    p1_func_bad = "Revenue - UndefinedVar"
    
    try:
        game_bad = ExtensiveForm(nature, p1, p2, payoff_data, p1_func_bad, None)
        game_bad.payoff('case1')
        print("Test 1 Failed: Should have raised ValueError")
    except ValueError as e:
        print(f"Test 1 Passed: Caught expected error: {e}")
        assert "Undefined variables" in str(e)
        assert "UndefinedVar" in str(e)
        
    # Test 2: Whitespace Handling
    p1_func_space = "  Revenue - Cost  "
    game_space = ExtensiveForm(nature, p1, p2, payoff_data, p1_func_space, None)
    
    try:
        res, _ = game_space.payoff('case1')
        print(f"Test 2 Passed: Result {res} (Expected 80)")
        assert res == 80
    except Exception as e:
        print(f"Test 2 Failed: Unexpected error: {e}")

if __name__ == "__main__":
    test_robust_payoff()
