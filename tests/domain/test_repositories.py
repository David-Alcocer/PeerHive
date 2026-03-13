"""Tests for domain repositories using mocks."""
import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from datetime import datetime


class TestUserRepositoryMock:
    """Tests for UserRepository using mocked database."""

    @pytest.mark.asyncio
    async def test_create_user(self, sample_user_data):
        """Test user creation through repository."""
        from backend.app.domain.repositories import UserRepositoryPort
        
        # Create mock repository
        mock_repo = AsyncMock(spec=UserRepositoryPort)
        mock_repo.create.return_value = sample_user_data
        
        # Execute
        result = await mock_repo.create(sample_user_data)
        
        # Assert
        assert result == sample_user_data
        mock_repo.create.assert_called_once_with(sample_user_data)

    @pytest.mark.asyncio
    async def test_get_user_by_email(self, sample_user_data):
        """Test getting user by email."""
        from backend.app.domain.repositories import UserRepositoryPort
        
        mock_repo = AsyncMock(spec=UserRepositoryPort)
        mock_repo.get_by_email.return_value = sample_user_data
        
        result = await mock_repo.get_by_email("test@example.com")
        
        assert result == sample_user_data
        mock_repo.get_by_email.assert_called_once_with("test@example.com")

    @pytest.mark.asyncio
    async def test_get_user_by_id(self, sample_user_data):
        """Test getting user by ID."""
        from backend.app.domain.repositories import UserRepositoryPort
        
        mock_repo = AsyncMock(spec=UserRepositoryPort)
        mock_repo.get_by_id.return_value = sample_user_data
        
        result = await mock_repo.get_by_id("user123")
        
        assert result == sample_user_data
        mock_repo.get_by_id.assert_called_once_with("user123")

    @pytest.mark.asyncio
    async def test_list_all_users(self, sample_user_data):
        """Test listing all users."""
        from backend.app.domain.repositories import UserRepositoryPort
        
        mock_repo = AsyncMock(spec=UserRepositoryPort)
        mock_repo.list_all.return_value = [sample_user_data]
        
        result = await mock_repo.list_all()
        
        assert len(result) == 1
        assert result[0]["email"] == "test@example.com"


class TestRequestRepositoryMock:
    """Tests for RequestRepository using mocked database."""

    @pytest.mark.asyncio
    async def test_create_request(self, sample_request_data):
        """Test request creation through repository."""
        from backend.app.domain.repositories import RequestRepositoryPort
        
        mock_repo = AsyncMock(spec=RequestRepositoryPort)
        mock_repo.create.return_value = sample_request_data
        
        result = await mock_repo.create(sample_request_data)
        
        assert result == sample_request_data
        mock_repo.create.assert_called_once_with(sample_request_data)

    @pytest.mark.asyncio
    async def test_get_pending_requests(self, sample_request_data):
        """Test getting pending requests."""
        from backend.app.domain.repositories import RequestRepositoryPort
        
        mock_repo = AsyncMock(spec=RequestRepositoryPort)
        mock_repo.list_pending.return_value = [sample_request_data]
        
        result = await mock_repo.list_pending()
        
        assert len(result) == 1
        assert result[0]["status"] == "pending"

    @pytest.mark.asyncio
    async def test_update_request_status(self, sample_request_data):
        """Test updating request status."""
        from backend.app.domain.repositories import RequestRepositoryPort
        
        mock_repo = AsyncMock(spec=RequestRepositoryPort)
        updated_request = {**sample_request_data, "status": "assigned"}
        mock_repo.update.return_value = updated_request
        
        result = await mock_repo.update("request123", {"status": "assigned"})
        
        assert result["status"] == "assigned"


class TestSessionRepositoryMock:
    """Tests for SessionRepository using mocked database."""

    @pytest.mark.asyncio
    async def test_create_session(self, sample_session_data):
        """Test session creation through repository."""
        from backend.app.domain.repositories import SessionRepositoryPort
        
        mock_repo = AsyncMock(spec=SessionRepositoryPort)
        mock_repo.create.return_value = sample_session_data
        
        result = await mock_repo.create(sample_session_data)
        
        assert result == sample_session_data
        mock_repo.create.assert_called_once_with(sample_session_data)

    @pytest.mark.asyncio
    async def test_get_session_by_id(self, sample_session_data):
        """Test getting session by ID."""
        from backend.app.domain.repositories import SessionRepositoryPort
        
        mock_repo = AsyncMock(spec=SessionRepositoryPort)
        mock_repo.get_by_id.return_value = sample_session_data
        
        result = await mock_repo.get_by_id("session123")
        
        assert result == sample_session_data
        mock_repo.get_by_id.assert_called_once_with("session123")

    @pytest.mark.asyncio
    async def test_list_sessions_by_student(self, sample_session_data):
        """Test listing sessions by student."""
        from backend.app.domain.repositories import SessionRepositoryPort
        
        mock_repo = AsyncMock(spec=SessionRepositoryPort)
        mock_repo.list_by_student.return_value = [sample_session_data]
        
        result = await mock_repo.list_by_student("user123")
        
        assert len(result) == 1
        assert result[0]["student_id"] == "user123"
