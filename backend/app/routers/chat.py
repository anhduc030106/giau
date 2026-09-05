from typing import List, Optional
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_
from ..database import get_db
from ..models import Message, User
from ..schemas import MessageCreate, MessageResponse

router = APIRouter(prefix="/api/chat", tags=["Chat"])

# Từ khóa nhạy cảm cần cảnh báo và điều hướng SOS
CRISIS_KEYWORDS = ["tự tử", "tự hại", "chết đi", "không muốn sống", "kết thúc tất cả", "tự sát"]

@router.get("/messages", response_model=List[MessageResponse])
def get_messages(
    user_id: int,
    partner_id: Optional[int] = Query(None),
    group_id: Optional[int] = Query(None),
    db: Session = Depends(get_db)
):
    if group_id:
        msgs = db.query(Message).filter(Message.group_id == group_id).order_by(Message.created_at.asc()).all()
    elif partner_id:
        msgs = db.query(Message).filter(
            or_(
                and_(Message.sender_id == user_id, Message.receiver_id == partner_id),
                and_(Message.sender_id == partner_id, Message.receiver_id == user_id)
            )
        ).order_by(Message.created_at.asc()).all()
    else:
        msgs = []

    res = []
    for m in msgs:
        sender = db.query(User).filter(User.id == m.sender_id).first()
        res.append(MessageResponse(
            id=m.id,
            sender_id=m.sender_id,
            sender_name=sender.display_name if sender else "Ẩn danh",
            sender_alias=sender.anonymous_alias if sender else "Mầm Nhỏ",
            sender_avatar=sender.avatar_url if sender else "",
            receiver_id=m.receiver_id,
            group_id=m.group_id,
            content=m.content,
            message_type=m.message_type,
            created_at=m.created_at
        ))
    return res

@router.post("/messages/{sender_id}", response_model=MessageResponse)
def send_message(sender_id: int, msg_in: MessageCreate, db: Session = Depends(get_db)):
    sender = db.query(User).filter(User.id == sender_id).first()
    if not sender:
        raise HTTPException(status_code=404, detail="Người gửi không tồn tại.")

    # Phát hiện từ khóa khủng hoảng để can thiệp hỗ trợ
    has_crisis = any(kw in msg_in.content.lower() for kw in CRISIS_KEYWORDS)
    m_type = msg_in.message_type
    if has_crisis:
        m_type = "crisis_alert"

    new_msg = Message(
        sender_id=sender_id,
        receiver_id=msg_in.receiver_id,
        group_id=msg_in.group_id,
        content=msg_in.content,
        message_type=m_type
    )
    db.add(new_msg)
    db.commit()
    db.refresh(new_msg)

    return MessageResponse(
        id=new_msg.id,
        sender_id=new_msg.sender_id,
        sender_name=sender.display_name,
        sender_alias=sender.anonymous_alias,
        sender_avatar=sender.avatar_url,
        receiver_id=new_msg.receiver_id,
        group_id=new_msg.group_id,
        content=new_msg.content,
        message_type=new_msg.message_type,
        created_at=new_msg.created_at
    )

