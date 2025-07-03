#!/usr/bin/env python3
"""
Website Uptime Monitor Script
Checks if websites are up or down and measures response time.
Includes logging with timestamps.
"""

import requests
import time
import logging
from datetime import datetime
from typing import List, Dict, Tuple
import json
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('uptime_monitor.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

class UptimeMonitor:
    def __init__(self, websites: List[str], timeout: int = 10):
        """
        Initialize the uptime monitor
        
        Args:
            websites: List of URLs to monitor
            timeout: Request timeout in seconds
        """
        self.websites = websites
        self.timeout = timeout
        self.results = []
        
    def check_website(self, url: str) -> Dict:
        """
        Check if a single website is up and measure response time
        
        Args:
            url: Website URL to check
            
        Returns:
            Dictionary with status information
        """
        start_time = time.time()
        
        try:
            # Ensure URL has protocol
            if not url.startswith(('http://', 'https://')):
                url = 'https://' + url
                
            response = requests.get(url, timeout=self.timeout)
            response_time = round((time.time() - start_time) * 1000, 2)  # Convert to milliseconds
            
            status = {
                'url': url,
                'status': 'UP' if response.status_code == 200 else 'DOWN',
                'status_code': response.status_code,
                'response_time_ms': response_time,
                'timestamp': datetime.now().isoformat(),
                'error': None
            }
            
            if response.status_code == 200:
                logger.info(f"[UP] {url} is UP - Response time: {response_time}ms")
            else:
                logger.warning(f"[WARNING] {url} returned status code {response.status_code} - Response time: {response_time}ms")
                
        except requests.exceptions.Timeout:
            response_time = round((time.time() - start_time) * 1000, 2)
            status = {
                'url': url,
                'status': 'DOWN',
                'status_code': None,
                'response_time_ms': response_time,
                'timestamp': datetime.now().isoformat(),
                'error': 'Timeout'
            }
            logger.error(f"[DOWN] {url} is DOWN - Timeout after {self.timeout}s")
            
        except requests.exceptions.ConnectionError:
            response_time = round((time.time() - start_time) * 1000, 2)
            status = {
                'url': url,
                'status': 'DOWN',
                'status_code': None,
                'response_time_ms': response_time,
                'timestamp': datetime.now().isoformat(),
                'error': 'Connection Error'
            }
            logger.error(f"[DOWN] {url} is DOWN - Connection Error")
            
        except Exception as e:
            response_time = round((time.time() - start_time) * 1000, 2)
            status = {
                'url': url,
                'status': 'DOWN',
                'status_code': None,
                'response_time_ms': response_time,
                'timestamp': datetime.now().isoformat(),
                'error': str(e)
            }
            logger.error(f"[DOWN] {url} is DOWN - Error: {str(e)}")
            
        return status
    
    def check_all_websites(self) -> List[Dict]:
        """
        Check all websites and return results
        
        Returns:
            List of status dictionaries for all websites
        """
        logger.info(f"Starting uptime check for {len(self.websites)} websites...")
        
        results = []
        for website in self.websites:
            result = self.check_website(website)
            results.append(result)
            self.results.append(result)
            
        # Log summary
        up_count = sum(1 for r in results if r['status'] == 'UP')
        down_count = len(results) - up_count
        
        logger.info(f"[SUMMARY] {up_count} UP, {down_count} DOWN out of {len(results)} websites")
        
        return results
    
    def save_results_to_json(self, filename: str = 'uptime_results.json'):
        """
        Save results to JSON file
        
        Args:
            filename: Output filename
        """
        try:
            with open(filename, 'w') as f:
                json.dump(self.results, f, indent=2)
            logger.info(f"Results saved to {filename}")
        except Exception as e:
            logger.error(f"Failed to save results to {filename}: {str(e)}")
    
    def send_email_alert(self, down_sites: List[Dict]):
        """
        Send email alert for down sites
        
        Args:
            down_sites: List of down site dictionaries
        """
        # Email configuration from environment variables
        smtp_server = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
        smtp_port = int(os.getenv('SMTP_PORT', '587'))
        email_user = os.getenv('EMAIL_USER')
        email_password = os.getenv('EMAIL_PASSWORD')
        email_to = os.getenv('EMAIL_TO')
        
        if not all([email_user, email_password, email_to]):
            logger.warning("Email credentials not configured. Skipping email alert.")
            return
            
        try:
            msg = MIMEMultipart()
            msg['From'] = email_user
            msg['To'] = email_to
            msg['Subject'] = f"ALERT: Website Down - {len(down_sites)} sites affected"
            
            body = "The following websites are currently down:\n\n"
            for site in down_sites:
                body += f"• {site['url']} - {site['error'] or 'HTTP ' + str(site['status_code'])}\n"
                body += f"  Checked at: {site['timestamp']}\n\n"
            
            msg.attach(MIMEText(body, 'plain'))
            
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()
            server.login(email_user, email_password)
            text = msg.as_string()
            server.sendmail(email_user, email_to, text)
            server.quit()
            
            logger.info(f"Email alert sent for {len(down_sites)} down sites")
            
        except Exception as e:
            logger.error(f"Failed to send email alert: {str(e)}")
    
    def send_slack_alert(self, down_sites: List[Dict]):
        """
        Send Slack alert for down sites
        
        Args:
            down_sites: List of down site dictionaries
        """
        webhook_url = os.getenv('SLACK_WEBHOOK_URL')
        
        if not webhook_url:
            logger.warning("Slack webhook URL not configured. Skipping Slack alert.")
            return
            
        try:
            message = {
                "text": f"🚨 Website Down Alert - {len(down_sites)} sites affected",
                "attachments": [
                    {
                        "color": "danger",
                        "fields": [
                            {
                                "title": site['url'],
                                "value": f"Status: {site['error'] or 'HTTP ' + str(site['status_code'])}\nTime: {site['timestamp']}",
                                "short": True
                            }
                            for site in down_sites
                        ]
                    }
                ]
            }
            
            response = requests.post(webhook_url, json=message, timeout=10)
            
            if response.status_code == 200:
                logger.info(f"Slack alert sent for {len(down_sites)} down sites")
            else:
                logger.error(f"Failed to send Slack alert: HTTP {response.status_code}")
                
        except Exception as e:
            logger.error(f"Failed to send Slack alert: {str(e)}")

def main():
    """Main function to run the uptime monitor"""
    
    # List of websites to monitor
    websites = [
        'https://google.com',
        'https://github.com',
        'https://stackoverflow.com',
        'https://python.org',
        'https://example.com',
        # Add more websites as needed
    ]
    
    # You can also load websites from environment variable
    env_websites = os.getenv('WEBSITES_TO_MONITOR')
    if env_websites:
        websites = env_websites.split(',')
    
    # Initialize monitor
    monitor = UptimeMonitor(websites, timeout=10)
    
    # Check all websites
    results = monitor.check_all_websites()
    
    # Save results to JSON
    monitor.save_results_to_json()
    
    # Check for down sites and send alerts
    down_sites = [site for site in results if site['status'] == 'DOWN']
    
    if down_sites:
        logger.warning(f"Found {len(down_sites)} down sites. Sending alerts...")
        monitor.send_email_alert(down_sites)
        monitor.send_slack_alert(down_sites)
    else:
        logger.info("All websites are up! All systems operational.")

if __name__ == "__main__":
    main()