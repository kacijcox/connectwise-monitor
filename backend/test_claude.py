# backend/test_claude.py
from src.monitoring.claude_analyzer import ClaudeAnalyzer
from datetime import datetime, timedelta

def test_claude_analysis():
    # Create some mock tickets for testing
    mock_tickets = [
        {
            'id': '1001',
            'summary': 'Outlook keeps asking for password',
            'dateEntered': (datetime.now() - timedelta(hours=2)).isoformat(),
            'contact': {'name': 'John Smith'}
        },
        {
            'id': '1002',
            'summary': 'Cannot log into Outlook',
            'dateEntered': (datetime.now() - timedelta(hours=4)).isoformat(),
            'contact': {'name': 'John Smith'}
        },
        {
            'id': '1003',
            'summary': 'Outlook authentication issues',
            'dateEntered': (datetime.now() - timedelta(hours=6)).isoformat(),
            'contact': {'name': 'John Smith'}
        },
        {
            'id': '1004',
            'summary': 'Printer not working',
            'dateEntered': (datetime.now() - timedelta(hours=3)).isoformat(),
            'contact': {'name': 'Jane Doe'}
        }
    ]

    # Initialize Claude analyzer
    claude = ClaudeAnalyzer()

    print("Testing Claude Pattern Analysis...")
    print("-" * 50)

    # Analyze patterns
    patterns = claude.analyze_user_patterns(mock_tickets)

    # Display results
    for pattern in patterns:
        print(f"\nUser: {pattern['user']}")
        print(f"Ticket Count: {pattern['ticket_count']}")
        print(f"Analysis Time: {pattern['analyzed_at']}")
        print("\nClaude's Analysis:")
        print(pattern['analysis'])
        print("-" * 50)

if __name__ == "__main__":
    test_claude_analysis()