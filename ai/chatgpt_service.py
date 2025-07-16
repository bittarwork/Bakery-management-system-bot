from openai import OpenAI
from typing import Dict, List, Any, Optional
import json
import logging
from config import config
from database.connection import db_manager

# Configure logging
logger = logging.getLogger(__name__)

class ChatGPTService:
    """Service for interacting with ChatGPT API with database context"""
    
    def __init__(self):
        """Initialize ChatGPT service with API key"""
        self.client = OpenAI(api_key=config.OPENAI_API_KEY)
        self.model = config.OPENAI_MODEL
        self.max_tokens = config.MAX_TOKENS
        self.temperature = config.TEMPERATURE
    
    def get_database_context(self) -> str:
        """Get database schema and structure information for context"""
        try:
            tables = db_manager.get_all_tables()
            context_parts = []
            
            for table in tables:
                schema = db_manager.get_table_schema(table)
                context_parts.append(f"Table: {table}")
                if "columns" in schema:
                    for column in schema["columns"]:
                        context_parts.append(f"  - {column['column_name']}: {column['data_type']}")
                context_parts.append("")
            
            return "\n".join(context_parts)
        except Exception as e:
            logger.error(f"Failed to get database context: {str(e)}")
            return "Database context unavailable"
    
    def generate_sql_query(self, user_question: str) -> str:
        """Generate SQL query based on user question and database schema"""
        try:
            db_context = self.get_database_context()
            
            system_prompt = f"""You are a SQL expert for a bakery management system. 
            Based on the database schema below, generate a valid SQL query to answer the user's question.
            
            Database Schema:
            {db_context}
            
            Important Notes:
            - This is a bakery distribution system with users, products, stores, orders, distributors, and payments
            - Products have prices in both EUR and SYP (Syrian Pounds)
            - Orders contain both total amounts and final amounts (after discounts)
            - Users have different roles: admin, manager, distributor, store_owner, accountant
            - Stores are customers that place orders
            - The database name is 'railway'
            
            Rules:
            1. Only generate SQL queries, no explanations
            2. Use proper SQL syntax for {config.DATABASE_TYPE}
            3. Include appropriate WHERE clauses and JOINs when needed
            4. Use LIMIT 10 for large result sets
            5. Return only the SQL query, nothing else
            6. Use table names without database prefix (no 'railway.' prefix)
            """
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_question}
                ],
                max_tokens=self.max_tokens,
                temperature=self.temperature
            )
            
            sql_query = response.choices[0].message.content.strip()
            # Clean up the response to extract only the SQL query
            if sql_query.startswith("```sql"):
                sql_query = sql_query[6:]
            if sql_query.endswith("```"):
                sql_query = sql_query[:-3]
            
            return sql_query.strip()
            
        except Exception as e:
            logger.error(f"Failed to generate SQL query: {str(e)}")
            raise
    
    def analyze_results(self, user_question: str, query_results: List[Dict[str, Any]]) -> str:
        """Analyze query results and provide natural language response"""
        try:
            # Convert results to JSON string for context
            results_json = json.dumps(query_results, indent=2, default=str)
            
            system_prompt = f"""You are a helpful assistant for a bakery distribution management system. 
            Analyze the database query results and provide a clear, helpful response to the user's question.
            
            User Question: {user_question}
            Query Results: {results_json}
            
            Context:
            - This is a bakery distribution system managing products, stores (customers), orders, and deliveries
            - Prices are shown in EUR (Euro) and SYP (Syrian Pounds)
            - Users include distributors, store owners, managers, and administrators
            - Orders go through different statuses: pending, confirmed, prepared, delivered, cancelled
            - Payments can be: pending, partial, paid, overdue
            
            Guidelines:
            1. Provide a natural, conversational response
            2. Summarize the key findings clearly
            3. If no results found, explain why
            4. Use simple language that a bakery manager would understand
            5. Include relevant numbers and statistics when available
            6. Respond in the same language as the user's question
            7. Format currency values appropriately (EUR/SYP)
            8. Explain business insights when relevant
            """
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Please analyze these results and answer: {user_question}"}
                ],
                max_tokens=self.max_tokens,
                temperature=self.temperature
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            logger.error(f"Failed to analyze results: {str(e)}")
            return f"Sorry, I couldn't analyze the results. Error: {str(e)}"
    
    def process_question(self, user_question: str) -> Dict[str, Any]:
        """Process user question: generate SQL, execute it, and analyze results"""
        try:
            # Step 1: Generate SQL query
            logger.info(f"Generating SQL query for: {user_question}")
            sql_query = self.generate_sql_query(user_question)
            
            # Step 2: Execute the query
            logger.info(f"Executing SQL query: {sql_query}")
            query_results = db_manager.execute_query(sql_query)
            
            # Step 3: Analyze results
            logger.info("Analyzing query results")
            analysis = self.analyze_results(user_question, query_results)
            
            return {
                "question": user_question,
                "sql_query": sql_query,
                "results": query_results,
                "analysis": analysis,
                "success": True
            }
            
        except Exception as e:
            logger.error(f"Failed to process question: {str(e)}")
            return {
                "question": user_question,
                "error": str(e),
                "success": False
            }
    
    def get_system_info(self) -> str:
        """Get system information and capabilities"""
        try:
            tables = db_manager.get_all_tables()
            db_context = self.get_database_context()
            
            info = f"""I am {config.BOT_NAME}, your bakery distribution management assistant.

Available Database Tables: {', '.join(tables)}

I can help you with:
- Product catalog and pricing (EUR/SYP)
- Store management and customer information
- Order tracking and delivery status
- Sales analysis and revenue reports
- Distributor performance and assignments
- Payment tracking and financial summaries
- User management and roles
- Business insights and analytics

Just ask me a question in natural language, and I'll query the database and provide you with a helpful analysis.

Database Schema:
{db_context}
"""
            return info
            
        except Exception as e:
            logger.error(f"Failed to get system info: {str(e)}")
            return f"I am {config.BOT_NAME}, your bakery management assistant. I'm having trouble accessing the database right now."

# Global ChatGPT service instance
chatgpt_service = ChatGPTService() 