#!/usr/bin/env python3
"""
Database initialization script
Creates all tables from SQLAlchemy models
"""

from app.db import engine, Base
from app.infrastructure.models.question_model import QuestionModel
from app.infrastructure.models.questionnaire_model import QuestionnaireModel

def init_database():
    """Drop all existing tables and create fresh ones"""
    print("Dropping existing tables...")
    Base.metadata.drop_all(bind=engine)
    print("✅ Tables dropped successfully!")
    
    print("\nCreating database tables...")
    Base.metadata.create_all(bind=engine)
    
    print("✅ All tables created successfully!")
    print("\nCreated tables:")
    for table_name in Base.metadata.tables.keys():
        print(f"  - {table_name}")

if __name__ == "__main__":
    init_database()
