from pydantic import BaseModel, Field
from typing import Dict, List, Any, Optional

class QuestionRequest(BaseModel):
    """Request model for asking questions to the bot"""
    question: str = Field(..., description="The question to ask about bakery data")
    language: Optional[str] = Field("en", description="Language for response (en/ar)")

class QuestionResponse(BaseModel):
    """Response model for bot answers"""
    question: str
    sql_query: Optional[str] = None
    results: Optional[List[Dict[str, Any]]] = None
    analysis: str
    success: bool
    error: Optional[str] = None

class SystemInfoResponse(BaseModel):
    """Response model for system information"""
    bot_name: str
    available_tables: List[str]
    capabilities: List[str]
    database_type: str
    status: str

class HealthCheckResponse(BaseModel):
    """Response model for health check"""
    status: str
    database_connected: bool
    openai_configured: bool
    timestamp: str 