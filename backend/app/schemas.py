from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, EmailStr

# Auth & User Schemas
class UserRegister(BaseModel):
    username: str
    email: EmailStr
    password: str
    display_name: Optional[str] = None
    is_anonymous: bool = True
    anonymous_alias: Optional[str] = None

class UserLogin(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    display_name: str
    avatar_url: Optional[str] = ""
    is_anonymous: bool
    anonymous_alias: str
    has_completed_survey: bool = False
    created_at: datetime

    class Config:
        from_attributes = True

# Survey Schemas
class SurveyCreate(BaseModel):
    age_bracket: str
    life_stage: str
    primary_issues: List[str]
    goals: List[str]
    preferred_format: str = "one_to_one"
    story_summary: Optional[str] = ""
    urgency_level: int = 1
    personality_style: Optional[str] = "Lắng nghe"

class SurveyResponse(BaseModel):
    id: int
    user_id: int
    age_bracket: str
    life_stage: str
    primary_issues: List[str]
    goals: List[str]
    preferred_format: str
    story_summary: str
    urgency_level: int
    personality_style: str
    created_at: datetime

    class Config:
        from_attributes = True

# Recommendation Schemas
class UserMatchRecommendation(BaseModel):
    user_id: int
    display_name: str
    anonymous_alias: str
    is_anonymous: bool
    avatar_url: str
    age_bracket: str
    life_stage: str
    primary_issues: List[str]
    story_summary: str
    similarity_score: int # 0-100%
    match_reasons: str
    urgency_level: int

class GroupMatchRecommendation(BaseModel):
    id: int
    name: str
    description: str
    category: str
    is_micro_group: bool
    max_members: int
    current_members: int
    icon: str
    match_percentage: int
    match_reasons: str

# Chat Schemas
class MessageCreate(BaseModel):
    receiver_id: Optional[int] = None
    group_id: Optional[int] = None
    content: str
    message_type: str = "text"

class MessageResponse(BaseModel):
    id: int
    sender_id: int
    sender_name: str
    sender_alias: str
    sender_avatar: str
    receiver_id: Optional[int] = None
    group_id: Optional[int] = None
    content: str
    message_type: str
    created_at: datetime

    class Config:
        from_attributes = True

# Journal Schemas
class JournalCreate(BaseModel):
    mood_score: int
    title: str = ""
    content: str
    tags: Optional[str] = ""

class JournalResponse(BaseModel):
    id: int
    mood_score: int
    title: str
    content: str
    tags: str
    created_at: datetime

    class Config:
        from_attributes = True

# Expert & Appointment Schemas
class ExpertResponse(BaseModel):
    id: int
    name: str
    title: str
    specialty: str
    bio: str
    rating: float
    reviews_count: int
    experience_years: int
    available_time: str
    avatar_url: str
    organization: str
    fee_per_session: int
    student_fee: int
    session_duration: str

    class Config:
        from_attributes = True

class AppointmentCreate(BaseModel):
    user_id: int
    expert_id: int
    selected_time: str
    service_package: Optional[str] = "Tham vấn Tiêu chuẩn"
    call_format: Optional[str] = "Video Call Riêng Tư"
    is_student: Optional[bool] = False
    user_note: Optional[str] = ""

class AppointmentResponse(BaseModel):
    id: int
    booking_code: str
    expert_name: str
    expert_title: str
    selected_time: str
    service_package: str
    call_format: str
    fee_amount: int
    payment_status: str
    payment_instructions: str
    created_at: datetime

    class Config:
        from_attributes = True

class AppointmentSummary(BaseModel):
    id: int
    booking_code: str
    expert_name: str
    expert_title: str
    selected_time: str
    service_package: str
    call_format: str
    fee_amount: int
    payment_status: str
    created_at: datetime

    class Config:
        from_attributes = True

class AvailabilitySlot(BaseModel):
    value: str
    label: str
    available: bool

class ExpertAvailabilityResponse(BaseModel):
    expert_id: int
    expert_name: str
    slots: List[AvailabilitySlot]
