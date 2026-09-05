from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Expert
from ..schemas import ExpertResponse, AppointmentCreate

router = APIRouter(prefix="/api/experts", tags=["Experts & Counseling"])

@router.get("", response_model=List[ExpertResponse])
def list_experts(db: Session = Depends(get_db)):
    experts = db.query(Expert).all()
    return experts

@router.post("/book")
def book_expert_appointment(booking: AppointmentCreate, db: Session = Depends(get_db)):
    expert = db.query(Expert).filter(Expert.id == booking.expert_id).first()
    if not expert:
        raise HTTPException(status_code=404, detail="Không tìm thấy thông tin chuyên gia.")

    return {
        "status": "success",
        "message": f"Yêu cầu tham vấn với {expert.name} vào khung giờ {booking.selected_time} đã được ghi nhận.",
        "expert_name": expert.name,
        "selected_time": booking.selected_time,
        "note": "Phòng tham vấn sẽ gửi email/thông báo xác nhận lịch hẹn chính thức trong vòng 24 giờ."
    }

