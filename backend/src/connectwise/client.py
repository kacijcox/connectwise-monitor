# src/connectwise/client.py
import requests
from datetime import datetime, timedelta
from typing import List, Dict, Any
from ..config import settings
import base64

class ConnectWiseClient:
    def __init__(self):
        self.base_url = settings.CW_BASE_URL
        self.company_id = settings.CW_COMPANY_ID
        self.client_id = settings.CW_CLIENT_ID
        self.headers = self._build_headers()

    def _build_headers(self) -> Dict[str, str]:
        # Create authorization header
        credentials = f"{settings.CW_COMPANY_ID}+{settings.CW_PUBLIC_KEY}:{settings.CW_PRIVATE_KEY}"
        encoded_credentials = base64.b64encode(credentials.encode()).decode()
        
        return {
            'Authorization': f'Basic {encoded_credentials}',
            'clientId': settings.CW_CLIENT_ID,
            'Content-Type': 'application/json'
        }

    def get_tickets(self, start_date: datetime, end_date: datetime) -> List[Dict[str, Any]]:
        """
        Retrieve tickets within the specified date range
        """
        endpoint = f"{self.base_url}/service/tickets"
        
        # Format dates for ConnectWise API
        conditions = [
            f"dateEntered >= [{start_date.strftime('%Y-%m-%d')}]",
            f"dateEntered <= [{end_date.strftime('%Y-%m-%d')}]"
        ]
        
        params = {
            'conditions': ' AND '.join(conditions),
            'pageSize': 1000  # Adjust based on your needs
        }
        
        response = requests.get(endpoint, headers=self.headers, params=params)
        response.raise_for_status()
        
        return response.json()

    def get_ticket_details(self, ticket_id: int) -> Dict[str, Any]:
        """
        Get detailed information about a specific ticket
        """
        endpoint = f"{self.base_url}/service/tickets/{ticket_id}"
        response = requests.get(endpoint, headers=self.headers)
        response.raise_for_status()
        
        return response.json()

    def get_member_tickets(self, member_identifier: str, days: int = 30) -> List[Dict[str, Any]]:
        """
        Get tickets created by a specific member within the last X days
        """
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        tickets = self.get_tickets(start_date, end_date)
        return [t for t in tickets if t.get('enteredBy') == member_identifier]