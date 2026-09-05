import random
from typing import List
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Expert, Appointment, User
from ..schemas import ExpertResponse, AppointmentCreate, AppointmentResponse

router = APIRouter(prefix="/api/experts", tags=["Experts & Counseling"])

@router.get("", response_model=List[ExpertResponse])
def list_experts(db: Session = Depends(get_db)):
    experts = db.query(Expert).all()
    return experts

@router.post("/book", response_model=AppointmentResponse)
def book_expert_appointment(booking: AppointmentCreate, db: Session = Depends(get_db)):
    expert = db.query(Expert).filter(Expert.id == booking.expert_id).first()
    if not expert:
        raise HTTPException(status_code=404, detail="Không tìm thấy thông tin chuyên gia.")

    user = db.query(User).filter(User.id == booking.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Không tìm thấy người dùng.")

    # Tính toán chi phí thực tế: Giảm giá nếu là Học sinh/Sinh viên
    final_fee = expert.student_fee if booking.is_student else expert.fee_per_session

    booking_code = f"TG-{random.randint(10000, 99999)}"

    new_app = Appointment(
        booking_code=booking_code,
        user_id=booking.user_id,
        expert_id=booking.expert_id,
        service_package=booking.service_package or f"Tham vấn {expert.session_duration}",
        call_format=booking.call_format or "Video Call Riêng Tư",
        selected_time=booking.selected_time,
        fee_amount=final_fee,
        payment_status="Chờ thanh toán / Giữ chỗ",
        user_note=booking.user_note or ""
    )
    db.add(new_app)
    db.commit()
    db.refresh(new_app)

    payment_instructions = (
        f"Vui lòng chuyển khoản {final_fee:,} VNĐ đến STK: 190384729108 (Ngân hàng Quân Đội MB Bank - CTK: TÂM GIAO SOULECHO), "
        f"Nội dung: {booking_code} để giữ lịch hẹn chính thức."
    )

    return AppointmentResponse(
        id=new_app.id,
        booking_code=new_app.booking_code,
        expert_name=expert.name,
        expert_title=expert.title,
        selected_time=new_app.selected_time,
        service_package=new_app.service_package,
        call_format=new_app.call_format,
        fee_amount=new_app.fee_amount,
        payment_status=new_app.payment_status,
        payment_instructions=payment_instructions,
        created_at=new_app.created_at
    )
