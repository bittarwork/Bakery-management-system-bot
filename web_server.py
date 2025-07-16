#!/usr/bin/env python3
"""
Bakery Management System - Web Server for React Integration
Simple web server to run the bakery management API
"""

import os
import sys
import logging
from api.web_routes import app

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def main():
    """Main entry point for the web server"""
    try:
        logger.info("🚀 Starting Bakery Management System Web Server...")
        logger.info("📊 Ready for React.js integration")
        logger.info("🌐 API endpoints available at: http://localhost:8000/api/")
        
        # Run the Flask app
        app.run(
            host='0.0.0.0',
            port=8000,
            debug=True
        )
        
    except Exception as e:
        logger.error(f"❌ Failed to start web server: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main() 