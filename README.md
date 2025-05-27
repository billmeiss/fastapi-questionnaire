# Backend Challenge

A FastAPI-based backend service for managing questions and questionnaires.

## Quick Start

Run the application using Docker Compose:

```bash
docker-compose up --build
```

The API will be available at `http://localhost:8001`

## API Documentation

Once running, access:
- Swagger UI: `http://localhost:8001/docs`
- ReDoc: `http://localhost:8001/redoc`

## Question CRUD Endpoints

All question endpoints are prefixed with `/question`:

### Create Question
**POST** `/question/`

Creates a new question. Required fields vary by question type (see [Question Types](#question-types) below).

**Example Request:**
```json
{
  "question_text": "What is the capital of France?",
  "question_type": "text",
  "correct_text": "Paris"
}
```

**Response:** `201 Created` with the created question object.

### Get Question
**GET** `/question/{question_id}`

Retrieves a specific question by its ID.

**Response:** `200 OK` with the question object, or `404 Not Found` if the question doesn't exist.

### Update Question
**PUT** `/question/{question_id}`

Updates an existing question. All required fields for the question type must be provided.

**Example Request:**
```json
{
  "question_text": "What is the capital of Germany?",
  "question_type": "text",
  "correct_text": "Berlin"
}
```

**Response:** `200 OK` with the updated question object.

### Delete Question
**DELETE** `/question/{question_id}`

Deletes a question by its ID.

**Response:** `200 OK` with a success message.

## Question Types

The API supports four question types, each with specific requirements and validation rules.

Validation is enforced so there is no need to worry about providing fields that are not allowed for the question type.

### 1. TEXT
Free-text answer questions.

**Required Fields:**
- `question_text` (string, 1-500 characters)
- `question_type`: `"text"`
- `correct_text` (string) - The correct answer

**Example:**
```json
{
  "question_text": "What is the capital of France?",
  "question_type": "text",
  "correct_text": "Paris"
}
```

**Caveats:**
- `question_text` must be between 1 and 500 characters
- Only `correct_text` field is allowed (other type-specific fields will be rejected)

### 2. YES_NO
Boolean true/false questions.

**Required Fields:**
- `question_text` (string, 1-500 characters)
- `question_type`: `"yes_no"`
- `correct_boolean` (boolean) - The correct answer

**Optional Fields:**
- `following_question_id` (integer) - ID of parent question for conditional logic

**Example:**
```json
{
  "question_text": "Is Python a programming language?",
  "question_type": "yes_no",
  "correct_boolean": true,
  "following_question_id": 1
}
```

**Caveats:**
- Only `correct_boolean` and `following_question_id` fields are allowed
- Cannot use fields from other question types (e.g., `correct_text`, `options`)

### 3. SINGLE_CHOICE
Multiple choice questions with a single correct answer.

**Required Fields:**
- `question_text` (string, 1-500 characters)
- `question_type`: `"single_choice"`
- `options` (array of strings) - List of answer options (minimum 2)
- `correct_option_index` (integer) - Zero-based index of the correct option

**Example:**
```json
{
  "question_text": "What is 2 + 2?",
  "question_type": "single_choice",
  "options": ["3", "4", "5", "6"],
  "correct_option_index": 1
}
```

**Caveats:**
- Must provide at least 2 options
- `correct_option_index` must be a valid zero-based index (0 to `len(options) - 1`)
- Only `options` and `correct_option_index` fields are allowed
- Cannot use `correct_option_indices` (that's for MULTI_CHOICE)

### 4. MULTI_CHOICE
Multiple choice questions with multiple correct answers.

**Required Fields:**
- `question_text` (string, 1-500 characters)
- `question_type`: `"multi_choice"`
- `options` (array of strings) - List of answer options (minimum 3)
- `correct_option_indices` (array of integers) - Zero-based indices of all correct options (minimum 2)

**Example:**
```json
{
  "question_text": "Select all prime numbers:",
  "question_type": "multi_choice",
  "options": ["2", "4", "7", "9", "11"],
  "correct_option_indices": [0, 2, 4]
}
```

**Caveats:**
- Must provide at least 3 options
- Must provide at least 2 correct option indices
- All indices in `correct_option_indices` must be unique
- All indices must be valid zero-based indices (0 to `len(options) - 1`)
- Only `options` and `correct_option_indices` fields are allowed
- Cannot use `correct_option_index` (that's for SINGLE_CHOICE)

## Common Validation Rules

- **Question Text:** Must be between 1 and 500 characters for all question types
- **Type-Specific Fields:** Only fields relevant to the question type are allowed. Providing fields from other types will result in a validation error
- **Required Fields:** All required fields for the selected question type must be provided
- **Type Changes:** When updating a question and changing its type, you must provide all required fields for the new type. Fields from the old type will be cleared automatically

## Development

- Format code: `black .`
- Run tests: `pytest`

## Project Structure

```
.
├── app/
│   ├── __init__.py
│   ├── api.py         # FastAPI application and routes
│   └── db.py          # Database configuration
├── requirements.txt   # Python dependencies
├── Dockerfile        # Container configuration
└── docker-compose.yml # Docker services configuration
```
# fastapi-questionnaire
