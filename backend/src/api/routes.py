# backend/src/api/routes.py
from flask import Flask, jsonify
from flask_cors import CORS
from ..connectwise.client import ConnectWiseClient
from ..monitoring.analyzer import TicketAnalyzer

# Create the Flask application instance
app = Flask(__name__)
CORS(app)

# Initialize clients
cw_client = ConnectWiseClient()
analyzer = TicketAnalyzer(cw_client)

@app.route('/')
def home():
    return jsonify({"message": "ConnectWise Monitor API"})

@app.route('/api/patterns', methods=['GET'])
def get_patterns():
    try:
        patterns = analyzer.analyze_tickets()
        return jsonify(patterns)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/stats', methods=['GET'])
def get_stats():
    try:
        tickets = cw_client.get_all_tickets()
        
        # Calculate basic stats
        stats = {
            'total_tickets': len(tickets),
            'time_period': '7 Days',
            'active_users': len(set(t.get('assignedTo', {}).get('name') for t in tickets if t.get('assignedTo'))),
            'departments': len(set(t.get('team', {}).get('name') for t in tickets if t.get('team')))
        }
        
        return jsonify(stats)
    except Exception as e:
        return jsonify({'error': str(e)}), 500