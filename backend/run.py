import uvicorn
import os
import sys

# Thêm thư mục gốc backend vào sys.path để import chuẩn module
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

if __name__ == "__main__":
    print("=" * 60)
    print("  🌿 ĐANG KHỞI ĐỘNG HỆ THỐNG FULLSTACK TÂM GIAO (SOULECHO) 🌿")
    print("=" * 60)
    print("  📡 Backend API:     http://localhost:8000")
    print("  📑 Tài liệu API:    http://localhost:8000/docs")
    print("  🖥️  Giao diện Web:   http://localhost:8000/")
    print("=" * 60)
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)

