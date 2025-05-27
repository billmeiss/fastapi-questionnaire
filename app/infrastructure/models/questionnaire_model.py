from sqlalchemy import Column, Integer, ForeignKey, String, Boolean, ARRAY, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db import Base
from sqlalchemy import Table, Column, Integer, ForeignKey, UniqueConstraint

# Did not implement this within the API since I wanted to focus on CRUD operations for the question entity.
# This is how I would implement the relationship in PROD

# questionnaire_questions = Table(
#     'questionnaire_questions',
#     Base.metadata,
#     Column('id', Integer, primary_key=True, autoincrement=True),
#     Column('questionnaire_id', Integer, ForeignKey('questionnaires.id', ondelete='CASCADE'), nullable=False),
#     Column('question_id', Integer, ForeignKey('questions.id', ondelete='CASCADE'), nullable=False),
#     Column('order', Integer, nullable=False),  # Preserve order
#     UniqueConstraint('questionnaire_id', 'question_id', name='uq_questionnaire_question')
# )

class QuestionnaireModel(Base):
    """SQLAlchemy model for the Questionnaire entity"""

    __tablename__ = "questionnaires"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    description = Column(String(500), nullable=True)
    # This is a simpler implementation for a relationship to questions, although having a separate table for the many-to-many relationship (like in the comments of this file) would be more robust.
    question_ids = Column(ARRAY(Integer), nullable=False, default=list)
    created_at = Column(DateTime, nullable=False, default=datetime.now)
    updated_at = Column(DateTime, nullable=False, default=datetime.now)

    # questions = relationship(
    #     "QuestionModel", 
    #     secondary=questionnaire_questions, 
    #     order_by="questionnaire_questions.c.order",
    #     backref="questionnaires"
    # )