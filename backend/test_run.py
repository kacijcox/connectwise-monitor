# test_run.py
from src.connectwise.mock_client import MockConnectWiseClient
from src.monitoring.analyzer import TicketAnalyzer
from src.monitoring.alerts import AlertManager

def run_test():
    print("Starting ConnectWise Monitor Test Run")
    print("-" * 50)
    
    # Initialize components
    mock_client = MockConnectWiseClient()
    analyzer = TicketAnalyzer(mock_client)
    alert_manager = AlertManager()
    
    # Test members
    test_members = [
        {"identifier": "sarah.smith", "name": "Sarah Smith"},
        {"identifier": "john.doe", "name": "John Doe"}
    ]
    
    for member in test_members:
        print(f"\nAnalyzing tickets for {member['name']}")
        print("-" * 30)
        
        # Get and analyze tickets
        patterns = analyzer.analyze_member_tickets(member['identifier'])
        
        if patterns:
            print(f"Found {len(patterns)} patterns:")
            for pattern in patterns:
                print(f"\nPattern Type: {pattern['pattern_type']}")
                print(f"Pattern Value: {pattern['pattern_value']}")
                print(f"Ticket Count: {pattern['ticket_count']}")
                print("\nAffected Tickets:")
                for ticket in pattern['tickets']:
                    print(f"- {ticket['summary']} (ID: {ticket['id']})")
        else:
            print("No significant patterns found")

if __name__ == "__main__":
    run_test()