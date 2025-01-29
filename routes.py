from flask import Flask, jsonify
from flask_cors import CORS
from backend.src.connectwise.client import ConnectWiseClient
from backend.src.monitoring.analyzer import TicketAnalyzer
from datetime import datetime, timedelta

app = Flask(__name__)
CORS(app)

cw_client = ConnectWiseClient()
analyzer = TicketAnalyzer(cw_client)

@app.route('/')
def home():
    return jsonify({"message": "ConnectWise Monitor API"})

@app.route('/api/patterns/user', methods=['GET'])
def get_user_patterns():
    try:
        patterns = analyzer.analyze_tickets()
        return jsonify({
            'timestamp': datetime.now().isoformat(),
            'patterns': patterns
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/patterns/live', methods=['GET'])
def get_live_patterns():
    """Get patterns from the last hour for immediate analysis"""
    try:
        end_date = datetime.now()
        start_date = end_date - timedelta(hours=1)
        tickets = cw_client.get_tickets(start_date, end_date)
        patterns = analyzer.analyze_tickets()
        return jsonify({
            'timestamp': datetime.now().isoformat(),
            'ticket_count': len(tickets),
            'patterns': patterns
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/test-email', methods=['GET'])
def test_email():
    try:
        # Create a dummy pattern for testing
        dummy_pattern = {
            'user': 'Test User',
            'ticket_count': 3,
            'time_period': '3 days',
            'issue_type': 'Test Issue',
            'significance': 'high',
            'user_impact': 'This is a test pattern for email functionality.'
        }
        
        # Send the test email
        analyzer.claude.send_pattern_email('Test User', dummy_pattern)
        
        return jsonify({'message': 'Test email sent successfully.'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)