from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import JournalEntry, User
from ..schemas import JournalCreate, JournalResponse

router = APIRouter(prefix="/api/wellness", tags=["Wellness & SOS"])

VIETNAM_SOS_HOTLINES = [
    {
        "name": "Đường dây nóng Ngày Mai",
        "phone": "096 306 1414",
        "description": "Tham vấn & hỗ trợ người trầm cảm, khủng hoảng tinh thần bởi TS. Đặng Hoàng Giang.",
        "operating_hours": "13:00 - 20:30 (Thứ 4 đến Chủ Nhật)",
        "badge": "Chữa lành & Trầm cảm",
        "cost": "Cước viễn thông thông thường"
    },
    {
        "name": "Tổng đài Quốc gia Bảo vệ Trẻ em & Thanh thiếu niên 111",
        "phone": "111",
        "description": "Tư vấn tâm lý, bảo vệ khẩn cấp khỏi bạo lực học đường, xâm hại và áp lực gia đình.",
        "operating_hours": "24/7 (Cả tuần)",
        "badge": "Miễn phí 100%",
        "cost": "Hoàn toàn miễn cước gọi"
    },
    {
        "name": "Viện Sức khỏe Tâm thần - Bệnh viện Bạch Mai",
        "phone": "024 3869 3731",
        "description": "Cấp cứu can thiệp rối loạn lo âu nặng, mất ngủ kéo dài và các bệnh lý tâm thần chuyên sâu.",
        "operating_hours": "24/7 Cấp cứu",
        "badge": "Y tế chuyên sâu",
        "cost": "Theo biểu phí viện phí"
    },
    {
        "name": "Đường dây Phím Số Kỳ Diệu (CSAGA)",
        "phone": "024 3333 5599",
        "description": "Tư vấn tâm lý tình cảm, bạo lực giới và sang chấn tinh thần cho thanh thiếu niên.",
        "operating_hours": "24/7",
        "badge": "Tình cảm & Sang chấn",
        "cost": "Cước viễn thông tiêu chuẩn"
    }
]

@router.get("/sos-hotlines")
def get_sos_hotlines():
    return {
        "status": "success",
        "hotlines": VIETNAM_SOS_HOTLINES,
        "first_aid_steps": [
            "1. DỪNG LẠI: Hít một hơi thật sâu bằng mũi trong 4 giây, giữ lại 7 giây và thở ra từ từ qua miệng trong 8 giây.",
            "2. TIẾP ĐẤT: Nhìn xung quanh, gọi tên 5 đồ vật màu xanh, chạm vào 4 bề mặt khác nhau xung quanh bạn.",
            "3. KẾT NỐI: Nhấn nút gọi ngay một trong các đường dây nóng phía trên, bạn không hề cô độc."
        ]
    }

@router.get("/journal/{user_id}", response_model=List[JournalResponse])
def get_user_journals(user_id: int, db: Session = Depends(get_db)):
    entries = db.query(JournalEntry).filter(JournalEntry.user_id == user_id).order_by(JournalEntry.created_at.desc()).all()
    return entries

@router.post("/journal/{user_id}", response_model=JournalResponse)
def create_journal_entry(user_id: int, entry_in: JournalCreate, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Không tìm thấy người dùng.")

    entry = JournalEntry(
        user_id=user_id,
        mood_score=entry_in.mood_score,
        title=entry_in.title or "Ghi chép cảm xúc hôm nay",
        content=entry_in.content,
        tags=entry_in.tags or ""
    )
    db.add(entry)
    db.commit()
    db.refresh(entry)
    return entry

