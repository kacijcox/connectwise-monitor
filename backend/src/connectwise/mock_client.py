# src/connectwise/mock_client.py
from datetime import datetime, timedelta
from typing import List, Dict, Any
import random

class MockConnectWiseClient:
    def __init__(self):
        self.ticket_types = ["Service Request", "Problem", "Incident"]
        self.priorities = ["Low", "Medium", "High"]
        self.common_issues = [
            "Password Reset",
            "Network Connection Issue",
            "Software Installation",
            "Email Problems",
            "Printer Not Working"
        ]

    def generate_mock_ticket(self, date: datetime, member: str) -> Dict[str, Any]:
        """Generate a realistic-looking ticket"""
        ticket_type = random.choice(self.ticket_types)
        issue = random.choice(self.common_issues)
        
        return {
            "id": random.randint(1000, 9999),
            "summary": f"{issue} - {random.randint(100, 999)}",
            "type": {"name": ticket_type},
            "priority": {"name": random.choice(self.priorities)},
            "status": {"name": "New"},
            "dateEntered": date.isoformat(),
            "enteredBy": member,
            "company": {"name": "Test Company"},
            "board": {"name": "Service Board"}
        }

    def get_member_tickets(self, member_identifier: str, days: int = 7) -> List[Dict[str, Any]]:
        """
        Generate a set of test tickets with patterns for testing
        """
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        tickets = []

        # Generate normal random tickets
        for _ in range(random.randint(5, 10)):
            ticket_date = start_date + timedelta(
                days=random.randint(0, days)
            )
            tickets.append(self.generate_mock_ticket(ticket_date, member_identifier))

        # Insert a pattern - multiple similar tickets
        pattern_issue = random.choice(self.common_issues)
        for _ in range(4):  # Create pattern with 4 similar tickets
            ticket_date = start_date + timedelta(
                days=random.randint(0, days)
            )
            ticket = self.generate_mock_ticket(ticket_date, member_identifier)
            ticket["summary"] = f"{pattern_issue} - {random.randint(100, 999)}"
            ticket["type"]["name"] = self.ticket_types[0]  # Same type for pattern
            tickets.append(ticket)

        return tickets

    def test_different_patterns(self, member_identifier: str) -> List[Dict[str, Any]]:
        """
        Generate test data with different types of patterns for testing
        """
        tickets = self.get_member_tickets(member_identifier)
        
        print("\nTest Data Generated:")
        print(f"Total Tickets: {len(tickets)}")
        
        # Count pattern occurrences
        summaries = {}
        types = {}
        for ticket in tickets:
            summary = ticket["summary"].split(" - ")[0]
            summaries[summary] = summaries.get(summary, 0) + 1
            types[ticket["type"]["name"]] = types.get(ticket["type"]["name"], 0) + 1
        
        print("\nPattern Distribution:")
        print("Issue Types:", dict(types))
        print("Common Issues:", dict(summaries))
        
        return tickets