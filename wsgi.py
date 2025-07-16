#!/usr/bin/env python3
"""
WSGI Configuration for PythonAnywhere Deployment
This file configures the Flask application for deployment on PythonAnywhere
"""

import sys
import os

# Add the project directory to the Python path
project_home = '/home/yourusername/mysite'  # Change this to your actual path on PythonAnywhere
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# Set up the virtual environment (if using one)
# Uncomment the following lines if you're using a virtual environment
# activate_this = '/home/yourusername/mysite/venv/bin/activate_this.py'
# with open(activate_this) as file_:
#     exec(file_.read(), dict(__file__=activate_this))

# Import the Flask application
from api.web_routes import app as application

# Configure logging for production
import logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('bakery_app.log'),
        logging.StreamHandler()
    ]
)

# Initialize database connection
try:
    from database.connection import db_manager
    db_manager.connect()
    logging.info("Database connected successfully")
except Exception as e:
    logging.error(f"Database connection failed: {e}")

if __name__ == "__main__":
    application.run(debug=False) 