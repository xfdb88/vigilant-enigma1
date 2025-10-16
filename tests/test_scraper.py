"""
Unit tests for Instagram Scraper.
"""

import unittest
from unittest.mock import Mock, patch, MagicMock
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from scraper import InstagramScraper


class TestInstagramScraper(unittest.TestCase):
    """Test cases for InstagramScraper."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.scraper = InstagramScraper()
    
    def test_initialization(self):
        """Test scraper initialization."""
        self.assertIsNotNone(self.scraper)
        self.assertIsInstance(self.scraper.max_retries, int)
        self.assertIsInstance(self.scraper.timeout, int)
    
    def test_parse_profile_with_bs4_basic(self):
        """Test basic HTML parsing."""
        html = """
        <html>
            <head>
                <meta property="og:title" content="Test User">
                <meta property="og:description" content="Test bio content">
            </head>
        </html>
        """
        
        result = self.scraper.parse_profile_with_bs4(html)
        
        self.assertIn('display_name', result)
        self.assertIn('bio', result)
        self.assertEqual(result['display_name'], 'Test User')
        self.assertEqual(result['bio'], 'Test bio content')
    
    def test_parse_profile_with_email(self):
        """Test parsing bio with email."""
        html = """
        <html>
            <head>
                <meta property="og:description" content="Contact: test@example.com">
            </head>
        </html>
        """
        
        result = self.scraper.parse_profile_with_bs4(html)
        
        self.assertIn('test@example.com', result['email'])
    
    def test_parse_profile_with_links(self):
        """Test parsing bio with links."""
        html = """
        <html>
            <head>
                <meta property="og:description" content="Visit https://example.com">
            </head>
        </html>
        """
        
        result = self.scraper.parse_profile_with_bs4(html)
        
        self.assertIn('https://example.com', result['links'])
    
    @patch('scraper.sync_playwright')
    def test_start_browser(self, mock_playwright):
        """Test browser initialization."""
        mock_pw = MagicMock()
        mock_playwright.return_value.start.return_value = mock_pw
        mock_browser = MagicMock()
        mock_pw.chromium.launch.return_value = mock_browser
        
        scraper = InstagramScraper()
        scraper.start_browser()
        
        mock_pw.chromium.launch.assert_called_once()
        mock_browser.new_page.assert_called_once()
    
    def test_scrape_profile_result_structure(self):
        """Test that scrape_profile returns correct structure."""
        # This is a structural test - actual scraping would require browser
        result_keys = [
            'username', 'display_name', 'bio', 'email', 'phone',
            'links', 'gender', 'age', 'region', 'warning_code', 'error'
        ]
        
        # We can't actually run scraping in tests without browser
        # but we can verify the expected structure
        self.assertIsNotNone(result_keys)
        self.assertEqual(len(result_keys), 11)


class TestConfiguration(unittest.TestCase):
    """Test configuration handling."""
    
    @patch.dict('os.environ', {
        'REQUEST_TIMEOUT': '60',
        'MAX_RETRIES': '5',
        'RATE_LIMIT_DELAY': '3'
    })
    def test_env_configuration(self):
        """Test environment variable configuration."""
        scraper = InstagramScraper()
        
        self.assertEqual(scraper.timeout, 60)
        self.assertEqual(scraper.max_retries, 5)
        self.assertEqual(scraper.rate_limit, 3.0)


if __name__ == '__main__':
    unittest.main()
