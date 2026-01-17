from sqlmodel import create_engine
from sqlalchemy.pool import QueuePool
import os
from dotenv import load_dotenv

load_dotenv()

# Get database URL from environment variable
DATABASE_URL = os.getenv("DATABASE_URL", os.getenv("NEON_DATABASE_URL"))

if not DATABASE_URL:
    raise ValueError("DATABASE_URL or NEON_DATABASE_URL environment variable is required")

def get_database_url():
    """Return the database URL for use by Alembic."""
    return DATABASE_URL

# Create engine with appropriate settings for PostgreSQL/Neon
engine = create_engine(
    DATABASE_URL,
    poolclass=QueuePool,
    pool_size=5,
    max_overflow=10,
    pool_pre_ping=True,
    pool_recycle=300,
)