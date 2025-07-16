"""
OpenAI Service for Python 3.8 Compatibility
Alternative to Google Gemini for PythonAnywhere deployment
"""

import openai
import json
import time
import logging
from typing import Dict, Any, Optional

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class OpenAIService:
    """OpenAI service for bakery management system"""
    
    def __init__(self, api_key: str = None, model: str = "gpt-3.5-turbo"):
        """Initialize OpenAI service"""
        self.api_key = api_key or "your-openai-api-key"
        self.model = model
        self.cache = {}
        
        # Set OpenAI API key
        openai.api_key = self.api_key
        
        logger.info(f"OpenAI service initialized with model: {model}")
    
    def get_ai_response(self, user_message: str) -> Dict[str, Any]:
        """Get AI response for user message"""
        try:
            # Check cache first
            cache_key = f"openai_{hash(user_message)}"
            if cache_key in self.cache:
                logger.info("Response retrieved from cache")
                return self.cache[cache_key]
            
            # Create system message for bakery context
            system_message = """
            You are an AI assistant for a bakery management system. 
            You can help with:
            - Product information and inventory
            - Sales analysis and reports
            - Order management
            - Customer data insights
            - Business analytics
            
            Always respond in Arabic and provide helpful, accurate information.
            """
            
            # Make API call to OpenAI
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": user_message}
                ],
                max_tokens=1000,
                temperature=0.7
            )
            
            # Extract response
            ai_response = response.choices[0].message.content
            
            # Prepare result
            result = {
                "response": ai_response,
                "cached": False,
                "processing_time": 0.5,
                "model_used": self.model,
                "tokens_used": response.usage.total_tokens if hasattr(response, 'usage') else 0
            }
            
            # Cache the result
            self.cache[cache_key] = result
            
            logger.info("AI response generated successfully")
            return result
            
        except Exception as e:
            logger.error(f"OpenAI API error: {e}")
            return {
                "response": "عذراً، حدث خطأ في الخدمة. يرجى المحاولة مرة أخرى.",
                "cached": False,
                "processing_time": 0,
                "model_used": self.model,
                "tokens_used": 0,
                "error": str(e)
            }
    
    def get_analytics_report(self, report_type: str = "comprehensive") -> str:
        """Generate analytics report"""
        try:
            prompt = f"""
            Generate a comprehensive analytics report for a bakery management system.
            Report type: {report_type}
            
            Please provide insights on:
            1. Sales performance
            2. Popular products
            3. Customer trends
            4. Inventory status
            5. Business recommendations
            
            Respond in Arabic with professional analysis.
            """
            
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1500,
                temperature=0.5
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            logger.error(f"Analytics report error: {e}")
            return "عذراً، لا يمكن إنشاء التقرير في الوقت الحالي."
    
    def clear_cache(self) -> Dict[str, Any]:
        """Clear response cache"""
        try:
            cache_size = len(self.cache)
            self.cache.clear()
            return {
                "success": True,
                "message": f"تم مسح {cache_size} عنصر من الذاكرة المؤقتة",
                "error": ""
            }
        except Exception as e:
            return {
                "success": False,
                "message": "",
                "error": str(e)
            }
    
    def test_connection(self) -> bool:
        """Test OpenAI API connection"""
        try:
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[{"role": "user", "content": "Hello"}],
                max_tokens=5
            )
            return True
        except Exception as e:
            logger.error(f"OpenAI connection test failed: {e}")
            return False

# Create global instance
openai_service = OpenAIService()

# Fallback function for backward compatibility
def get_ai_response(message: str) -> Dict[str, Any]:
    """Fallback function for compatibility"""
    return openai_service.get_ai_response(message) 