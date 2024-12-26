# src/monitoring/alerts.py
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import List, Dict, Any
from datetime import datetime
from ..config import settings

class AlertManager:
    def __init__(self):
        self.smtp_server = settings.SMTP_SERVER
        self.smtp_port = settings.SMTP_PORT
        self.smtp_username = settings.SMTP_USERNAME
        self.smtp_password = settings.SMTP_PASSWORD
        self.notification_email = settings.NOTIFICATION_EMAIL

    def generate_alert(self, member_name: str, patterns: List[Dict[str, Any]]) -> None:
        """
        Generate and send alert for identified patterns
        """
        if not patterns:
            return

        message = self._create_alert_message(member_name, patterns)
        self._send_email(message)

    def _create_alert_message(self, member_name: str, patterns: List[Dict[str, Any]]) -> str:
        """
        Create formatted alert message from patterns
        """
        message = f"Alert: Ticket Pattern Detected for {member_name}\n\n"
        
        for pattern in patterns:
            message += f"Pattern Type: {pattern['pattern_type']}\n"
            message += f"Pattern Value: {pattern['pattern_value']}\n"
            message += f"Ticket Count: {pattern['ticket_count']}\n"
            message += f"Date Range: {pattern['first_occurrence']} to {pattern['last_occurrence']}\n"
            
            message += "\nAffected Tickets:\n"
            for ticket in pattern['tickets']:
                message += f"- Ticket #{ticket.get('id')}: {ticket.get('summary')}\n"
            
            message += "\n" + "-"*50 + "\n"
        
        return message

    def _send_email(self, message: str) -> None:
        """
        Send email alert
        """
        msg = MIMEMultipart()
        msg['From'] = self.smtp_username
        msg['To'] = self.notification_email
        msg['Subject'] = "ConnectWise Ticket Pattern Alert"
        
        msg.attach(MIMEText(message, 'plain'))
        
        try:
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.smtp_username, self.smtp_password)
                server.send_message(msg)
        except Exception as e:
            print(f"Failed to send email alert: {str(e)}")