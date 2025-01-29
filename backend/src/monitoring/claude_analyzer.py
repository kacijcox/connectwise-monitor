from anthropic import Anthropic
from typing import List, Dict, Any
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib

class ClaudeAnalyzer:
    def __init__(self):
        # Load environment variables
        load_dotenv()

        # Get API key
        api_key = os.getenv('ANTHROPIC_API_KEY')
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY not found in environment variables")

        self.client = Anthropic(api_key=api_key)

    def analyze_user_patterns(self, tickets: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Analyze tickets to identify user-specific patterns
        """
        user_tickets = self._group_by_user(tickets)
        patterns = []

        for user, user_tickets in user_tickets.items():
            # Only analyze if user has submitted multiple tickets in past 3 days
            recent_tickets = [t for t in user_tickets
                              if (datetime.now() - datetime.fromisoformat(t['dateEntered'])).days <= 3]

            if len(recent_tickets) >= 2:
                pattern = self._analyze_user_tickets(user, recent_tickets)
                if pattern:
                    patterns.append(pattern)

        return patterns

    def _analyze_user_tickets(self, user: str, tickets: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Analyze a specific user's tickets for patterns
        """
        ticket_summaries = [
            f"Ticket {t['id']}: {t['summary']} (Created: {t['dateEntered']})"
            for t in tickets
        ]

        prompt = f"""Analyze these support tickets submitted by user {user} in the past 3 days:

        Tickets: {ticket_summaries}

        Focus specifically on identifying:
        1. If the user is submitting multiple tickets about the same or similar issues
        2. The specific type of recurring problem (e.g., "Outlook login", "printer connection") 
        3. Whether this might indicate a deeper underlying issue the user is facing

        Respond in JSON format with these keys:
        - has_pattern (boolean)
        - issue_type (string, the main type of recurring issue)
        - ticket_count (number of related tickets)
        - significance (high/medium/low, based on frequency and impact)
        - user_impact (brief description of how this affects the user)"""

        try:
            response = self.client.messages.create(
                model="claude-3-sonnet-20240229",
                max_tokens=300,
                messages=[{"role": "user", "content": prompt}]
            )
            analysis = response.content

            # Check if the pattern is significant
            if 'high' in analysis.lower() or 'medium' in analysis.lower():
                pattern = {
                    'user': user,
                    'ticket_count': len(tickets),
                    'time_period': '3 days',
                    'issue_type': analysis.get('issue_type', ''),
                    'significance': analysis.get('significance', ''),
                    'user_impact': analysis.get('user_impact', '')
                }
                self.send_pattern_email(user, pattern)

            return {
                'user': user,
                'ticket_count': len(tickets),
                'time_period': '3 days',
                'analysis': analysis,
                'analyzed_at': datetime.now().isoformat()
            }
        except Exception as e:
            print(f"Error analyzing tickets for user {user}: {str(e)}")
            return None

    def send_pattern_email(self, user: str, pattern: Dict[str, Any]):
        # Load email settings from environment variables
        smtp_server = os.getenv('SMTP_SERVER')
        smtp_port = int(os.getenv('SMTP_PORT'))
        sender_email = os.getenv('SENDER_EMAIL')
        sender_password = os.getenv('SENDER_PASSWORD')
        recipient_email = os.getenv('RECIPIENT_EMAIL')

        # Create email message
        message = MIMEMultipart()
        message['From'] = sender_email
        message['To'] = recipient_email
        message['Subject'] = f"Significant Pattern Detected for User {user}"

        body = f"""
        A significant pattern has been detected for user {user}:

        Issue Type: {pattern['issue_type']}
        Ticket Count: {pattern['ticket_count']}
        Significance: {pattern['significance']}
        User Impact: {pattern['user_impact']}
        """
        message.attach(MIMEText(body, 'plain'))

        # Send email
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(message)

    def _group_by_user(self, tickets: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
        """Group tickets by user"""
        grouped = {}
        for ticket in tickets:
            user = ticket.get('contact', {}).get('name', 'Unknown')
            if user not in grouped:
                grouped[user] = []
            grouped[user].append(ticket)
        return grouped