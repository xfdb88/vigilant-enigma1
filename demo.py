#!/usr/bin/env python3
"""
Demo script showing how to use the Instagram Scraper programmatically.
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from scraper import InstagramScraper


def demo_single_profile():
    """Demo: Scrape a single profile."""
    print("=" * 60)
    print("Demo 1: Scraping a single Instagram profile")
    print("=" * 60)
    
    scraper = InstagramScraper()
    
    try:
        scraper.start_browser()
        
        username = "instagram"
        print(f"\nScraping profile: {username}")
        
        result = scraper.scrape_profile(username)
        
        print("\nResults:")
        print("-" * 60)
        for key, value in result.items():
            if value:
                print(f"{key:15}: {value}")
        
    finally:
        scraper.close_browser()


def demo_batch_scraping():
    """Demo: Batch scraping from CSV."""
    print("\n" + "=" * 60)
    print("Demo 2: Batch scraping from CSV")
    print("=" * 60)
    
    # Create sample input
    sample_usernames = ['instagram', 'natgeo']
    
    with open('data/demo_input.csv', 'w') as f:
        f.write('username\n')
        for username in sample_usernames:
            f.write(f'{username}\n')
    
    print(f"\nCreated demo_input.csv with {len(sample_usernames)} usernames")
    
    scraper = InstagramScraper()
    scraper.scrape_from_csv('data/demo_input.csv', 'data/demo_output.csv')
    
    print("\nResults saved to data/demo_output.csv")


def demo_custom_config():
    """Demo: Using custom configuration."""
    print("\n" + "=" * 60)
    print("Demo 3: Custom configuration")
    print("=" * 60)
    
    import os
    
    # Set custom configuration
    os.environ['REQUEST_TIMEOUT'] = '60'
    os.environ['MAX_RETRIES'] = '5'
    os.environ['RATE_LIMIT_DELAY'] = '3'
    
    scraper = InstagramScraper()
    
    print(f"\nCustom configuration:")
    print(f"  Timeout: {scraper.timeout}s")
    print(f"  Max retries: {scraper.max_retries}")
    print(f"  Rate limit: {scraper.rate_limit}s")


if __name__ == '__main__':
    print("\nInstagram Scraper - Demo Script")
    print("=" * 60)
    print("\nThis script demonstrates the three main usage patterns:\n")
    print("1. Scraping a single profile")
    print("2. Batch scraping from CSV")
    print("3. Custom configuration")
    print("\n" + "=" * 60)
    
    choice = input("\nWhich demo would you like to run? (1/2/3 or 'all'): ").strip()
    
    if choice == '1':
        demo_single_profile()
    elif choice == '2':
        demo_batch_scraping()
    elif choice == '3':
        demo_custom_config()
    elif choice.lower() == 'all':
        demo_custom_config()
        # Note: Browser demos are commented out to avoid actual web scraping
        print("\n[Browser demos disabled for safety - uncomment to run]")
        # demo_single_profile()
        # demo_batch_scraping()
    else:
        print("Invalid choice. Please run with 1, 2, 3, or 'all'")
