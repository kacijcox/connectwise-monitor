# src/monitoring/analyzer.py
from collections import defaultdict
from typing import List, Dict, Any, Tuple
from datetime import datetime, timedelta
from ..connectwise.client import ConnectWiseClient
from ..config import settings

class TicketAnalyzer:
    def __init__(self, cw_client: ConnectWiseClient):
        self.cw_client = cw_client
        self.user_threshold = 2  # Number of similar tickets from same user
        self.company_network_threshold = 3  # Number of network issues from same company
        self.timeframe_days = 3  # Rolling 3-day window

    def analyze_tickets(self) -> Dict[str, List[Dict[str, Any]]]:
        """
        Analyze tickets for two specific pattern types:
        1. Company-wide network issues
        2. Repeated user issues
        """
        tickets = self.cw_client.get_all_tickets(days=self.timeframe_days)
        
        return {
            'company_network_patterns': self._analyze_company_network_issues(tickets),
            'user_repeat_patterns': self._analyze_user_repeat_issues(tickets)
        }

    def _analyze_company_network_issues(self, tickets: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Detect network-related issues occurring multiple times within the same company
        """
        # Group by company
        company_tickets = defaultdict(list)
        network_keywords = ['network', 'connection', 'internet', 'wifi', 'ethernet', 'connectivity']
        
        for ticket in tickets:
            company = ticket.get('company', {}).get('name')
            if not company:
                continue
                
            # Check if ticket is network-related
            summary = ticket.get('summary', '').lower()
            description = ticket.get('description', '').lower()
            
            if any(keyword in summary or keyword in description for keyword in network_keywords):
                company_tickets[company].append(ticket)

        # Identify patterns
        patterns = []
        for company, company_network_tickets in company_tickets.items():
            if len(company_network_tickets) >= self.company_network_threshold:
                # Calculate time clustering
                dates = [datetime.fromisoformat(t['dateEntered']) for t in company_network_tickets]
                clusters = self._identify_time_clusters(dates)
                
                if any(len(cluster) >= self.company_network_threshold for cluster in clusters):
                    patterns.append({
                        'type': 'company_network',
                        'company': company,
                        'ticket_count': len(company_network_tickets),
                        'tickets': company_network_tickets,
                        'first_occurrence': min(t['dateEntered'] for t in company_network_tickets),
                        'last_occurrence': max(t['dateEntered'] for t in company_network_tickets),
                        'alert_level': 'high' if len(company_network_tickets) >= 5 else 'medium'
                    })

        return patterns

    def _analyze_user_repeat_issues(self, tickets: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Detect when the same user reports similar issues multiple times
        """
        # Group tickets by user
        user_tickets = defaultdict(list)
        for ticket in tickets:
            contact = ticket.get('contact', {}).get('name')
            if contact:
                user_tickets[contact].append(ticket)

        # Analyze each user's tickets for patterns
        patterns = []
        for user, user_ticket_list in user_tickets.items():
            if len(user_ticket_list) >= self.user_threshold:
                # Group by similar issues
                issue_groups = self._group_similar_issues(user_ticket_list)
                
                for issue_type, issue_tickets in issue_groups.items():
                    if len(issue_tickets) >= self.user_threshold:
                        patterns.append({
                            'type': 'user_repeat',
                            'user': user,
                            'issue_type': issue_type,
                            'ticket_count': len(issue_tickets),
                            'tickets': issue_tickets,
                            'first_occurrence': min(t['dateEntered'] for t in issue_tickets),
                            'last_occurrence': max(t['dateEntered'] for t in issue_tickets),
                            'alert_level': 'high' if len(issue_tickets) >= 3 else 'medium'
                        })

        return patterns

    def _group_similar_issues(self, tickets: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
        """
        Group tickets by similar issues using keyword matching
        """
        issue_groups = defaultdict(list)
        
        # Define common issue types and their keywords
        issue_types = {
            'outlook': ['outlook', 'email', 'mail'],
            'password': ['password', 'login', 'credentials'],
            'printer': ['print', 'printer', 'scanning'],
            'software': ['software', 'application', 'program', 'install'],
            'hardware': ['hardware', 'computer', 'device', 'monitor'],
            'access': ['access', 'permission', 'authorize'],
        }

        for ticket in tickets:
            summary = ticket.get('summary', '').lower()
            description = ticket.get('description', '').lower()
            text = f"{summary} {description}"
            
            # Match ticket to issue type
            matched = False
            for issue_type, keywords in issue_types.items():
                if any(keyword in text for keyword in keywords):
                    issue_groups[issue_type].append(ticket)
                    matched = True
                    break
            
            if not matched:
                issue_groups['other'].append(ticket)

        return issue_groups

    def _identify_time_clusters(self, dates: List[datetime], hours_threshold: int = 24) -> List[List[datetime]]:
        """
        Identify clusters of tickets that were created close together in time
        """
        if not dates:
            return []
            
        dates = sorted(dates)
        clusters = [[dates[0]]]
        
        for date in dates[1:]:
            if (date - clusters[-1][-1]).total_seconds() <= hours_threshold * 3600:
                clusters[-1].append(date)
            else:
                clusters.append([date])
                
        return clusters