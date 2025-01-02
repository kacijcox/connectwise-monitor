# backend/src/monitoring/analyzer.py
from .claude_analyzer import ClaudeAnalyzer
from datetime import datetime, timedelta

class TicketAnalyzer:
    def __init__(self, cw_client):
        self.cw_client = cw_client
        self.claude = ClaudeAnalyzer()

    def analyze_tickets(self):
        """
        Analyze tickets for user-specific patterns
        """
        # Get recent tickets (last 3 days)
        end_date = datetime.now()
        start_date = end_date - timedelta(days=3)
        tickets = self.cw_client.get_tickets(start_date, end_date)

        # Use Claude to analyze user patterns
        patterns = self.claude.analyze_user_patterns(tickets)

        # Format results for the frontend
        formatted_patterns = []
        for pattern in patterns:
            if pattern and 'analysis' in pattern:
                formatted_patterns.append({
                    'user': pattern['user'],
                    'ticket_count': pattern['ticket_count'],
                    'time_period': pattern['time_period'],
                    'pattern_details': pattern['analysis'],
                    'detected_at': pattern['analyzed_at']
                })

        return formatted_patterns