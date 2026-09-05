from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, Text, DateTime, ForeignKey, Float
from sqlalchemy.orm import relationship
from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    display_name = Column(String(100), nullable=False)
    avatar_url = Column(String(255), default="")
    is_anonymous = Column(Boolean, default=True)
    anonymous_alias = Column(String(100), default="Mầm Nhỏ")
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    survey = relationship("Survey", back_populates="user", uselist=False, cascade="all, delete-orphan")
    journals = relationship("JournalEntry", back_populates="user", cascade="all, delete-orphan")

class Survey(Base):
    __tablename__ = "surveys"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    age_bracket = Column(String(30), default="18-22")
    life_stage = Column(String(100), default="Sinh viên")
    primary_issues = Column(Text, default="[]")  # JSON-encoded array: ["Áp lực học tập", "Cô đơn"]
    goals = Column(Text, default="[]")           # JSON-encoded array: ["Tìm người lắng nghe"]
    preferred_format = Column(String(30), default="one_to_one") # one_to_one, small_group, both
    story_summary = Column(Text, default="")
    urgency_level = Column(Integer, default=1)   # 1: Nhẹ, 2: Vừa, 3: Cần người chia sẻ gấp
    personality_style = Column(String(50), default="Lắng nghe") # Lắng nghe, Cởi mở, Sâu sắc, v.v.
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="survey")

class Group(Base):
    __tablename__ = "groups"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), nullable=False)
    description = Column(Text, nullable=False)
    category = Column(String(100), nullable=False)
    is_micro_group = Column(Boolean, default=False) # True: Nhóm nhỏ 2-5 người cùng cảnh ngộ
    max_members = Column(Integer, default=5)
    current_members = Column(Integer, default=1)
    icon = Column(String(50), default="🌱")
    tags = Column(Text, default="[]") # JSON tags
    created_at = Column(DateTime, default=datetime.utcnow)

class GroupMembership(Base):
    __tablename__ = "group_memberships"

    id = Column(Integer, primary_key=True, index=True)
    group_id = Column(Integer, ForeignKey("groups.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    role = Column(String(30), default="member")
    joined_at = Column(DateTime, default=datetime.utcnow)

class Connection(Base):
    __tablename__ = "connections"

    id = Column(Integer, primary_key=True, index=True)
    user_id_1 = Column(Integer, ForeignKey("users.id"), nullable=False)
    user_id_2 = Column(Integer, ForeignKey("users.id"), nullable=False)
    status = Column(String(30), default="pending") # pending, accepted, declined
    similarity_score = Column(Integer, default=80) # 0 - 100
    match_reasons = Column(Text, default="")
    created_at = Column(DateTime, default=datetime.utcnow)

class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    sender_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    receiver_id = Column(Integer, ForeignKey("users.id"), nullable=True) # None if group message
    group_id = Column(Integer, ForeignKey("groups.id"), nullable=True)   # None if 1-1 message
    content = Column(Text, nullable=False)
    message_type = Column(String(30), default="text") # text, icebreaker, reaction, call_event
    created_at = Column(DateTime, default=datetime.utcnow)

class JournalEntry(Base):
    __tablename__ = "journal_entries"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    mood_score = Column(Integer, default=3) # 1 (Rất tệ) - 5 (Rất tốt)
    title = Column(String(200), default="")
    content = Column(Text, nullable=False)
    tags = Column(String(200), default="")
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="journals")

class Expert(Base):
    __tablename__ = "experts"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    title = Column(String(150), nullable=False)
    specialty = Column(String(150), nullable=False)
    bio = Column(Text, nullable=False)
    rating = Column(Float, default=5.0)
    reviews_count = Column(Integer, default=10)
    experience_years = Column(Integer, default=5)
    available_time = Column(String(100), default="T2 - T6 (18:00 - 21:00)")
    avatar_url = Column(String(255), default="")
    organization = Column(String(200), default="Tổ chức Sức khỏe Tinh thần")

