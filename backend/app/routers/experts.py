import random
from datetime import date, timedelta
from typing import List
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Expert, Appointment, User
from ..schemas import ExpertResponse, AppointmentCreate, AppointmentResponse, AppointmentSummary, ExpertAvailabilityResponse, AvailabilitySlot

router = APIRouter(prefix="/api/experts", tags=["Experts & Counseling"])

@router.get("", response_model=List[ExpertResponse])
def list_experts(db: Session = Depends(get_db)):
    experts = db.query(Expert).all()
    return experts

@router.get("/{expert_id}/availability", response_model=ExpertAvailabilityResponse)
def expert_availability(expert_id: int, db: Session = Depends(get_db)):
    expert = db.query(Expert).filter(Expert.id == expert_id).first()
    if not expert:
        raise HTTPException(status_code=404, detail="Không tìm thấy thông tin chuyên gia.")

    weekday_names = ["Thứ 2", "Thứ 3", "Thứ 4", "Thứ 5", "Thứ 6", "Thứ 7", "Chủ Nhật"]
    booked_times = {item.selected_time for item in db.query(Appointment).filter(Appointment.expert_id == expert_id).all()}
    slots = []
    for day_offset in range(14):
        slot_date = date.today() + timedelta(days=day_offset)
        weekday = weekday_names[slot_date.weekday()]
        if weekday not in expert.available_time and not (weekday == "Chủ Nhật" and "CN" in expert.available_time):
            continue
        time_ranges = ["09:00 - 10:00", "10:30 - 11:30"] if weekday in ("Thứ 7", "Chủ Nhật") else ["18:30 - 19:30", "20:00 - 21:00"]
        for time_range in time_ranges:
            value = f"{slot_date.isoformat()}|{time_range}"
            slots.append(AvailabilitySlot(value=value, label=f"{weekday}, {slot_date.strftime('%d/%m')} · {time_range}", available=value not in booked_times))
    return ExpertAvailabilityResponse(expert_id=expert.id, expert_name=expert.name, slots=slots)

@router.get("/appointments/{user_id}", response_model=List[AppointmentSummary])
def list_user_appointments(user_id: int, db: Session = Depends(get_db)):
    appointments = db.query(Appointment).filter(Appointment.user_id == user_id).order_by(Appointment.created_at.desc()).all()
    return [AppointmentSummary(
        id=item.id,
        booking_code=item.booking_code,
        expert_name=item.expert.name,
        expert_title=item.expert.title,
        selected_time=item.selected_time,
        service_package=item.service_package,
        call_format=item.call_format,
        fee_amount=item.fee_amount,
        payment_status=item.payment_status,
        created_at=item.created_at,
    ) for item in appointments]

@router.post("/book", response_model=AppointmentResponse)
def book_expert_appointment(booking: AppointmentCreate, db: Session = Depends(get_db)):
    expert = db.query(Expert).filter(Expert.id == booking.expert_id).first()
    if not expert:
        raise HTTPException(status_code=404, detail="Không tìm thấy thông tin chuyên gia.")

    user = db.query(User).filter(User.id == booking.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Không tìm thấy người dùng.")

    existing_booking = db.query(Appointment).filter(
        Appointment.expert_id == booking.expert_id,
        Appointment.selected_time == booking.selected_time,
    ).first()
    if existing_booking:
        raise HTTPException(status_code=409, detail="Khung giờ này vừa được đặt. Vui lòng chọn khung giờ khác.")

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
