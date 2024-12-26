# src/monitoring/analyzer.py
from collections import defaultdict
from typing import List, Dict, Any, Tuple
from datetime import datetime
from ..connectwise.client import ConnectWiseClient
from ..config import settings

class TicketAnalyzer:
    def __init__(self, cw_client: ConnectWiseClient):
        self.cw_client = cw_client
        self.threshold = settings.ALERT_THRESHOLD
        self.timeframe_days = settings.ALERT_TIMEFRAME_DAYS

    def analyze_member_tickets(self, member_identifier: str) -> List[Dict[str, Any]]:
        """
        Analyze tickets submitted by a specific member to identify patterns
        """
        tickets = self.cw_client.get_member_tickets(
            member_identifier, 
            days=self.timeframe_days
        )
        
        patterns = self._identify_patterns(tickets)
        return self._filter_significant_patterns(patterns)

    def _identify_patterns(self, tickets: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
        """
        Group tickets by common characteristics to identify patterns
        """
        patterns = defaultdict(list)
        
        for ticket in tickets:
            # Group by summary/title similarities
            summary_key = self._normalize_summary(ticket.get('summary', ''))
            patterns[f"summary:{summary_key}"].append(ticket)
            
            # Group by type
            ticket_type = ticket.get('type', {}).get('name', 'Unknown')
            patterns[f"type:{ticket_type}"].append(ticket)
            
            # Group by priority
            priority = ticket.get('priority', {}).get('name', 'Unknown')
            patterns[f"priority:{priority}"].append(ticket)
        
        return patterns

    def _normalize_summary(self, summary: str) -> str:
        """
        Normalize ticket summaries to group similar issues
        Basic implementation - can be enhanced with NLP
        """
        return summary.lower().strip()

    def _filter_significant_patterns(self, patterns: Dict[str, List[Dict[str, Any]]]) -> List[Dict[str, Any]]:
        """
        Filter patterns that meet the threshold for alerting
        """
        significant_patterns = []
        
        for pattern_key, tickets in patterns.items():
            if len(tickets) >= self.threshold:
                pattern_type, pattern_value = pattern_key.split(':', 1)
                significant_patterns.append({
                    'pattern_type': pattern_type,
                    'pattern_value': pattern_value,
                    'ticket_count': len(tickets),
                    'tickets': tickets,
                    'first_occurrence': min(t.get('dateEntered', '') for t in tickets),
                    'last_occurrence': max(t.get('dateEntered', '') for t in tickets)
                })
        
        return significant_patterns