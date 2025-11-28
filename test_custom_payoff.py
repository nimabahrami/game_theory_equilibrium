from tripple_b_gt import Player, ExtensiveForm
import sympy

def test_custom_payoff():
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
        'p2': {
            'Profit': {'case1': 10, 'case2': 10, 'case3': 10, 'case4': 10, 'case5': 5, 'case6': 5, 'case7': 5, 'case8': 5}
        }
    }
    
    # Custom Functions
    p1_func = "Revenue - Cost"
    p2_func = "Profit * 2"
    
    # Initialize Game
    game = ExtensiveForm(nature, p1, p2, payoff_data, p1_func, p2_func)
    
    # Test Payoff for case1
    # P1: 100 - 20 = 80
    # P2: 10 * 2 = 20
    p1_res, p2_res = game.payoff('case1')
    
    print(f"Case 1 Payoff: P1={p1_res}, P2={p2_res}")
    
    assert p1_res == 80
    assert p2_res == 20
    
    # Test Payoff for case5
    # P1: 50 - 10 = 40
    # P2: 5 * 2 = 10
    p1_res, p2_res = game.payoff('case5')
    
    print(f"Case 5 Payoff: P1={p1_res}, P2={p2_res}")
    
    assert p1_res == 40
    assert p2_res == 10
    
    print("Test Passed!")

if __name__ == "__main__":
    test_custom_payoff()
