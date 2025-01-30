# ConnectWise Monitor

The ConnectWise Monitor is an application that analyzes support tickets from ConnectWise PSA to identify patterns. It helps service desk teams gain insights into recurring issues and improve their support processes.
=======
The ConnectWise Monitor is an application that analyzes support tickets from ConnectWise PSA to identify patterns and potential root causes leveraging Claude. It helps service desk teams gain insights into recurring issues and improve their support processes.

## Features

- Retrieves support tickets from ConnectWise PSA API
- Analyzes tickets to identify patterns and trends
- Sends email notifications when significant patterns are detected
- Provides a web interface for viewing analysis results
  

## Prerequisites

- Python 3.x
- ConnectWise PSA account with API access
- Email account for sending email notifications

## Installation

1. Clone the repository:
   - git clone https://github.com/kacijcox/connectwise-monitor.git
2. Install the required dependencies:
   -pip install -r requirements.txt
3. Set up the environment variables:
- Create a `.env` file in the project root.
- Add the following variables to the `.env` file:
  ```
  SMTP_SERVER=smtp.gmail.com
  SMTP_PORT=587
  SENDER_EMAIL=your_gmail_email
  SENDER_PASSWORD=your_gmail_password
  RECIPIENT_EMAIL=recipient_email
  ```
- Replace `your_gmail_email`, `your_gmail_password`, and `recipient_email` with your actual values.

## Usage

1. Run the Flask application:
   -python routes.py
2. Access the web interface:
- Open a web browser and go to `http://localhost:5000`.
- Use the available endpoints to retrieve analysis results.
