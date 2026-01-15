"""Initialize database with pgvector extension."""

from db.connection import init_db

if __name__ == "__main__":
    print("Initializing database...")
    init_db()
    print("Database initialized successfully!")
