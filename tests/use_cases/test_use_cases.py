"""Tests for use cases using mocks."""
import pytest
from unittest.mock import AsyncMock, MagicMock
from datetime import datetime, timedelta


class TestCreateUserUseCase:
    """Tests for CreateUserUseCase."""

    @pytest.mark.asyncio
    async def test_create_user_success(self):
        """Test successful user creation."""
        from backend.app.application.use_cases.create_user import CreateUserUseCase
        
        # Mock dependencies
        mock_repo = AsyncMock()
        mock_repo.get_by_email.return_value = None
        mock_repo.create.return_value = {
            "id": "new_user_id",
            "name": "Test User",
            "email": "test@example.com",
            "role": "student",
        }
        
        use_case = CreateUserUseCase(mock_repo)
        
        result = await use_case.execute(
            name="Test User",
            email="test@example.com",
            password="password123",
            role="student"
        )
        
        assert result["email"] == "test@example.com"
        mock_repo.create.assert_called_once()

    @pytest.mark.asyncio
    async def test_create_user_duplicate_email(self):
        """Test user creation with duplicate email."""
        from backend.app.application.use_cases.create_user import CreateUserUseCase
        
        mock_repo = AsyncMock()
        mock_repo.get_by_email.return_value = {"email": "test@example.com"}
        
        use_case = CreateUserUseCase(mock_repo)
        
        with pytest.raises(ValueError, match="Email already registered"):
            await use_case.execute(
                name="Test User",
                email="test@example.com",
                password="password123",
                role="student"
            )


class TestGetUserUseCase:
    """Tests for GetUserUseCase."""

    @pytest.mark.asyncio
    async def test_get_user_by_id(self):
        """Test getting user by ID."""
        from backend.app.application.use_cases.get_user import GetUserUseCase
        
        mock_repo = AsyncMock()
        mock_repo.get_by_id.return_value = {
            "id": "user123",
            "name": "Test User",
            "email": "test@example.com",
        }
        
        use_case = GetUserUseCase(mock_repo)
        
        result = await use_case.execute(user_id="user123")
        
        assert result["id"] == "user123"
        mock_repo.get_by_id.assert_called_once_with("user123")

    @pytest.mark.asyncio
    async def test_get_user_not_found(self):
        """Test getting non-existent user."""
        from backend.app.application.use_cases.get_user import GetUserUseCase
        
        mock_repo = AsyncMock()
        mock_repo.get_by_id.return_value = None
        
        use_case = GetUserUseCase(mock_repo)
        
        result = await use_case.execute(user_id="nonexistent")
        
        assert result is None


class TestCreateRequestUseCase:
    """Tests for CreateRequestUseCase."""

    @pytest.mark.asyncio
    async def test_create_request_success(self):
        """Test successful request creation."""
        from backend.app.application.use_cases.create_request import CreateRequestUseCase
        
        mock_repo = AsyncMock()
        mock_repo.create.return_value = {
            "id": "request123",
            "student_id": "user123",
            "subject": "Mathematics",
            "description": "Need help",
            "status": "pending",
        }
        
        use_case = CreateRequestUseCase(mock_repo)
        
        result = await use_case.execute(
            student_id="user123",
            subject="Mathematics",
            description="Need help"
        )
        
        assert result["subject"] == "Mathematics"
        assert result["status"] == "pending"
        mock_repo.create.assert_called_once()


class TestAssignRequestUseCase:
    """Tests for AssignRequestUseCase."""

    @pytest.mark.asyncio
    async def test_assign_request_success(self):
        """Test successful request assignment."""
        from backend.app.application.use_cases.assign_request import AssignRequestUseCase
        
        mock_repo = AsyncMock()
        mock_repo.get_by_id.return_value = {
            "id": "request123",
            "status": "pending",
            "student_id": "user123",
        }
        mock_repo.update.return_value = {
            "id": "request123",
            "status": "assigned",
            "advisor_id": "advisor123",
        }
        
        use_case = AssignRequestUseCase(mock_repo)
        
        result = await use_case.execute(
            request_id="request123",
            advisor_id="advisor123"
        )
        
        assert result["status"] == "assigned"
        mock_repo.update.assert_called_once()

    @pytest.mark.asyncio
    async def test_assign_already_assigned_request(self):
        """Test assigning already assigned request."""
        from backend.app.application.use_cases.assign_request import AssignRequestUseCase
        
        mock_repo = AsyncMock()
        mock_repo.get_by_id.return_value = {
            "id": "request123",
            "status": "assigned",
        }
        
        use_case = AssignRequestUseCase(mock_repo)
        
        with pytest.raises(ValueError, match="Request already assigned"):
            await use_case.execute(
                request_id="request123",
                advisor_id="advisor123"
            )
