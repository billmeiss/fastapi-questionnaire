from typing import List, Optional
from datetime import datetime


MAX_TITLE_LENGTH = 255
MIN_TITLE_LENGTH = 1
MAX_DESCRIPTION_LENGTH = 500

class Questionnaire:
    """Domain entity for a questionnaire - simple ordered list of question IDs"""

    def __init__(
        self,
        id: Optional[int],
        title: str,
        description: Optional[str] = None,
        question_ids: Optional[List[int]] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
    ):
        self.id = id
        self.title = title
        self.description = description
        self.question_ids = question_ids or []
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()

        self._validate()

    def _validate(self):
        """Validate questionnaire"""
        self._validate_title()
        self._validate_description()
        self._validate_question_ids()

    def _validate_title(self):
        if not self.title or len(self.title) < MIN_TITLE_LENGTH or len(self.title) > MAX_TITLE_LENGTH:
            raise ValueError("Title must be 1-255 characters")

    def _validate_description(self):
        if self.description and len(self.description) > MAX_DESCRIPTION_LENGTH:
            raise ValueError("Description must not exceed 500 characters")

    def _validate_question_ids(self):
        """Ensure no duplicate question IDs"""
        if not self.question_ids:
            return

        if len(self.question_ids) != len(set(self.question_ids)):
            raise ValueError("Duplicate question IDs are not allowed")
