from sqlalchemy import Column, Integer, ForeignKey, String, Boolean, ARRAY, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db import Base


class QuestionModel(Base):
    """SQLAlchemy model for the Question entity"""

    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    question_text = Column(String(500), nullable=False)
    question_type = Column(String(50), nullable=False)
    options = Column(ARRAY(String(255)), nullable=True)
    correct_text = Column(String(500), nullable=True)
    correct_boolean = Column(Boolean, nullable=True)
    correct_option_index = Column(Integer, nullable=True)
    correct_option_indices = Column(ARRAY(Integer), nullable=True)
    following_question_id = Column(Integer, ForeignKey("questions.id"), nullable=True)
    created_at = Column(DateTime, nullable=False, default=datetime.now)
    updated_at = Column(DateTime, nullable=False, default=datetime.now)
