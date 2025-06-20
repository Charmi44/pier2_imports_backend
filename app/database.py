from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Define the path to the SQLite database file
SQLALCHEMY_DATABASE_URL = "sqlite:///./pier2.db"

# Create a SQLAlchemy engine for SQLite
# 'check_same_thread=False' allows the database connection to be shared across threads
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

# autocommit=False ensures changes must be explicitly committed
# autoflush=False prevents automatic flushing before queries
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    
    """
    Dependency that provides a SQLAlchemy database session.
    
    Yields:
        db (Session): A new SQLAlchemy session.
        
    This function ensures that the database session is properly closed 
    after the request lifecycle end
    
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() # always close the session to avoid DB connection leaks
