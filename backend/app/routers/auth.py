import random
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import User
from ..schemas import UserRegister, UserLogin, UserResponse

router = APIRouter(prefix="/api/auth", tags=["Authentication"])

ANONYMOUS_ADJECTIVES = ["Mầm", "Mây", "Đom Đóm", "Gió", "Cỏ May", "Sao Băng", "Ánh Nắng", "Biển Xanh", "Hạt Mưa"]
ANONYMOUS_NOUNS = ["Nhỏ", "Trắng", "Hiền", "Thì Thầm", "Ấm Áp", "Lặng Lẽ", "Bình Yên", "Vươn Lên"]

def generate_random_alias():
    adj = random.choice(ANONYMOUS_ADJECTIVES)
    noun = random.choice(ANONYMOUS_NOUNS)
    number = random.randint(10, 999)
    return f"{adj} {noun} #{number}"

@router.post("/register", response_model=UserResponse)
def register(user_in: UserRegister, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(
        (User.username == user_in.username) | (User.email == user_in.email)
    ).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Tên đăng nhập hoặc email đã tồn tại trên hệ thống."
        )

    alias = user_in.anonymous_alias or generate_random_alias()
    display_name = user_in.display_name or user_in.username
    avatar = f"https://api.dicebear.com/7.x/bottts/svg?seed={user_in.username}"

    new_user = User(
        username=user_in.username,
        email=user_in.email,
        hashed_password=user_in.password,  # Trong thực tế hash với bcrypt/passlib
        display_name=display_name,
        anonymous_alias=alias,
        avatar_url=avatar,
        is_anonymous=user_in.is_anonymous
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return UserResponse(
        id=new_user.id,
        username=new_user.username,
        email=new_user.email,
        display_name=new_user.display_name,
        avatar_url=new_user.avatar_url,
        is_anonymous=new_user.is_anonymous,
        anonymous_alias=new_user.anonymous_alias,
        has_completed_survey=False,
        created_at=new_user.created_at
    )

@router.post("/login", response_model=UserResponse)
def login(user_in: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == user_in.username).first()
    if not user or user.hashed_password != user_in.password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Tên đăng nhập hoặc mật khẩu không chính xác."
        )

    has_survey = user.survey is not None
    return UserResponse(
        id=user.id,
        username=user.username,
        email=user.email,
        display_name=user.display_name,
        avatar_url=user.avatar_url,
        is_anonymous=user.is_anonymous,
        anonymous_alias=user.anonymous_alias,
        has_completed_survey=has_survey,
        created_at=user.created_at
    )

@router.get("/me/{user_id}", response_model=UserResponse)
def get_current_user_profile(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Không tìm thấy người dùng.")

    return UserResponse(
        id=user.id,
        username=user.username,
        email=user.email,
        display_name=user.display_name,
        avatar_url=user.avatar_url,
        is_anonymous=user.is_anonymous,
        anonymous_alias=user.anonymous_alias,
        has_completed_survey=user.survey is not None,
        created_at=user.created_at
    )

@router.post("/toggle-anonymous/{user_id}", response_model=UserResponse)
def toggle_anonymous_mode(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Không tìm thấy người dùng.")

    user.is_anonymous = not user.is_anonymous
    db.commit()
    db.refresh(user)

    return UserResponse(
        id=user.id,
        username=user.username,
        email=user.email,
        display_name=user.display_name,
        avatar_url=user.avatar_url,
        is_anonymous=user.is_anonymous,
        anonymous_alias=user.anonymous_alias,
        has_completed_survey=user.survey is not None,
        created_at=user.created_at
    )

