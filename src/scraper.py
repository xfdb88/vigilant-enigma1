"""
Instagram Public User Scraper
A tool to scrape public Instagram user profile information.

License: MIT
WARNING: This tool is for educational purposes only. 
Only scrape public information and respect Instagram's Terms of Service.
"""

import os
import csv
import time
import logging
from typing import Dict, Optional, List
from pathlib import Path
import httpx
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright, Browser, Page
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('scraper.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class InstagramScraper:
    """Instagram public profile scraper using Playwright and httpx/BeautifulSoup."""
    
    def __init__(self):
        """Initialize the scraper with configuration from environment."""
        self.username = os.getenv('INSTAGRAM_USERNAME', '')
        self.password = os.getenv('INSTAGRAM_PASSWORD', '')
        self.proxy_server = os.getenv('PROXY_SERVER', '')
        self.proxy_username = os.getenv('PROXY_USERNAME', '')
        self.proxy_password = os.getenv('PROXY_PASSWORD', '')
        self.timeout = int(os.getenv('REQUEST_TIMEOUT', '30'))
        self.max_retries = int(os.getenv('MAX_RETRIES', '3'))
        self.retry_delay = int(os.getenv('RETRY_DELAY', '5'))
        self.rate_limit = float(os.getenv('RATE_LIMIT_DELAY', '2'))
        
        self.browser: Optional[Browser] = None
        self.page: Optional[Page] = None
        
    def start_browser(self):
        """Start Playwright browser instance."""
        try:
            playwright = sync_playwright().start()
            
            launch_options = {
                'headless': True,
            }
            
            if self.proxy_server:
                proxy_config = {'server': self.proxy_server}
                if self.proxy_username and self.proxy_password:
                    proxy_config['username'] = self.proxy_username
                    proxy_config['password'] = self.proxy_password
                launch_options['proxy'] = proxy_config
            
            self.browser = playwright.chromium.launch(**launch_options)
            self.page = self.browser.new_page()
            logger.info("Browser started successfully")
            
        except Exception as e:
            logger.error(f"Failed to start browser: {e}")
            raise
    
    def close_browser(self):
        """Close the browser instance."""
        if self.browser:
            self.browser.close()
            logger.info("Browser closed")
    
    def parse_profile_with_bs4(self, html: str) -> Dict[str, str]:
        """Parse Instagram profile HTML using BeautifulSoup."""
        soup = BeautifulSoup(html, 'lxml')
        
        profile_data = {
            'display_name': '',
            'bio': '',
            'email': '',
            'phone': '',
            'links': '',
            'gender': '',
            'age': '',
            'region': ''
        }
        
        try:
            # Try to extract data from JSON-LD or meta tags
            # Instagram uses React and stores data in script tags
            scripts = soup.find_all('script', type='application/ld+json')
            
            # Try meta tags
            og_title = soup.find('meta', property='og:title')
            if og_title and og_title.get('content'):
                profile_data['display_name'] = og_title['content']
            
            og_description = soup.find('meta', property='og:description')
            if og_description and og_description.get('content'):
                desc = og_description['content']
                profile_data['bio'] = desc
                
                # Try to extract email from bio
                import re
                email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
                emails = re.findall(email_pattern, desc)
                if emails:
                    profile_data['email'] = ', '.join(emails)
                
                # Try to extract links
                url_pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
                links = re.findall(url_pattern, desc)
                if links:
                    profile_data['links'] = ', '.join(links)
            
        except Exception as e:
            logger.error(f"Error parsing profile with BS4: {e}")
        
        return profile_data
    
    def scrape_profile(self, username: str) -> Dict[str, str]:
        """
        Scrape a single Instagram profile.
        
        Args:
            username: Instagram username to scrape
            
        Returns:
            Dictionary containing profile data
        """
        result = {
            'username': username,
            'display_name': '',
            'bio': '',
            'email': '',
            'phone': '',
            'links': '',
            'gender': '',
            'age': '',
            'region': '',
            'warning_code': '',
            'error': ''
        }
        
        url = f'https://www.instagram.com/{username}/'
        
        for attempt in range(self.max_retries):
            try:
                logger.info(f"Scraping {username} (attempt {attempt + 1}/{self.max_retries})")
                
                # Navigate to profile page
                response = self.page.goto(url, timeout=self.timeout * 1000)
                
                # Check status code
                if response and response.status == 404:
                    result['error'] = 'Profile not found'
                    result['warning_code'] = '404'
                    logger.warning(f"Profile {username} not found")
                    return result
                
                if response and response.status == 429:
                    result['error'] = 'Rate limited'
                    result['warning_code'] = '429'
                    logger.warning(f"Rate limited on {username}")
                    time.sleep(self.retry_delay * (attempt + 1))
                    continue
                
                # Wait for content to load
                time.sleep(2)
                
                # Get page HTML
                html = self.page.content()
                
                # Also try with httpx for comparison
                try:
                    with httpx.Client(timeout=self.timeout) as client:
                        httpx_response = client.get(url)
                        if httpx_response.status_code == 200:
                            # Parse with BeautifulSoup
                            profile_data = self.parse_profile_with_bs4(httpx_response.text)
                            result.update(profile_data)
                except Exception as e:
                    logger.warning(f"httpx request failed for {username}: {e}")
                    # Fall back to Playwright HTML
                    profile_data = self.parse_profile_with_bs4(html)
                    result.update(profile_data)
                
                # Check for private account warning
                if 'This Account is Private' in html:
                    result['warning_code'] = 'PRIVATE'
                    logger.info(f"Profile {username} is private")
                
                logger.info(f"Successfully scraped {username}")
                return result
                
            except Exception as e:
                logger.error(f"Error scraping {username} (attempt {attempt + 1}): {e}")
                result['error'] = str(e)
                
                if attempt < self.max_retries - 1:
                    time.sleep(self.retry_delay)
                    
        return result
    
    def scrape_from_csv(self, input_file: str, output_file: str):
        """
        Scrape multiple profiles from CSV file.
        
        Args:
            input_file: Path to input CSV with usernames
            output_file: Path to output CSV for results
        """
        try:
            self.start_browser()
            
            # Read usernames
            usernames = []
            with open(input_file, 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
                next(reader, None)  # Skip header if present
                for row in reader:
                    if row and row[0].strip():
                        usernames.append(row[0].strip())
            
            logger.info(f"Found {len(usernames)} usernames to scrape")
            
            # Prepare output file
            fieldnames = [
                'username', 'display_name', 'bio', 'email', 'phone',
                'links', 'gender', 'age', 'region', 'warning_code', 'error'
            ]
            
            with open(output_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                
                # Scrape each profile
                for i, username in enumerate(usernames, 1):
                    logger.info(f"Processing {i}/{len(usernames)}: {username}")
                    
                    result = self.scrape_profile(username)
                    writer.writerow(result)
                    f.flush()  # Ensure data is written immediately
                    
                    # Rate limiting
                    if i < len(usernames):
                        time.sleep(self.rate_limit)
            
            logger.info(f"Scraping complete. Results saved to {output_file}")
            
        finally:
            self.close_browser()


def main():
    """Main entry point for the scraper."""
    input_file = 'data/input.csv'
    output_file = 'data/output.csv'
    
    # Create data directory if it doesn't exist
    Path('data').mkdir(exist_ok=True)
    
    # Check if input file exists
    if not Path(input_file).exists():
        logger.error(f"Input file {input_file} not found")
        print(f"Error: {input_file} not found. Please create it with Instagram usernames.")
        return
    
    scraper = InstagramScraper()
    scraper.scrape_from_csv(input_file, output_file)
    
    print(f"\nScraping complete! Results saved to {output_file}")


if __name__ == '__main__':
    main()
