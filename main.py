#!/usr/bin/env python3
"""
Bakery Management System - Main Entry Point
Starts the web server for React.js integration
"""

import sys
import os

# Add current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import and run the web server
from web_server import main

if __name__ == '__main__':
    main() 