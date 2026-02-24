from pydantic import BaseModel, Field, EmailStr, ConfigDict
from typing import Optional, List, Any, Dict
from datetime import datetime
from enum import Enum
from bson import ObjectId
from typing_extensions import Annotated

# Helper functions for ObjectId handling
class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v, handler):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)

    @classmethod
    def __get_pydantic_json_schema__(cls, field_schema, handler):
        field_schema.update(type="string")

# Base model for common config
class MongoBaseModel(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str}
    )

# Enums
class RoleEnum(str, Enum):
    ADMIN = "admin"
    ADVISOR = "advisor"
    STUDENT = "student"

class RequestStatusEnum(str, Enum):
    PENDING = "pending"
    TAKEN = "taken"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

class MeetingPlatformEnum(str, Enum):
    TEAMS = "teams"
    ZOOM = "zoom"
    PRESENCIAL = "presencial"

class SessionStatusEnum(str, Enum):
    PENDING_APPROVAL = "pending_approval"
    APPROVED = "approved"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    REQUIRES_REVIEW = "requires_review"
    CANCELLED = "cancelled"

class EvidenceTypeEnum(str, Enum):
    TEAMS_API = "teams_api"
    MANUAL_UPLOAD = "manual_upload"
    ADMIN_OVERRIDE = "admin_override"

# Sub-models / Embedded
class AttendanceRecord(BaseModel):
    userId: PyObjectId
    joinedAt: datetime
    leftAt: datetime
    durationMinutes: int

class Verification(BaseModel):
    wasHeld: bool
    attendance: List[AttendanceRecord] = []
    durationMinutes: Optional[int] = None
    actualStartTime: Optional[datetime] = None
    actualEndTime: Optional[datetime] = None
    evidenceType: EvidenceTypeEnum
    manualEvidence: Optional[Dict[str, Any]] = None # Screenshots, files
    verifiedBy: Optional[PyObjectId] = None # Admin ID
    verifiedAt: Optional[datetime] = None
    notes: Optional[str] = None

class Attachment(BaseModel):
    type: str # image, document
    url: str
    name: str

class Message(BaseModel):
    fromUserId: PyObjectId
    content: Optional[str] = None
    attachment: Optional[Attachment] = None
    sentAt: datetime = Field(default_factory=datetime.now)
    isRead: bool = False

# Main Models
class User(MongoBaseModel):
    name: str
    email: EmailStr
    microsoftId: str
    role: RoleEnum
    # --- Tus adiciones de Admin ---
    is_verified: bool = False  
    id_card_url: Optional[str] = None  
    kardex_screenshot_url: Optional[str] = None  
    # ------------------------------
    advisorSubjects: Optional[List[str]] = []
    createdAt: datetime = Field(default_factory=datetime.now)
    updatedAt: datetime = Field(default_factory=datetime.now)
    updatedAt: datetime = Field(default_factory=datetime.now)
class Subject(MongoBaseModel):
    name: str
    description: Optional[str] = None
    isActive: bool = True
    createdBy: PyObjectId
    createdAt: datetime = Field(default_factory=datetime.now)

class Request(MongoBaseModel):
    studentId: PyObjectId
    advisorId: Optional[PyObjectId] = None
    subject: str
    topic: str
    description: Optional[str] = None
    status: RequestStatusEnum = RequestStatusEnum.PENDING
    createdAt: datetime = Field(default_factory=datetime.now)
    takenAt: Optional[datetime] = None

class Session(MongoBaseModel):
    requestId: PyObjectId
    studentId: PyObjectId
    advisorId: PyObjectId
    approvedBy: Optional[PyObjectId] = None
    
    scheduledAt: datetime
    meetingPlatform: MeetingPlatformEnum
    meetingLink: Optional[str] = None
    teamsMeetingId: Optional[str] = None
    
    status: SessionStatusEnum = SessionStatusEnum.PENDING_APPROVAL
    
    verification: Optional[Verification] = None
    
    createdAt: datetime = Field(default_factory=datetime.now)
    approvedAt: Optional[datetime] = None
    completedAt: Optional[datetime] = None

class Chat(MongoBaseModel):
    sessionId: PyObjectId
    studentId: PyObjectId
    advisorId: PyObjectId
    messages: List[Message] = []
    lastMessageAt: Optional[datetime] = None
    createdAt: datetime = Field(default_factory=datetime.now)
