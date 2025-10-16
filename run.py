#!/usr/bin/env python3
"""
Instagram Scraper - Quick Start Script
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from cli import main

if __name__ == '__main__':
    main()
