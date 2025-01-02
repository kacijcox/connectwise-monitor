# Add to your existing tests/test_analyzer.py
import unittest
from src.connectwise.mock_client import MockConnectWiseClient
from src.monitoring.analyzer import TicketAnalyzer

class TestTicketAnalyzer(unittest.TestCase):
    def setUp(self):
        self.mock_client = MockConnectWiseClient()
        self.analyzer = TicketAnalyzer(self.mock_client)

    def test_pattern_detection(self):
        # Test for a single member
        member = "sarah.smith"
        patterns = self.analyzer.analyze_member_tickets(member)
        
        # Assert that patterns are being detected
        self.assertIsNotNone(patterns)
        self.assertIsInstance(patterns, list)
        
        # If patterns are found, verify their structure
        if patterns:
            for pattern in patterns:
                self.assertIn('pattern_type', pattern)
                self.assertIn('pattern_value', pattern)
                self.assertIn('ticket_count', pattern)
                self.assertIn('tickets', pattern)

if __name__ == '__main__':
    unittest.main()