#!/usr/bin/env python3
"""
Main entry point for Instagram Scraper.
This file is used by PyInstaller to create the executable.
"""

import sys
import os
from pathlib import Path

# Ensure src is in the path
if getattr(sys, 'frozen', False):
    # Running as compiled executable
    application_path = Path(sys._MEIPASS)
else:
    # Running as script
    application_path = Path(__file__).parent

sys.path.insert(0, str(application_path / 'src'))
sys.path.insert(0, str(application_path))

# Now import the actual CLI
from src.cli import main

if __name__ == '__main__':
    main()
