from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
from ..connectwise.client import ConnectWiseClient
from ..monitoring.analyzer import TicketAnalyzer
from datetime import datetime, timedelta

app = Flask(__name__)
CORS(app)

cw_client = ConnectWiseClient()
analyzer = TicketAnalyzer(cw_client)

# Changed: Removed old home route and added new root route that serves index.html
@app.route('/', defaults={'path': 'index.html'})
@app.route('/<path:path>')
def serve_static(path):
   try:
       return send_from_directory('static', path)
   except:
       return send_from_directory('static', 'index.html')

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

if __name__ == '__main__':
   app.run(debug=True)