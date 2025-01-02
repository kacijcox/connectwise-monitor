# src/config/settings.py
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# ConnectWise API Configuration
CW_COMPANY_ID = os.getenv('CW_COMPANY_ID')
CW_PUBLIC_KEY = os.getenv('CW_PUBLIC_KEY')
CW_PRIVATE_KEY = os.getenv('CW_PRIVATE_KEY')
CW_CLIENT_ID = os.getenv('CW_CLIENT_ID')
CW_BASE_URL = os.getenv('CW_BASE_URL')

# Alert Configuration
ALERT_THRESHOLD = int(os.getenv('ALERT_THRESHOLD', '3'))  # Minimum tickets to trigger alert
ALERT_TIMEFRAME_DAYS = int(os.getenv('ALERT_TIMEFRAME_DAYS', '7'))  # Time window for analysis

# Notification Settings
NOTIFICATION_EMAIL = os.getenv('NOTIFICATION_EMAIL')
SMTP_SERVER = os.getenv('SMTP_SERVER')
SMTP_PORT = int(os.getenv('SMTP_PORT', '587'))
SMTP_USERNAME = os.getenv('SMTP_USERNAME')
SMTP_PASSWORD = os.getenv('SMTP_PASSWORD')