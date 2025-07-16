import google.generativeai as genai
from typing import Dict, List, Any, Optional, Tuple
import json
import logging
from config import config
from database.connection import db_manager
import time
import random
import hashlib
import sqlite3
import os
from datetime import datetime, timedelta
import asyncio
import threading

# Configure logging
logger = logging.getLogger(__name__)

class SmartCache:
    """Smart caching system for AI responses"""
    
    def __init__(self, cache_file: str = "ai_cache.db"):
        self.cache_file = cache_file
        self._init_cache()
    
    def _init_cache(self):
        """Initialize SQLite cache database"""
        conn = sqlite3.connect(self.cache_file)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS ai_cache (
                query_hash TEXT PRIMARY KEY,
                query TEXT,
                response TEXT,
                timestamp DATETIME,
                hit_count INTEGER DEFAULT 1
            )
        ''')
        conn.commit()
        conn.close()
    
    def get_cache_key(self, query: str, context: str = "") -> str:
        """Generate cache key for query"""
        combined = f"{query}:{context}"
        return hashlib.md5(combined.encode()).hexdigest()
    
    def get_cached_response(self, query: str, context: str = "") -> Optional[str]:
        """Get cached response if available and not expired"""
        cache_key = self.get_cache_key(query, context)
        conn = sqlite3.connect(self.cache_file)
        cursor = conn.cursor()
        
        # Get cached response (valid for 1 hour)
        cursor.execute('''
            SELECT response, timestamp FROM ai_cache 
            WHERE query_hash = ? AND datetime(timestamp) > datetime('now', '-1 hour')
        ''', (cache_key,))
        
        result = cursor.fetchone()
        if result:
            # Update hit count
            cursor.execute('''
                UPDATE ai_cache SET hit_count = hit_count + 1 
                WHERE query_hash = ?
            ''', (cache_key,))
            conn.commit()
            conn.close()
            return result[0]
        
        conn.close()
        return None
    
    def cache_response(self, query: str, response: str, context: str = ""):
        """Cache AI response"""
        cache_key = self.get_cache_key(query, context)
        conn = sqlite3.connect(self.cache_file)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT OR REPLACE INTO ai_cache 
            (query_hash, query, response, timestamp, hit_count)
            VALUES (?, ?, ?, ?, 1)
        ''', (cache_key, query, response, datetime.now().isoformat()))
        
        conn.commit()
        conn.close()

class AdvancedAnalytics:
    """Advanced analytics for bakery data"""
    
    def __init__(self, db_manager):
        self.db_manager = db_manager
    
    def get_sales_trends(self, days: int = 30) -> Dict[str, Any]:
        """Get detailed sales trends analysis"""
        query = f"""
        SELECT 
            DATE(created_at) as date,
            COUNT(*) as order_count,
            SUM(COALESCE(amount, 0)) as total_sales,
            AVG(COALESCE(amount, 0)) as avg_order_value
        FROM orders 
        WHERE created_at >= DATE_SUB(NOW(), INTERVAL {days} DAY)
        GROUP BY DATE(created_at)
        ORDER BY date DESC
        """
        
        try:
            results = self.db_manager.execute_query(query)
            return {
                "period_days": days,
                "daily_trends": results,
                "summary": self._calculate_trends_summary(results)
            }
        except Exception as e:
            logger.error(f"Error getting sales trends: {e}")
            # Fallback query for basic order count
            fallback_query = f"""
            SELECT 
                DATE(created_at) as date,
                COUNT(*) as order_count,
                COUNT(*) * 25 as estimated_sales,
                25 as avg_order_value
            FROM orders 
            WHERE created_at >= DATE_SUB(NOW(), INTERVAL {days} DAY)
            GROUP BY DATE(created_at)
            ORDER BY date DESC
            """
            try:
                results = self.db_manager.execute_query(fallback_query)
                return {
                    "period_days": days,
                    "daily_trends": results,
                    "summary": self._calculate_trends_summary(results, fallback=True),
                    "note": "Using estimated values due to database schema differences"
                }
            except Exception as fallback_error:
                logger.error(f"Fallback query also failed: {fallback_error}")
                return {"error": str(e)}
    
    def _calculate_trends_summary(self, daily_data: List[Dict], fallback: bool = False) -> Dict[str, Any]:
        """Calculate summary statistics for trends"""
        if not daily_data:
            return {}
        
        # Handle different column names based on query type
        sales_key = 'estimated_sales' if fallback else 'total_sales'
        
        total_sales = sum(float(day.get(sales_key, 0)) for day in daily_data)
        total_orders = sum(int(day.get('order_count', 0)) for day in daily_data)
        avg_daily_sales = total_sales / len(daily_data) if daily_data else 0
        
        return {
            "total_sales": total_sales,
            "total_orders": total_orders,
            "avg_daily_sales": avg_daily_sales,
            "avg_order_value": total_sales / total_orders if total_orders > 0 else 0,
            "is_estimated": fallback
        }
    
    def get_product_performance(self) -> Dict[str, Any]:
        """Get detailed product performance analysis"""
        query = """
        SELECT 
            p.name as product_name,
            p.category,
            p.price,
            COUNT(oi.id) as times_ordered,
            SUM(oi.quantity) as total_quantity_sold,
            SUM(oi.quantity * p.price) as total_revenue
        FROM products p
        LEFT JOIN order_items oi ON p.id = oi.product_id
        GROUP BY p.id, p.name, p.category, p.price
        ORDER BY total_revenue DESC
        """
        
        try:
            results = self.db_manager.execute_query(query)
            return {
                "products": results,
                "top_performers": results[:5] if results else [],
                "categories_summary": self._get_category_summary(results)
            }
        except Exception as e:
            logger.error(f"Error getting product performance: {e}")
            return {"error": str(e)}
    
    def _get_category_summary(self, product_data: List[Dict]) -> Dict[str, Any]:
        """Summarize performance by category"""
        categories = {}
        for product in product_data:
            category = product.get('category', 'Unknown')
            if category not in categories:
                categories[category] = {
                    'total_revenue': 0,
                    'total_quantity': 0,
                    'product_count': 0
                }
            
            categories[category]['total_revenue'] += float(product.get('total_revenue', 0))
            categories[category]['total_quantity'] += int(product.get('total_quantity_sold', 0))
            categories[category]['product_count'] += 1
        
        return categories

class GeminiServicePro:
    """Advanced Gemini service with premium features for Google Cloud AI"""
    
    def __init__(self):
        """Initialize enhanced Gemini service"""
        genai.configure(api_key=config.GEMINI_API_KEY)
        
        # Use the most advanced model available
        self.model = genai.GenerativeModel(
            config.GEMINI_MODEL,
            generation_config=genai.GenerationConfig(
                max_output_tokens=config.MAX_TOKENS,
                temperature=config.TEMPERATURE,
                top_p=config.TOP_P,
                top_k=config.TOP_K,
            )
        )
        
        # Initialize premium features
        self.cache = SmartCache() if config.ENABLE_SMART_CACHING else None
        self.analytics = AdvancedAnalytics(db_manager) if config.ENABLE_ADVANCED_ANALYTICS else None
        
        # Rate limiting (more generous for paid API)
        self.last_request_time = 0
        self.min_request_interval = 0.5  # 500ms for premium API
        
        # Multi-language support
        self.supported_languages = {
            'ar': 'Arabic',
            'en': 'English',
            'fr': 'French',
            'es': 'Spanish',
            'de': 'German'
        }
    
    def _wait_for_rate_limit(self):
        """Optimized rate limiting for premium API"""
        current_time = time.time()
        time_since_last_request = current_time - self.last_request_time
        
        if time_since_last_request < self.min_request_interval:
            wait_time = self.min_request_interval - time_since_last_request
            time.sleep(wait_time)
        
        self.last_request_time = time.time()
    
    def get_enhanced_database_context(self) -> str:
        """Get comprehensive database context with analytics"""
        try:
            # Basic schema info
            tables = db_manager.get_all_tables()
            context_parts = [
                "=== BAKERY MANAGEMENT SYSTEM DATABASE ===",
                f"Total Tables: {len(tables)}",
                ""
            ]
            
            # Add table schemas
            for table in tables:
                schema = db_manager.get_table_schema(table)
                context_parts.append(f"Table: {table}")
                if "columns" in schema:
                    for column in schema["columns"]:
                        context_parts.append(f"  - {column['column_name']}: {column['data_type']}")
                context_parts.append("")
            
            # Add analytics if enabled
            if self.analytics:
                context_parts.extend([
                    "=== RECENT ANALYTICS ===",
                    "Sales Trends (Last 7 days):",
                ])
                
                trends = self.analytics.get_sales_trends(7)
                if 'summary' in trends:
                    summary = trends['summary']
                    context_parts.append(f"  - Total Sales: €{summary.get('total_sales', 0):.2f}")
                    context_parts.append(f"  - Total Orders: {summary.get('total_orders', 0)}")
                    context_parts.append(f"  - Average Order Value: €{summary.get('avg_order_value', 0):.2f}")
                
                context_parts.append("")
            
            return "\n".join(context_parts)
            
        except Exception as e:
            logger.error(f"Error getting enhanced database context: {e}")
            return self._get_basic_context()
    
    def _get_basic_context(self) -> str:
        """Fallback to basic context if enhanced fails"""
        try:
            tables = db_manager.get_all_tables()
            return f"Database Tables: {', '.join(tables)}"
        except Exception as e:
            logger.error(f"Error getting basic context: {e}")
            return "Database connection error"
    
    def detect_language(self, text: str) -> str:
        """Detect the language of input text"""
        # Simple language detection based on character patterns
        arabic_chars = sum(1 for char in text if '\u0600' <= char <= '\u06FF')
        total_chars = len([char for char in text if char.isalpha()])
        
        if total_chars > 0 and arabic_chars / total_chars > 0.3:
            return 'ar'
        return 'en'
    
    def enhance_prompt(self, user_query: str, context: str) -> str:
        """Create enhanced prompt with advanced instructions"""
        detected_lang = self.detect_language(user_query)
        
        enhanced_prompt = f"""
You are BakeryBot Pro, an advanced AI assistant specialized in bakery management systems.
You have access to a comprehensive MySQL database with the following structure:

{context}

ADVANCED CAPABILITIES:
- Multi-language support (Arabic, English, French, Spanish, German)
- Advanced analytics and trend analysis
- Smart caching for faster responses
- Detailed financial reporting
- Inventory optimization suggestions
- Customer behavior analysis

RESPONSE GUIDELINES:
- Detected Language: {self.supported_languages.get(detected_lang, 'English')}
- Provide detailed, actionable insights
- Include relevant statistics and trends when available
- Suggest improvements and optimizations
- Use professional formatting with bullet points and sections
- Always format currency in Euros (€) or Syrian Pounds (SYP)
- Include confidence levels for predictions

USER QUERY: {user_query}

Provide a comprehensive, professional response with:
1. Direct answer to the query
2. Relevant data analysis
3. Actionable recommendations
4. Future predictions if applicable
"""
        
        return enhanced_prompt
    
    async def get_ai_response_async(self, user_query: str) -> Dict[str, Any]:
        """Asynchronous AI response for better performance"""
        try:
            # Check cache first
            if self.cache:
                cached = self.cache.get_cached_response(user_query)
                if cached:
                    return {
                        "response": cached,
                        "cached": True,
                        "processing_time": 0.1
                    }
            
            start_time = time.time()
            
            # Get enhanced context
            context = self.get_enhanced_database_context()
            
            # Create enhanced prompt
            enhanced_prompt = self.enhance_prompt(user_query, context)
            
            # Rate limiting
            self._wait_for_rate_limit()
            
            # Generate response
            response = self.model.generate_content(enhanced_prompt)
            
            processing_time = time.time() - start_time
            
            result = {
                "response": response.text,
                "cached": False,
                "processing_time": processing_time,
                "model_used": config.GEMINI_MODEL,
                "tokens_used": len(response.text.split())
            }
            
            # Cache the response
            if self.cache:
                self.cache.cache_response(user_query, response.text, context)
            
            return result
            
        except Exception as e:
            logger.error(f"Error in async AI response: {e}")
            return {
                "response": f"عذراً، حدث خطأ في معالجة استفسارك: {str(e)}",
                "error": True,
                "cached": False
            }
    
    def get_ai_response(self, user_query: str) -> Dict[str, Any]:
        """Main method for getting AI responses with premium features"""
        try:
            # For now, use synchronous version
            # In future, can be upgraded to async
            return self._get_sync_response(user_query)
            
        except Exception as e:
            logger.error(f"Error getting AI response: {e}")
            return {
                "response": f"عذراً، حدث خطأ في معالجة استفسارك: {str(e)}",
                "error": True
            }
    
    def _get_sync_response(self, user_query: str) -> Dict[str, Any]:
        """Synchronous version of AI response"""
        try:
            # Check cache first
            if self.cache:
                cached = self.cache.get_cached_response(user_query)
                if cached:
                    return {
                        "response": cached,
                        "cached": True,
                        "processing_time": 0.1
                    }
            
            start_time = time.time()
            
            # Get enhanced context
            context = self.get_enhanced_database_context()
            
            # Create enhanced prompt
            enhanced_prompt = self.enhance_prompt(user_query, context)
            
            # Rate limiting
            self._wait_for_rate_limit()
            
            # Generate response with retry logic
            max_retries = 3
            for attempt in range(max_retries):
                try:
                    response = self.model.generate_content(enhanced_prompt)
                    break
                except Exception as e:
                    if attempt == max_retries - 1:
                        raise e
                    time.sleep(1 * (attempt + 1))  # Exponential backoff
            
            processing_time = time.time() - start_time
            
            result = {
                "response": response.text,
                "cached": False,
                "processing_time": processing_time,
                "model_used": config.GEMINI_MODEL,
                "tokens_used": len(response.text.split())
            }
            
            # Cache the response
            if self.cache:
                self.cache.cache_response(user_query, response.text, context)
            
            return result
            
        except Exception as e:
            logger.error(f"Error in sync AI response: {e}")
            return {
                "response": f"عذراً، حدث خطأ في معالجة استفسارك: {str(e)}",
                "error": True,
                "cached": False
            }
    
    def get_analytics_report(self, report_type: str = "comprehensive") -> Dict[str, Any]:
        """Generate comprehensive analytics reports"""
        if not self.analytics:
            return {"error": "Analytics not enabled"}
        
        try:
            if report_type == "comprehensive":
                return {
                    "sales_trends": self.analytics.get_sales_trends(30),
                    "product_performance": self.analytics.get_product_performance(),
                    "generated_at": datetime.now().isoformat(),
                    "report_type": report_type
                }
            elif report_type == "sales":
                return self.analytics.get_sales_trends(30)
            elif report_type == "products":
                return self.analytics.get_product_performance()
            else:
                return {"error": f"Unknown report type: {report_type}"}
                
        except Exception as e:
            logger.error(f"Error generating analytics report: {e}")
            return {"error": str(e)}
    
    def clear_cache(self):
        """Clear AI response cache"""
        if self.cache:
            try:
                os.remove(self.cache.cache_file)
                self.cache._init_cache()
                return {"success": True, "message": "Cache cleared successfully"}
            except Exception as e:
                return {"success": False, "error": str(e)}
        return {"success": False, "error": "Cache not enabled"}

# Create global instance
gemini_service = GeminiServicePro()

# Backward compatibility
GeminiService = GeminiServicePro 