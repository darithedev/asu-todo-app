from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from ..config import settings

# Import all document models
from .models.user import User
from .models.task import Task
from .models.label import Label


class Database:
    """
    Database connection and initialization class.
    Handles MongoDB connection and Beanie ODM setup.
    """
    
    def __init__(self):
        self.client: AsyncIOMotorClient = None
        self.database = None
    
    async def connect(self):
        """
        Initialize database connection and configure Beanie ODM.
        This should be called during application startup.
        """
        try:
            # Get MongoDB URL from settings
            mongodb_url = settings.get_database_url()
            database_name = settings.get_database_name()
            
            # Create Motor client
            self.client = AsyncIOMotorClient(mongodb_url)
            self.database = self.client[database_name]
            
            # Initialize Beanie with all document models
            await init_beanie(
                database=self.database,
                document_models=[User, Task, Label]
            )
            
            print(f"Connected to MongoDB database: {database_name}")
            
        except Exception as e:
            print(f"Failed to connect to MongoDB: {e}")
            raise
    
    async def disconnect(self):
        """
        Close database connection.
        This should be called during application shutdown.
        """
        if self.client:
            self.client.close()
            print("Disconnected from MongoDB")
    
    async def health_check(self) -> bool:
        """
        Check if database connection is healthy.
        Returns True if connection is working, False otherwise.
        """
        try:
            # Ping the database
            await self.database.command("ping")
            return True
        except Exception as e:
            print(f"Database health check failed: {e}")
            return False
    
    async def get_database_info(self) -> dict:
        """
        Get information about the connected database.
        Returns database stats and collection information.
        """
        try:
            # Get database stats
            stats = await self.database.command("dbStats")
            
            # Get collection names
            collections = await self.database.list_collection_names()
            
            return {
                "database_name": self.database.name,
                "collections": collections,
                "stats": {
                    "collections": stats.get("collections", 0),
                    "data_size": stats.get("dataSize", 0),
                    "storage_size": stats.get("storageSize", 0),
                    "indexes": stats.get("indexes", 0)
                }
            }
        except Exception as e:
            print(f"Failed to get database info: {e}")
            return {}


# Global database instance
database = Database()


async def init_db():
    """
    Initialize database connection.
    This function should be called during FastAPI application startup.
    """
    await database.connect()


async def close_db():
    """
    Close database connection.
    This function should be called during FastAPI application shutdown.
    """
    await database.disconnect()


async def get_db():
    """
    Get database instance.
    This can be used as a dependency in FastAPI routes.
    """
    return database.database


# Database configuration constants
class DatabaseConfig:
    """Database configuration constants"""
    
    # Connection settings
    CONNECTION_TIMEOUT = 10000  # 10 seconds
    SERVER_SELECTION_TIMEOUT = 5000  # 5 seconds
    
    # Index settings
    CREATE_INDEXES_ON_STARTUP = True
    
    # Collection settings
    DEFAULT_COLLECTION_OPTIONS = {
        "capped": False,
        "size": None,
        "max": None
    }
