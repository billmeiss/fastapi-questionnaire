import pytest

class TestQuestionE2E:
    """End-to-end tests for Question CRUD operations"""

    def test_question_crud_lifecycle(self, client):
        """Test complete CRUD lifecycle: Create -> Read -> Update -> Delete"""

        # === CREATE ===
        create_payload = {
            "question_text": "What is the capital of France?",
            "question_type": "text",
            "correct_text": "Paris",
        }

        create_response = client.post("/question/", json=create_payload)
        assert create_response.status_code == 201
        created_question = create_response.json()
        question_id = created_question["id"]

        assert created_question["question_text"] == "What is the capital of France?"
        assert created_question["question_type"] == "text"
        assert created_question["correct_text"] == "Paris"

        # === READ ===
        get_response = client.get(f"/question/{question_id}")
        assert get_response.status_code == 200
        retrieved_question = get_response.json()

        assert retrieved_question["id"] == question_id
        assert retrieved_question["question_text"] == "What is the capital of France?"
        assert retrieved_question["correct_text"] == "Paris"

        # === UPDATE ===
        update_payload = {
            "question_text": "What is the capital of Germany?",
            "question_type": "text",
            "correct_text": "Berlin",
        }

        update_response = client.put(f"/question/{question_id}", json=update_payload)
        assert update_response.status_code == 200
        updated_question = update_response.json()

        assert updated_question["id"] == question_id
        assert updated_question["question_text"] == "What is the capital of Germany?"
        assert updated_question["correct_text"] == "Berlin"

        verify_response = client.get(f"/question/{question_id}")
        assert verify_response.status_code == 200
        verified_question = verify_response.json()
        assert verified_question["correct_text"] == "Berlin"

        # === DELETE ===
        delete_response = client.delete(f"/question/{question_id}")
        assert delete_response.status_code == 200

        get_deleted_response = client.get(f"/question/{question_id}")
        assert get_deleted_response.status_code == 404

    def test_create_text_question(self, client):
        """Test creating a TEXT question"""
        payload = {
            "question_text": "Name a programming language",
            "question_type": "text",
            "correct_text": "Python",
        }

        response = client.post("/question/", json=payload)
        assert response.status_code == 201
        data = response.json()
        assert data["question_type"] == "text"
        assert data["correct_text"] == "Python"

    def test_create_yes_no_question(self, client):
        """Test creating a YES_NO question"""
        payload = {
            "question_text": "Is Python a programming language?",
            "question_type": "yes_no",
            "correct_boolean": True,
        }

        response = client.post("/question/", json=payload)
        assert response.status_code == 201
        data = response.json()
        assert data["question_type"] == "yes_no"
        assert data["correct_boolean"] is True

    def test_create_single_choice_question(self, client):
        """Test creating a SINGLE_CHOICE question"""
        payload = {
            "question_text": "What is 2+2?",
            "question_type": "single_choice",
            "options": ["3", "4", "5"],
            "correct_option_index": 1,
        }

        response = client.post("/question/", json=payload)
        assert response.status_code == 201
        data = response.json()
        assert data["question_type"] == "single_choice"
        assert data["options"] == ["3", "4", "5"]
        assert data["correct_option_index"] == 1

    def test_create_multi_choice_question(self, client):
        """Test creating a MULTI_CHOICE question"""
        payload = {
            "question_text": "Select all prime numbers:",
            "question_type": "multi_choice",
            "options": ["2", "4", "7", "9"],
            "correct_option_indices": [0, 2],
        }

        response = client.post("/question/", json=payload)
        assert response.status_code == 201
        data = response.json()
        assert data["question_type"] == "multi_choice"
        assert data["correct_option_indices"] == [0, 2]

    def test_create_question_validation_error(self, client):
        """Test that invalid question data returns 400"""
        payload = {
            "question_text": "What is Python?",
            "question_type": "text",
            # Missing correct_text
        }

        response = client.post("/question/", json=payload)
        assert response.status_code in [400, 422] 

    def test_get_nonexistent_question(self, client):
        """Test getting a question that doesn't exist"""
        response = client.get("/question/999999")
        assert response.status_code == 404

    def test_update_nonexistent_question(self, client):
        """Test updating a question that doesn't exist"""
        payload = {
            "question_text": "Updated text",
            "question_type": "text",
            "correct_text": "Answer",
        }

        response = client.put("/question/999999", json=payload)
        assert response.status_code == 400

    def test_delete_nonexistent_question(self, client):
        """Test deleting a question that doesn't exist"""
        response = client.delete("/question/999999")
        assert response.status_code == 400

    def test_update_question_type_change_text_to_yes_no(self, client):
        """Test changing question type from TEXT to YES_NO"""
        create_payload = {
            "question_text": "What is Python?",
            "question_type": "text",
            "correct_text": "A programming language",
        }

        create_response = client.post("/question/", json=create_payload)
        assert create_response.status_code == 201
        created_question = create_response.json()
        question_id = created_question["id"]

        update_payload = {
            "question_text": "Is Python a programming language?",
            "question_type": "yes_no",
            "correct_boolean": True,
        }

        update_response = client.put(f"/question/{question_id}", json=update_payload)
        assert update_response.status_code == 200
        updated_question = update_response.json()

        assert updated_question["question_type"] == "yes_no"
        assert updated_question["correct_boolean"] is True
        assert updated_question.get("correct_text") is None 

        get_response = client.get(f"/question/{question_id}")
        assert get_response.status_code == 200
        retrieved = get_response.json()
        assert retrieved["question_type"] == "yes_no"
        assert retrieved["correct_boolean"] is True

    def test_update_question_type_change_yes_no_to_single_choice(self, client):
        """Test changing question type from YES_NO to SINGLE_CHOICE"""
        create_payload = {
            "question_text": "Is the sky blue?",
            "question_type": "yes_no",
            "correct_boolean": True,
        }

        create_response = client.post("/question/", json=create_payload)
        assert create_response.status_code == 201
        created_question = create_response.json()
        question_id = created_question["id"]

        update_payload = {
            "question_text": "What color is the sky?",
            "question_type": "single_choice",
            "options": ["Blue", "Green", "Red"],
            "correct_option_index": 0,
        }

        update_response = client.put(f"/question/{question_id}", json=update_payload)
        assert update_response.status_code == 200
        updated_question = update_response.json()

        assert updated_question["question_type"] == "single_choice"
        assert updated_question["options"] == ["Blue", "Green", "Red"]
        assert updated_question["correct_option_index"] == 0
        assert updated_question.get("correct_boolean") is None 
        assert updated_question.get("following_question_id") is None 

    def test_update_question_type_change_single_choice_to_multi_choice(self, client):
        """Test changing question type from SINGLE_CHOICE to MULTI_CHOICE"""
        create_payload = {
            "question_text": "Pick one color",
            "question_type": "single_choice",
            "options": ["Red", "Blue", "Green"],
            "correct_option_index": 1,
        }

        create_response = client.post("/question/", json=create_payload)
        assert create_response.status_code == 201
        created_question = create_response.json()
        question_id = created_question["id"]

        update_payload = {
            "question_text": "Pick all primary colors",
            "question_type": "multi_choice",
            "options": ["Red", "Blue", "Green", "Yellow"],
            "correct_option_indices": [0, 1, 2],
        }

        update_response = client.put(f"/question/{question_id}", json=update_payload)
        assert update_response.status_code == 200
        updated_question = update_response.json()

        assert updated_question["question_type"] == "multi_choice"
        assert updated_question["correct_option_indices"] == [0, 1, 2]
        assert updated_question.get("correct_option_index") is None  # Should be cleared

    def test_update_question_type_change_multi_choice_to_text(self, client):
        """Test changing question type from MULTI_CHOICE to TEXT"""
        create_payload = {
            "question_text": "Select prime numbers",
            "question_type": "multi_choice",
            "options": ["1", "2", "3", "4"],
            "correct_option_indices": [1, 2],
        }

        create_response = client.post("/question/", json=create_payload)
        assert create_response.status_code == 201
        created_question = create_response.json()
        question_id = created_question["id"]

        update_payload = {
            "question_text": "What are prime numbers?",
            "question_type": "text",
            "correct_text": "Numbers greater than 1 with no positive divisors other than 1 and themselves",
        }

        update_response = client.put(f"/question/{question_id}", json=update_payload)
        assert update_response.status_code == 200
        updated_question = update_response.json()

        assert updated_question["question_type"] == "text"
        assert updated_question["correct_text"] == "Numbers greater than 1 with no positive divisors other than 1 and themselves"
        assert updated_question.get("options") is None
        assert updated_question.get("correct_option_indices") is None

    def test_update_question_with_invalid_type_change(self, client):
        """Test that updating with invalid fields for new type clears them automatically"""
        create_payload = {
            "question_text": "What is 2+2?",
            "question_type": "text",
            "correct_text": "4",
        }

        create_response = client.post("/question/", json=create_payload)
        assert create_response.status_code == 201
        created_question = create_response.json()
        question_id = created_question["id"]

        update_payload = {
            "question_text": "Is 2+2=4?",
            "question_type": "yes_no",
            "correct_boolean": True,
            "correct_text": "This should be cleared",
        }

        update_response = client.put(f"/question/{question_id}", json=update_payload)
        assert update_response.status_code == 200
        updated_question = update_response.json()
        
        assert updated_question["question_type"] == "yes_no"
        assert updated_question["correct_boolean"] is True
        assert updated_question.get("correct_text") is None 
