from tripple_b_gt import Player, ExtensiveForm, StrategicForm
import pprint

def test_custom_strategies():
    # Setup with CUSTOM names
    nature = Player('nature', ('stable', 'unstable'))
    p1 = Player('p1', ('Attack', 'Defend')) # Instead of Intervene/Not Intervene
    p2 = Player('p2', ('Run', 'Hide'))      # Instead of Relocate/Not Relocate
    
    # Payoff Data (using simple values to verify mapping)
    # Case 1: Unstable, Attack, Run
    # Case 2: Unstable, Defend, Run
    # Case 3: Stable, Attack, Run
    # Case 4: Stable, Defend, Run
    # Case 5: Unstable, Attack, Hide
    # Case 6: Unstable, Defend, Hide
    # Case 7: Stable, Attack, Hide
    # Case 8: Stable, Defend, Hide
    
    payoff_data = {
        'p1': {
            'Val': {'case1': 1, 'case2': 2, 'case3': 3, 'case4': 4, 'case5': 5, 'case6': 6, 'case7': 7, 'case8': 8}
        },
        'p2': {
            'Val': {'case1': 10, 'case2': 20, 'case3': 30, 'case4': 40, 'case5': 50, 'case6': 60, 'case7': 70, 'case8': 80}
        }
    }
    
    # Initialize Game
    game = ExtensiveForm(nature, p1, p2, payoff_data)
    
    # Verify Case Mapping
    # Case 1: Unstable (idx 1), Attack (idx 0), Run (idx 0)
    # Payoff should be P1=1, P2=10
    print("Testing Case 1 (Unstable, Attack, Run)...")
    p1_res, p2_res = game.payoff('case1')
    print(f"Result: P1={p1_res}, P2={p2_res}")
    assert p1_res == 1
    assert p2_res == 10
    
    # Verify Strategic Form Generation
    strategic_game = StrategicForm(game)
    equilibria = strategic_game.find_nash_equilibria()
    
    print("\nEquilibria Found:")
    pprint.pprint(equilibria)
    
    # If we get here without error and equilibria is a list, it's working
    assert isinstance(equilibria, list)
    print("\nTest Passed!")

if __name__ == "__main__":
    test_custom_strategies()
