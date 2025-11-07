import datetime
from typing import Dict, Set, List, Optional
from enum import Enum

## We could have either declared different entities for each question type or use a single class with a question_type field.
## I went with the latter option to keep the database schema simple, although this means validation logic can be quite overwhelming to make sure only fields relevant to the question type are used.

MAX_QUESTION_TEXT_LENGTH = 500
MIN_QUESTION_TEXT_LENGTH = 1
MIN_SINGLE_CHOICE_OPTIONS = 2
MIN_MULTI_CHOICE_OPTIONS = 3
MIN_MULTI_CHOICE_CORRECT_ANSWERS = 2

class QuestionType(Enum):
    TEXT = "text"
    YES_NO = "yes_no"
    SINGLE_CHOICE = "single_choice"
    MULTI_CHOICE = "multi_choice"


class Question:
    """Domain entity with type-specific fields"""

    COMMON_FIELDS = {"question_text", "question_type", "id"}

    TYPE_SPECIFIC_FIELDS: Dict[QuestionType, Dict[str, Set[str]]] = {
        QuestionType.TEXT: {"required": {"correct_text"}, "optional": set()},
        QuestionType.YES_NO: {
            "required": {"correct_boolean"},
            "optional": {"following_question_id"},
        },
        QuestionType.SINGLE_CHOICE: {
            "required": {"options", "correct_option_index"},
            "optional": set(),
        },
        QuestionType.MULTI_CHOICE: {
            "required": {"options", "correct_option_indices"},
            "optional": set(),
        },
    }

    ALL_TYPE_SPECIFIC_FIELDS = set().union(
        *[
            rules.get("required", set()) | rules.get("optional", set())
            for rules in TYPE_SPECIFIC_FIELDS.values()
        ]
    )

    def __init__(
        self,
        id: Optional[int],
        question_text: str,
        question_type: QuestionType,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
        # === Choice-based fields ===
        options: Optional[List[str]] = None,  # SINGLE_CHOICE, MULTI_CHOICE
        # === Type-specific answer fields ===
        correct_text: Optional[str] = None,  # TEXT only
        correct_boolean: Optional[bool] = None,  # YES_NO only
        correct_option_index: Optional[int] = None,  # SINGLE_CHOICE only
        correct_option_indices: Optional[List[int]] = None,  # MULTI_CHOICE only
        # === Conditional logic (YES_NO only) ===
        following_question_id: Optional[
            int
        ] = None,  
    ):
        self.id = id
        self.question_text = question_text
        self.question_type = question_type
        self.options = options
        self.correct_text = correct_text
        self.correct_boolean = correct_boolean
        self.correct_option_index = correct_option_index
        self.correct_option_indices = correct_option_indices
        self.following_question_id = following_question_id
        self.created_at = created_at
        self.updated_at = updated_at

        self._validate()

    def _validate(self):
        """Validate question based on type"""
        if not self.question_text or len(self.question_text) < MIN_QUESTION_TEXT_LENGTH or len(self.question_text) > MAX_QUESTION_TEXT_LENGTH:
            raise ValueError("Question text must be 1-500 characters")

        if self.question_type == QuestionType.TEXT:
            self.validate_text_question()

        elif self.question_type == QuestionType.YES_NO:
            self.validate_yes_no_question()

        elif self.question_type == QuestionType.SINGLE_CHOICE:
            self.validate_single_choice_question()

        elif self.question_type == QuestionType.MULTI_CHOICE:
            self.validate_multi_choice_question()

    def _validate_fields_for_type(self):
        """Validates only relevant fields are used for the question type"""
        rules = self.TYPE_SPECIFIC_FIELDS.get(self.question_type)
        if not rules:
            raise ValueError(f"Unknown question type: {self.question_type}")

        provided_fields = self._get_provided_type_specific_fields()

        allowed_fields = rules["required"] | rules["optional"] | self.COMMON_FIELDS

        missing = rules["required"] - provided_fields
        if missing:
            raise ValueError(
                f"{self.question_type.value} questions require: {', '.join(sorted(missing))}"
            )

        invalid = provided_fields - allowed_fields
        if invalid:
            raise ValueError(
                f"{self.question_type.value} questions cannot use: {', '.join(sorted(invalid))}. "
                f"These fields belong to other question types."
            )

    def validate_text_question(self):
        return self._validate_fields_for_type()

    def validate_yes_no_question(self):
        return self._validate_fields_for_type()

    def validate_single_choice_question(self):
        if not self.options or len(self.options) < MIN_SINGLE_CHOICE_OPTIONS:
            raise ValueError("SINGLE_CHOICE requires at least 2 options")
        if not (0 <= self.correct_option_index < len(self.options)):
            raise ValueError(
                f"correct_option_index {self.correct_option_index} out of range"
            )
        return self._validate_fields_for_type()

    def validate_multi_choice_question(self):
        if not self.options or len(self.options) < MIN_MULTI_CHOICE_OPTIONS:
            raise ValueError("MULTI_CHOICE requires at least 3 options")
        if not self.correct_option_indices or len(self.correct_option_indices) < 2:
            raise ValueError(
                "MULTI_CHOICE requires at least two correct_option_indices"
            )
        for idx in self.correct_option_indices:
            if not (0 <= idx < len(self.options)):
                raise ValueError(f"correct_option_indices {idx} out of range")
        if len(self.correct_option_indices) != len(set(self.correct_option_indices)):
            raise ValueError("correct_option_indices must be unique")
        return self._validate_fields_for_type()

    def _get_provided_type_specific_fields(self) -> Set[str]:
        """Returns ALL type-specific fields that are provided (not None)"""
        return {
            field
            for field in self.ALL_TYPE_SPECIFIC_FIELDS
            if field in self.__dict__ and getattr(self, field) is not None
        }

    def update(
        self,
        question_text: str,
        question_type: QuestionType,
        options: Optional[List[str]] = None,
        correct_text: Optional[str] = None,
        correct_boolean: Optional[bool] = None,
        correct_option_index: Optional[int] = None,
        correct_option_indices: Optional[List[int]] = None,
        following_question_id: Optional[int] = None,
    ):
        original_values = self.__dict__.copy()
        try:
            self.question_text = question_text
            self.question_type = question_type
            self.options = options
            self.correct_text = correct_text
            self.correct_boolean = correct_boolean
            self.correct_option_index = correct_option_index
            self.correct_option_indices = correct_option_indices
            self.following_question_id = following_question_id
            self._validate()
            return self
        except Exception as e:
            for key, value in original_values.items():
                if key in self.__dict__:
                    setattr(self, key, value)
            raise e
        return self
