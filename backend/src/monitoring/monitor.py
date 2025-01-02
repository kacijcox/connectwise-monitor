# backend/monitor.py
import schedule
import time
from src.connectwise.client import ConnectWiseClient
from src.monitoring.analyzer import TicketAnalyzer
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def check_patterns():
    try:
        cw_client = ConnectWiseClient()
        analyzer = TicketAnalyzer(cw_client)
        
        logger.info("Checking for ticket patterns...")
        patterns = analyzer.analyze_tickets()
        
        if patterns:
            logger.info(f"Found {len(patterns)} patterns")
            for pattern in patterns:
                logger.info(f"User: {pattern['user']}")
                logger.info(f"Pattern Details: {pattern['pattern_details']}")
        else:
            logger.info("No significant patterns detected")
            
    except Exception as e:
        logger.error(f"Error checking patterns: {str(e)}")

def main():
    logger.info("Starting pattern monitoring service...")
    
    # Run initial check
    check_patterns()
    
    # Schedule regular checks
    schedule.every(30).minutes.do(check_patterns)
    
    while True:
        schedule.run_pending()
        time.sleep(60)

if __name__ == "__main__":
    main()