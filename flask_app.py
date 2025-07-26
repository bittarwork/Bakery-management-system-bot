#!/usr/bin/env python3
"""
Flask App Entry Point for PythonAnywhere
This file is the main entry point for the Bakery Management System on PythonAnywhere
"""

import sys
import os
import logging

# Add the project directory to the Python path
project_home = '/home/osamabakery/mysite'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

try:
    # Import the main Flask application from api.web_routes
    from api.web_routes import app
    
    # Initialize database connection
    from database.connection import db_manager
    db_manager.connect()
    logger.info("✅ Database connected successfully")
    
    logger.info("🚀 Bakery Management System loaded successfully")
    logger.info("🍰 Welcome to the Bakery Management System!")
    
except Exception as e:
    logger.error(f"❌ Failed to initialize application: {e}")
    # Create a simple fallback app
    from flask import Flask
    app = Flask(__name__)
    
    @app.route('/')
    def error_page():
        return f"""
        <h1>🚫 خطأ في تحميل نظام المخبز</h1>
        <p>حدث خطأ أثناء تحميل التطبيق: {str(e)}</p>
        <p>يرجى التحقق من إعدادات قاعدة البيانات والملفات</p>
        """

# Export the app for PythonAnywhere
application = app

if __name__ == "__main__":
    app.run(debug=False) 