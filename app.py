from flask import Flask, render_template, request, jsonify, session
import os
from game.scenarios import ScenarioManager
from game.permissions import PermissionValidator
from game.scoring import ScoreManager

app = Flask(__name__)
app.secret_key = 'chmod-hero-secret-key-change-in-production'

# Initialize game components
scenario_manager = ScenarioManager()
permission_validator = PermissionValidator()
score_manager = ScoreManager()

@app.route('/')
def index():
    """Main landing page"""
    return render_template('index.html')

@app.route('/game')
def game():
    """Main game page"""
    # Initialize or reset game session
    if 'current_level' not in session:
        session['current_level'] = 1
        session['score'] = 0
        session['lives'] = 3
    
    # Get current scenario
    scenario = scenario_manager.get_scenario(session['current_level'])
    
    return render_template('game.html', 
                         scenario=scenario,
                         level=session['current_level'],
                         score=session['score'],
                         lives=session['lives'])

@app.route('/submit_command', methods=['POST'])
def submit_command():
    """Process player's chmod command"""
    data = request.get_json()
    command = data.get('command', '').strip()
    level = session.get('current_level', 1)
    
    # Get current scenario
    scenario = scenario_manager.get_scenario(level)
    
    # Validate the command
    result = permission_validator.validate_command(command, scenario)
    
    if result['correct']:
        # Command was correct!
        points = score_manager.calculate_points(level, result['time_taken'])
        session['score'] += points
        session['current_level'] += 1
        
        return jsonify({
            'success': True,
            'message': result['message'],
            'points': points,
            'new_score': session['score'],
            'next_level': session['current_level']
        })
    else:
        # Command was wrong
        session['lives'] -= 1
        
        if session['lives'] <= 0:
            # Game over
            final_score = session['score']
            session.clear()  # Reset game
            return jsonify({
                'success': False,
                'game_over': True,
                'message': result['message'],
                'final_score': final_score
            })
        else:
            return jsonify({
                'success': False,
                'message': result['message'],
                'lives_remaining': session['lives'],
                'hint': result.get('hint', '')
            })

@app.route('/leaderboard')
def leaderboard():
    """Show high scores"""
    scores = score_manager.get_top_scores()
    return render_template('leaderboard.html', scores=scores)

@app.route('/reset_game', methods=['POST'])
def reset_game():
    """Reset the current game"""
    session.clear()
    return jsonify({'success': True})

@app.route('/help')
def help_page():
    """Help and tutorial page"""
    return render_template('help.html')

@app.route('/tutorial')
def tutorial():
    """Interactive tutorial page"""
    return render_template('tutorial.html')

@app.route('/api/scenario/<int:level>')
def get_scenario(level):
    """API endpoint to get scenario data"""
    scenario = scenario_manager.get_scenario(level)
    return jsonify(scenario)

@app.route('/api/calculate_permission', methods=['POST'])
def calculate_permission():
    """API endpoint for permission calculator"""
    data = request.get_json()
    octal = data.get('octal', '644')
    
    try:
        # Convert octal to binary representation
        permissions = []
        for digit in octal:
            d = int(digit)
            permissions.append({
                'read': bool(d & 4),
                'write': bool(d & 2),
                'execute': bool(d & 1)
            })
        
        # Generate symbolic representation
        symbolic = ''
        for perm in permissions:
            symbolic += 'r' if perm['read'] else '-'
            symbolic += 'w' if perm['write'] else '-'
            symbolic += 'x' if perm['execute'] else '-'
        
        return jsonify({
            'success': True,
            'octal': octal,
            'symbolic': symbolic,
            'permissions': {
                'owner': permissions[0] if len(permissions) > 0 else {'read': False, 'write': False, 'execute': False},
                'group': permissions[1] if len(permissions) > 1 else {'read': False, 'write': False, 'execute': False},
                'others': permissions[2] if len(permissions) > 2 else {'read': False, 'write': False, 'execute': False}
            }
        })
    except (ValueError, IndexError):
        return jsonify({
            'success': False,
            'error': 'Invalid octal format'
        })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5089)