from flask import Flask, render_template, request, jsonify
from tripple_b_gt import Player, ExtensiveForm, StrategicForm
import sympy

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.json
    
    # Extract data from JSON
    p1_name = data.get('p1_name', 'Player 1')
    p2_name = data.get('p2_name', 'Player 2')
    
    nature_strategies = data.get('nature_strategies', ['stable', 'unstable'])
    p1_strategies = data.get('p1_strategies', ['intervene', 'not intervene'])
    p2_strategies = data.get('p2_strategies', ['relocate', 'not relocate'])
    
    # Payoff data structure from frontend:
    # {
    #   'p1': {'var_name': {'case1': val, ...}, ...},
    #   'p2': {'var_name': {'case1': val, ...}, ...}
    # }
    payoff_data = data.get('payoff_data', {})
    
    # Nature states
    nature = Player('nature', tuple(nature_strategies))
    
    # Players
    player1 = Player(p1_name, tuple(p1_strategies))
    player2 = Player(p2_name, tuple(p2_strategies))
    
    # Create Game
    try:
        extensive_form = ExtensiveForm(nature, player1, player2, payoff_data)
        strategic_game = StrategicForm(extensive_form)
        equilibria = strategic_game.find_nash_equilibria()
        
        # Format results for frontend
        results = []
        for eq in equilibria:
            # Convert sympy object to string for JSON serialization
            ro_range_str = str(eq['ro_range'])
            
            results.append({
                'p1_strategy': eq[p1_name],
                'p2_strategy': eq[p2_name],
                'ro_range': ro_range_str
            })
            
        # Also get the payoff matrix to display?
        # matrix = strategic_game.strategic_form_payoff_function()
        # We might want to display it, but let's start with equilibria.
        
        return jsonify({'status': 'success', 'equilibria': results})
        
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
