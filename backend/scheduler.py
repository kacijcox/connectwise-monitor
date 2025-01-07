# main.py
import schedule
import time
from src.connectwise.client import ConnectWiseClient
from src.monitoring.analyzer import TicketAnalyzer
from src.monitoring.alerts import AlertManager
from src.config import settings
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def monitor_member_tickets(member_identifier: str, member_name: str) -> None:
    """
    Monitor tickets for a specific member and generate alerts if patterns are found
    """
    try:
        client = ConnectWiseClient()
        analyzer = TicketAnalyzer(client)
        alert_manager = AlertManager()
        
        # Analyze tickets
        patterns = analyzer.analyze_member_tickets(member_identifier)
        
        # Generate alert if patterns are found
        if patterns:
            logger.info(f"Patterns detected for {member_name}")
            alert_manager.generate_alert(member_name, patterns)
        else:
            logger.info(f"No significant patterns found for {member_name}")
            
    except Exception as e:
        logger.error(f"Error monitoring tickets for {member_name}: {str(e)}")

def main():
    # List of members to monitor
    members_to_monitor = [
        {"identifier": "sarah.smith", "name": "Sarah Smith"},
        # Add more members as needed
    ]
    
    # Schedule monitoring for each member
    for member in members_to_monitor:
        schedule.every().day.at("08:00").do(
            monitor_member_tickets,
            member["identifier"],
            member["name"]
        )
    
    logger.info("ConnectWise monitoring service started")
    
    # Run continuously
    while True:
        schedule.run_pending()
        time.sleep(60)

if __name__ == "__main__":
    main()