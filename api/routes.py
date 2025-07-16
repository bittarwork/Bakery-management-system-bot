from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging
from datetime import datetime
from typing import Dict, Any

from api.models import (
    QuestionRequest, 
    QuestionResponse, 
    SystemInfoResponse, 
    HealthCheckResponse
)
from ai import chatgpt_service, gemini_service
from database.connection import db_manager
from config import config

# Configure logging
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Bakery Management Bot API",
    description="AI-powered chatbot for bakery management system",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    """Initialize services on startup"""
    try:
        # Validate configuration
        config.validate()
        logger.info("Configuration validated successfully")
        
        # Test database connection
        db_manager.get_all_tables()
        logger.info("Database connection established")
        
    except Exception as e:
        logger.error(f"Startup failed: {str(e)}")
        raise

@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    try:
        db_manager.close()
        logger.info("Database connections closed")
    except Exception as e:
        logger.error(f"Shutdown error: {str(e)}")

@app.get("/", response_model=Dict[str, str])
async def root():
    """Root endpoint with basic information"""
    return {
        "message": f"Welcome to {config.BOT_NAME} API",
        "version": "1.0.0",
        "status": "running"
    }

@app.get("/health", response_model=HealthCheckResponse)
async def health_check():
    """Health check endpoint"""
    try:
        # Check database connection
        db_manager.get_all_tables()
        database_connected = True
    except Exception as e:
        logger.error(f"Database health check failed: {str(e)}")
        database_connected = False
    
    # Check AI provider configuration
    if config.AI_PROVIDER == "openai":
        ai_configured = bool(config.OPENAI_API_KEY)
    elif config.AI_PROVIDER == "gemini":
        ai_configured = bool(config.GEMINI_API_KEY)
    else:
        ai_configured = False
    
    return HealthCheckResponse(
        status="healthy" if database_connected and ai_configured else "unhealthy",
        database_connected=database_connected,
        openai_configured=ai_configured,
        timestamp=datetime.now().isoformat()
    )

@app.get("/info", response_model=SystemInfoResponse)
async def get_system_info():
    """Get system information and capabilities"""
    try:
        # Select the appropriate AI service based on configuration
        if config.AI_PROVIDER == "openai":
            ai_service = chatgpt_service
        elif config.AI_PROVIDER == "gemini":
            ai_service = gemini_service
        else:
            raise HTTPException(status_code=500, detail="No valid AI provider configured")
        
        # Get system info from the AI service
        system_info = ai_service.get_system_info()
        
        tables = db_manager.get_all_tables()
        
        capabilities = [
            "Product inventory queries",
            "Sales analysis and reports", 
            "Customer information",
            "Order tracking",
            "Financial summaries",
            "Employee data",
            "Natural language database queries"
        ]
        
        return SystemInfoResponse(
            bot_name=config.BOT_NAME,
            available_tables=tables,
            capabilities=capabilities,
            database_type=config.DATABASE_TYPE,
            status="operational"
        )
        
    except Exception as e:
        logger.error(f"Failed to get system info: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/ask", response_model=QuestionResponse)
async def ask_question(request: QuestionRequest):
    """Ask a question to the bot about bakery data"""
    try:
        if not request.question.strip():
            raise HTTPException(status_code=400, detail="Question cannot be empty")
        
        logger.info(f"Processing question: {request.question}")
        
        # Select the appropriate AI service based on configuration
        if config.AI_PROVIDER == "openai":
            ai_service = chatgpt_service
        elif config.AI_PROVIDER == "gemini":
            ai_service = gemini_service
        else:
            raise HTTPException(status_code=500, detail="No valid AI provider configured")
        
        # Process the question through the selected AI service
        result = ai_service.process_question(request.question)
        
        if not result["success"]:
            raise HTTPException(status_code=500, detail=result["error"])
        
        return QuestionResponse(
            question=result["question"],
            sql_query=result.get("sql_query"),
            results=result.get("results"),
            analysis=result["analysis"],
            success=True
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to process question: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.get("/tables")
async def get_tables():
    """Get list of available database tables"""
    try:
        tables = db_manager.get_all_tables()
        return {"tables": tables}
    except Exception as e:
        logger.error(f"Failed to get tables: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/tables/{table_name}/schema")
async def get_table_schema(table_name: str):
    """Get schema information for a specific table"""
    try:
        schema = db_manager.get_table_schema(table_name)
        return schema
    except Exception as e:
        logger.error(f"Failed to get schema for {table_name}: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler"""
    logger.error(f"Unhandled exception: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    ) 