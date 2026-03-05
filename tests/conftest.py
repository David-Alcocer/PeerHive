"""Pytest configuration for PeerHive tests."""
import sys
import os
from pathlib import Path

# Add the backend directory to the Python path
backend_path = Path(__file__).parent.parent / "backend"
sys.path.insert(0, str(backend_path))

import pytest
from unittest.mock import AsyncMock, MagicMock
from datetime import datetime, timedelta


@pytest.fixture
def mock_db():
    """Fixture for mocking MongoDB database."""
    db = MagicMock()
    db.users = MagicMock()
    db.requests = MagicMock()
    db.sessions = MagicMock()
    return db


@pytest.fixture
def sample_user_data():
    """Fixture for sample user data."""
    return {
        "id": "user123",
        "name": "Test User",
        "email": "test@example.com",
        "password": "hashed_password",
        "role": "student",
        "subjects": [],
        "created_at": datetime.utcnow(),
    }


@pytest.fixture
def sample_request_data():
    """Fixture for sample request data."""
    return {
        "id": "request123",
        "student_id": "user123",
        "subject": "Mathematics",
        "description": "Need help with calculus",
        "status": "pending",
        "created_at": datetime.utcnow(),
    }


@pytest.fixture
def sample_session_data():
    """Fixture for sample session data."""
    return {
        "id": "session123",
        "request_id": "request123",
        "advisor_id": "advisor123",
        "student_id": "user123",
        "scheduled_time": datetime.utcnow() + timedelta(days=1),
        "status": "scheduled",
        "meeting_platform": "teams",
        "meeting_link": "https://teams.example.com/meet123",
    }
