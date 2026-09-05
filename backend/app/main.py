import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from .database import engine, Base, SessionLocal
from .seed_data import seed_database
from .routers import auth, survey, recommendations, chat, wellness, experts

# Khởi tạo bảng CSDL và nạp dữ liệu mẫu
Base.metadata.create_all(bind=engine)
db = SessionLocal()
try:
    seed_database(db)
finally:
    db.close()

app = FastAPI(
    title="TÂM GIAO (SoulEcho) API",
    description="Nền tảng kết nối thấu cảm thông minh theo vấn đề tâm lý - xã hội, thuật toán gợi ý tương đồng và sơ cứu tinh thần.",
    version="1.0.0"
)

# Cấu hình CORS để frontend tương tác mượt mà
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Đăng ký các API routers
app.include_router(auth.router)
app.include_router(survey.router)
app.include_router(recommendations.router)
app.include_router(chat.router)
app.include_router(wellness.router)
app.include_router(experts.router)

# Phục vụ file tĩnh frontend nếu có
frontend_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "frontend")
if not os.path.exists(frontend_path):
    frontend_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

if os.path.exists(os.path.join(frontend_path, "index.html")):
    app.mount("/static", StaticFiles(directory=frontend_path), name="static")

    @app.get("/")
    def read_index():
        return FileResponse(os.path.join(frontend_path, "index.html"))

@app.get("/api/health")
def health_check():
    return {
        "status": "healthy",
        "app_name": "Tâm Giao (SoulEcho)",
        "version": "1.0.0",
        "message": "Nền tảng kết nối thấu cảm đang hoạt động bình thường."
    }

