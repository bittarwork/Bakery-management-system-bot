import sqlalchemy
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
import pymongo
from typing import Dict, List, Any, Optional
import logging
from config import config

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DatabaseManager:
    """Database connection manager supporting multiple database types"""
    
    def __init__(self):
        self.engine = None
        self.session = None
        self.client = None
        self.db = None
        self.connect()
    
    def connect(self):
        """Establish database connection based on configuration"""
        try:
            if config.DATABASE_TYPE.lower() == "postgresql":
                self._connect_postgresql()
            elif config.DATABASE_TYPE.lower() == "mysql":
                self._connect_mysql()
            elif config.DATABASE_TYPE.lower() == "mongodb":
                self._connect_mongodb()
            else:
                raise ValueError(f"Unsupported database type: {config.DATABASE_TYPE}")
            
            logger.info(f"Successfully connected to {config.DATABASE_TYPE} database")
        except Exception as e:
            logger.error(f"Failed to connect to database: {str(e)}")
            raise
    
    def _connect_postgresql(self):
        """Connect to PostgreSQL database"""
        self.engine = create_engine(config.DATABASE_URL)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
    
    def _connect_mysql(self):
        """Connect to MySQL database"""
        self.engine = create_engine(config.DATABASE_URL)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
    
    def _connect_mongodb(self):
        """Connect to MongoDB database"""
        self.client = pymongo.MongoClient(config.DATABASE_URL)
        # Extract database name from URL or use default
        db_name = config.DATABASE_URL.split('/')[-1].split('?')[0]
        self.db = self.client[db_name]
    
    def execute_query(self, query: str) -> List[Dict[str, Any]]:
        """Execute SQL query and return results"""
        try:
            if config.DATABASE_TYPE.lower() in ["postgresql", "mysql"]:
                return self._execute_sql_query(query)
            elif config.DATABASE_TYPE.lower() == "mongodb":
                return self._execute_mongo_query(query)
        except Exception as e:
            logger.error(f"Query execution failed: {str(e)}")
            raise
    
    def _execute_sql_query(self, query: str) -> List[Dict[str, Any]]:
        """Execute SQL query on relational databases"""
        try:
            result = self.session.execute(text(query))
            if result.returns_rows:
                columns = result.keys()
                return [dict(zip(columns, row)) for row in result.fetchall()]
            else:
                self.session.commit()
                return [{"message": "Query executed successfully", "affected_rows": result.rowcount}]
        except SQLAlchemyError as e:
            self.session.rollback()
            raise
    
    def _execute_mongo_query(self, query: str) -> List[Dict[str, Any]]:
        """Execute MongoDB query (simplified implementation)"""
        # This is a simplified implementation
        # In a real scenario, you might want to parse the query string
        # and convert it to MongoDB operations
        try:
            # For now, we'll return a sample structure
            # You can extend this based on your specific MongoDB queries
            return [{"message": "MongoDB query executed", "query": query}]
        except Exception as e:
            raise
    
    def get_table_schema(self, table_name: str) -> Dict[str, Any]:
        """Get table schema information"""
        try:
            if config.DATABASE_TYPE.lower() in ["postgresql", "mysql"]:
                return self._get_sql_table_schema(table_name)
            elif config.DATABASE_TYPE.lower() == "mongodb":
                return self._get_mongo_collection_schema(table_name)
        except Exception as e:
            logger.error(f"Failed to get schema for {table_name}: {str(e)}")
            raise
    
    def _get_sql_table_schema(self, table_name: str) -> Dict[str, Any]:
        """Get SQL table schema"""
        try:
            if config.DATABASE_TYPE.lower() == "mysql":
                query = f"DESCRIBE {table_name}"
            else:  # PostgreSQL
                query = f"""
                SELECT column_name, data_type, is_nullable, column_default
                FROM information_schema.columns
                WHERE table_name = '{table_name}'
                ORDER BY ordinal_position
                """
            
            result = self.session.execute(text(query))
            
            if config.DATABASE_TYPE.lower() == "mysql":
                # MySQL DESCRIBE returns: Field, Type, Null, Key, Default, Extra
                columns = []
                for row in result.fetchall():
                    columns.append({
                        "column_name": row[0],
                        "data_type": row[1],
                        "is_nullable": row[2],
                        "column_default": row[4]
                    })
            else:
                # PostgreSQL
                columns = result.keys()
                columns = [dict(zip(columns, row)) for row in result.fetchall()]
            
            return {"table_name": table_name, "columns": columns}
        except Exception as e:
            logger.error(f"Error getting schema for {table_name}: {str(e)}")
            return {"table_name": table_name, "columns": []}
    
    def _get_mongo_collection_schema(self, collection_name: str) -> Dict[str, Any]:
        """Get MongoDB collection schema (simplified)"""
        # This is a simplified implementation
        # In a real scenario, you might analyze sample documents
        return {"collection_name": collection_name, "type": "document"}
    
    def get_all_tables(self) -> List[str]:
        """Get list of all tables/collections"""
        try:
            if config.DATABASE_TYPE.lower() in ["postgresql", "mysql"]:
                return self._get_sql_tables()
            elif config.DATABASE_TYPE.lower() == "mongodb":
                return self._get_mongo_collections()
        except Exception as e:
            logger.error(f"Failed to get tables: {str(e)}")
            raise
    
    def _get_sql_tables(self) -> List[str]:
        """Get SQL tables list"""
        if config.DATABASE_TYPE.lower() == "postgresql":
            query = """
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
            """
        else:  # MySQL
            query = "SHOW TABLES"
        
        result = self.session.execute(text(query))
        return [row[0] for row in result.fetchall()]
    
    def _get_mongo_collections(self) -> List[str]:
        """Get MongoDB collections list"""
        return self.db.list_collection_names()
    
    def close(self):
        """Close database connections"""
        if self.session:
            self.session.close()
        if self.engine:
            self.engine.dispose()
        if self.client:
            self.client.close()

# Global database manager instance
db_manager = DatabaseManager() 