"""
Web API Routes and Static Pages for Bakery Management System
This module provides REST API endpoints and web interface for the bakery management system
"""

from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_cors import CORS
import logging
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import config
from database.connection import db_manager

# Try to import AI service with fallback
try:
    from ai.gemini_service import gemini_service
except ImportError:
    # Fallback to OpenAI service for Python 3.8 compatibility
    try:
        from ai.openai_service import openai_service as gemini_service
    except ImportError:
        # Create dummy service if no AI available
        class DummyAIService:
            def get_ai_response(self, message):
                return {"response": "خدمة الذكاء الاصطناعي غير متوفرة حالياً", "cached": False}
            def get_analytics_report(self, report_type):
                return "التقارير غير متوفرة حالياً"
            def clear_cache(self):
                return {"success": True, "message": "لا توجد ذاكرة مؤقتة"}
        gemini_service = DummyAIService()
        from ai.openai_service import openai_service as gemini_service
    except ImportError:
        # Create dummy service if no AI available
        class DummyAIService:
            def get_ai_response(self, message):
                return {"response": "خدمة الذكاء الاصطناعي غير متوفرة حالياً", "cached": False}
            def get_analytics_report(self, report_type):
                return "التقارير غير متوفرة حالياً"
            def clear_cache(self):
                return {"success": True, "message": "لا توجد ذاكرة مؤقتة"}
        gemini_service = DummyAIService()
except ImportError:
    # Fallback to OpenAI service for Python 3.8 compatibility
    try:
        from ai.openai_service import openai_service as gemini_service
    except ImportError:
        # Create dummy service if no AI available
        class DummyAIService:
            def get_ai_response(self, message):
                return {"response": "خدمة الذكاء الاصطناعي غير متوفرة حالياً", "cached": False}
            def get_analytics_report(self, report_type):
                return "التقارير غير متوفرة حالياً"
            def clear_cache(self):
                return {"success": True, "message": "لا توجد ذاكرة مؤقتة"}
        gemini_service = DummyAIService()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create Flask app
<<<<<<< HEAD
app = Flask(__name__, 
            template_folder='../templates',
            static_folder='../static')

# Enable CORS for React integration
CORS(app, origins=["http://localhost:3000", "http://localhost:3001", "http://localhost:5173", "http://localhost:8000"])

# Main web interface route
@app.route('/')
def index():
    """Main web interface"""
    return render_template('index.html')

# Static files route
@app.route('/static/<path:filename>')
def static_files(filename):
    """Serve static files"""
    return send_from_directory('../static', filename)
=======
app = Flask(__name__)

# Enable CORS for React integration
CORS(app, origins=["http://localhost:3000", "http://localhost:3001", "http://localhost:5173"])
>>>>>>> 0dd058f6d3dead8ce4ad6f62ae5bfc5f080f34a4

# Health check endpoint
@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    try:
        # Test database connection
        tables = db_manager.get_all_tables()
        return jsonify({
            "status": "healthy",
            "database": "connected",
            "tables_count": len(tables),
            "ai_provider": config.AI_PROVIDER,
            "timestamp": db_manager.get_current_timestamp()
        })
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return jsonify({
            "status": "unhealthy",
            "error": str(e)
        }), 500

# AI Chat endpoint
@app.route('/api/chat', methods=['POST'])
def chat():
    """AI chat endpoint for natural language queries"""
    try:
        data = request.get_json()
        
        if not data or 'message' not in data:
            return jsonify({"error": "Message is required"}), 400
        
        user_message = data['message']
        language = data.get('language', 'ar')  # Default to Arabic
        
        # Get AI response
        response = gemini_service.get_ai_response(user_message)
        
        return jsonify({
            "success": True,
            "response": response.get("response", ""),
            "cached": response.get("cached", False),
            "processing_time": response.get("processing_time", 0),
            "model_used": response.get("model_used", ""),
            "tokens_used": response.get("tokens_used", 0),
            "language": language
        })
        
    except Exception as e:
        logger.error(f"Chat endpoint error: {e}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

# Analytics endpoint
@app.route('/api/analytics', methods=['GET'])
def analytics():
    """Get business analytics"""
    try:
        report_type = request.args.get('type', 'comprehensive')
        
        # Get analytics report
        report = gemini_service.get_analytics_report(report_type)
        
        return jsonify({
            "success": True,
            "report": report,
            "report_type": report_type
        })
        
    except Exception as e:
        logger.error(f"Analytics endpoint error: {e}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

# Database query endpoint
@app.route('/api/query', methods=['POST'])
def database_query():
    """Execute database queries"""
    try:
        data = request.get_json()
        
        if not data or 'query' not in data:
            return jsonify({"error": "Query is required"}), 400
        
        query = data['query']
        
        # Security: Only allow SELECT queries
        if not query.strip().upper().startswith('SELECT'):
            return jsonify({"error": "Only SELECT queries are allowed"}), 400
        
        # Execute query
        results = db_manager.execute_query(query)
        
        return jsonify({
            "success": True,
            "results": results,
            "count": len(results) if results else 0
        })
        
    except Exception as e:
        logger.error(f"Database query error: {e}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

# Tables information endpoint
@app.route('/api/tables', methods=['GET'])
def get_tables():
    """Get database tables information"""
    try:
        tables = db_manager.get_all_tables()
        
        tables_info = []
        for table in tables:
            schema = db_manager.get_table_schema(table)
            tables_info.append({
                "name": table,
                "columns": schema.get("columns", [])
            })
        
        return jsonify({
            "success": True,
            "tables": tables_info,
            "count": len(tables)
        })
        
    except Exception as e:
        logger.error(f"Tables endpoint error: {e}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

# Quick stats endpoint
@app.route('/api/stats', methods=['GET'])
def quick_stats():
    """Get quick statistics for dashboard"""
    try:
        stats = {}
        
        # Get basic counts
        try:
            users_count = db_manager.execute_query("SELECT COUNT(*) as count FROM users")[0]['count']
            stats['users'] = users_count
        except:
            stats['users'] = 0
            
        try:
            products_count = db_manager.execute_query("SELECT COUNT(*) as count FROM products")[0]['count']
            stats['products'] = products_count
        except:
            stats['products'] = 0
            
        try:
            orders_count = db_manager.execute_query("SELECT COUNT(*) as count FROM orders")[0]['count']
            stats['orders'] = orders_count
        except:
            stats['orders'] = 0
            
        try:
            stores_count = db_manager.execute_query("SELECT COUNT(*) as count FROM stores")[0]['count']
            stats['stores'] = stores_count
        except:
            stats['stores'] = 0
        
        return jsonify({
            "success": True,
            "stats": stats
        })
        
    except Exception as e:
        logger.error(f"Stats endpoint error: {e}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

# Cache management endpoint
@app.route('/api/cache', methods=['GET', 'DELETE'])
def cache_management():
    """Manage AI response cache"""
    try:
        if request.method == 'GET':
            # Get cache status
            if hasattr(gemini_service, 'cache') and gemini_service.cache:
                return jsonify({
                    "success": True,
                    "cache_enabled": True,
                    "status": "active"
                })
            else:
                return jsonify({
                    "success": True,
                    "cache_enabled": False,
                    "status": "disabled"
                })
                
        elif request.method == 'DELETE':
            # Clear cache
            result = gemini_service.clear_cache()
            return jsonify({
                "success": result.get("success", False),
                "message": result.get("message", ""),
                "error": result.get("error", "")
            })
            
    except Exception as e:
        logger.error(f"Cache management error: {e}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Endpoint not found"}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal server error"}), 500

# Run the app
if __name__ == '__main__':
    try:
        # Initialize database connection
        db_manager.connect()
        logger.info("Database connected successfully")
        
        # Start the Flask app
        app.run(
            host=config.HOST,
            port=config.PORT,
            debug=True
        )
        
    except Exception as e:
        logger.error(f"Failed to start web server: {e}")
        sys.exit(1) 