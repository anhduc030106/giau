# 🌿 TÂM GIAO (SoulEcho) - Nền Tảng Kết Nối Thấu Cảm & Sức Khỏe Tinh Thần

> **Slogan:** *Kết nối thấu cảm, chữa lành tâm tư.*  
> Nền tảng kết nối người dùng ẩn danh theo vấn đề tâm lý - xã hội (áp lực học đường, gia đình, tình cảm, tự ti, cô đơn...), tích hợp thuật toán phân tích khảo sát đa chiều, gợi ý người tương đồng 1-1, nhóm nhỏ 2–5 người, trạm sơ cứu tinh thần, journaling và mạng lưới tham vấn học đường.

---

## 📁 Cấu Trúc Hệ Thống Fullstack

```text
giau/
├── index.html               # Giao diện Web App chính (Mở trực tiếp trên trình duyệt hoặc chạy qua FastAPI)
├── style.css                # Hệ thống thiết kế Calm & Healing, hoạt ảnh thở 4-7-8, Mobile-First
├── script.js                # Logic tương tác: Khảo sát, thuật toán Matching, Chat, SOS, Journaling
│
├── frontend/                # Thư mục Frontend độc lập (Dùng khi deploy tách biệt)
│   ├── index.html
│   ├── style.css
│   └── script.js
│
├── backend/                 # BACKEND FASTAPI (PYTHON)
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py          # Khởi tạo FastAPI App, CORS, static files, routers
│   │   ├── database.py      # CSDL SQLAlchemy (mặc định SQLite zero-config, sẵn sàng cho PostgreSQL)
│   │   ├── models.py        # SQLAlchemy Models: User, Survey, Group, Connection, Message, Journal, Expert
│   │   ├── schemas.py       # Pydantic Schemas xác thực dữ liệu request/response
│   │   ├── matching.py      # Thuật toán tính chỉ số tương đồng (Weighted Jaccard & Feature Matching)
│   │   ├── seed_data.py     # Nạp tự động dữ liệu mẫu: người dùng, nhóm nhỏ 2-5, chuyên gia, hotline
│   │   └── routers/
│   │       ├── auth.py      # Đăng ký, đăng nhập, chế độ ẩn danh
│   │       ├── survey.py    # Tiếp nhận khảo sát & cập nhật đặc trưng
│   │       ├── recommendations.py # API trả về Gợi ý Người 1-1 & Gợi ý Nhóm (% tương đồng)
│   │       ├── chat.py      # Trò chuyện an toàn & phát hiện từ khóa nguy cấp
│   │       ├── wellness.py  # Sổ tay cảm xúc (Journaling) & bài tập tinh thần
│   │       └── experts.py   # Danh bạ chuyên gia & đặt lịch tham vấn
│   ├── requirements.txt     # Danh sách thư viện Python
│   └── run.py               # Script khởi chạy FastAPI server 1 lệnh duy nhất
└── README.md                # Tài liệu hướng dẫn sử dụng
```

---

## 🚀 Hướng Dẫn Khởi Chạy

### Cách 1: Chạy Thử Ngay Lập Tức Không Cần Cài Đặt (Nhanh Nhất)
1. Bạn chỉ cần **click đúp vào tệp `index.html`** ở thư mục `giau` trên máy tính để mở bằng trình duyệt (Chrome, Edge, Cốc Cốc, Firefox...).
2. Ứng dụng tích hợp sẵn cơ chế **Fallback thông minh (Client-Side Simulation)**:
   - Toàn bộ thuật toán đo lường độ tương đồng (Matching Similarity Algorithm) sẽ tự động chạy ngay trên trình duyệt.
   - Bạn có thể làm khảo sát, xem bảng đề xuất `% tương đồng`, thử nhắn tin, thử bài tập thở 4-7-8, viết nhật ký cảm xúc mà không cần bất kỳ server nào!

---

### Cách 2: Khởi Động Server Fullstack Backend (FastAPI + Database)
Khi bạn muốn kết nối REST API thực tế với cơ sở dữ liệu:

1. Mở terminal tại thư mục `backend`:
   ```bash
   cd backend
   ```
2. Cài đặt các thư viện cần thiết:
   ```bash
   pip install -r requirements.txt
   ```
3. Chạy server bằng lệnh:
   ```bash
   python run.py
   ```
   *Hoặc chạy trực tiếp bằng uvicorn:*
   ```bash
   uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
   ```

4. Truy cập hệ sinh thái:
   - 🖥️ **Giao diện Web App:** [http://localhost:8000/](http://localhost:8000/)
   - 📑 **Tài liệu API Swagger tự động:** [http://localhost:8000/docs](http://localhost:8000/docs)
   - 🔍 **Health check:** [http://localhost:8000/api/health](http://localhost:8000/api/health)

---

## 💡 Các Chức Năng Cốt Lõi Đã Triển Khai

### 1. Khảo Sát Tâm Lý - Xã Hội Đa Bước (Intake Survey)
- **Bước 1**: Độ tuổi & Giai đoạn (Học sinh THPT, Sinh viên năm nhất, Sinh viên năm cuối, Mới đi làm, Đang chông chênh).
- **Bước 2**: Nỗi niềm cốt lõi (Áp lực học tập/thi cử, Mâu thuẫn gia đình, Đổ vỡ tình cảm, Tự ti ngoại hình/năng lực, Cô đơn, Burnout công việc, Overthinking).
- **Bước 3**: Mục tiêu & Tâm sự cá nhân (Tìm người lắng nghe, Tìm bạn cùng tiến, Tìm người có kinh nghiệm vượt qua).
- **Bước 4**: Chế độ kết nối (Ghép đôi 1-1 hay Nhóm nhỏ 2-5 người) & Tự động tạo bí danh chữa lành (ví dụ: *Mầm Nhỏ #204*, *Đom Đóm #89*).

### 2. Thuật Toán Gợi Ý Tương Đồng (Recommendation / Matching Engine)
- Đo lường chỉ số tương đồng đa yếu tố:
  $$\text{MatchScore} = 0.40 \times \text{Sim}_{\text{issues}} + 0.25 \times \text{Sim}_{\text{stage}} + 0.20 \times \text{Sim}_{\text{goals}} + 0.15 \times \text{Sim}_{\text{format}}$$
- **Gợi ý Người 1-1**: Hiển thị thẻ người dùng kèm `% tương đồng`, câu chuyện trích dẫn và lý do thấu cảm cụ thể (Ví dụ: *"89% tương đồng · Cùng là sinh viên năm nhất đang chịu áp lực học tập và gia đình"*).
- **Gợi ý Nhóm**: Nhóm nhỏ 2–5 người (Micro-groups) và nhóm cộng đồng lớn.

### 3. Phòng Chat An Toàn & Cuộc Gọi Thoại Ẩn Danh (Voice Call)
- **Quy tắc ứng xử (Code of Conduct)**: Cam kết "3 Không" (Không phán xét, Không quấy rối, Không ép lộ danh tính thật).
- **Icebreakers**: Gợi ý câu mở lời sâu sắc chỉ bằng 1 cú click.
- **Cử chỉ thấu cảm**: Gửi cái ôm 🤗, Thả tim ❤️, Vỗ vai động viên ✨.
- **Phát hiện từ khóa nguy cấp**: Tự động nhận diện từ khóa tự hại/khủng hoảng để hiển thị cảnh báo can thiệp và điều hướng SOS.
- **Mô phỏng Voice Call**: Giao diện gọi thoại ẩn danh với sóng âm thanh động và bộ đếm thời gian.

### 4. Trạm Chữa Lành & Sơ Cứu Cảm Xúc (Mental Wellness Toolkit)
- **Kỹ thuật thở 4-7-8**: Vòng tròn hoạt ảnh nở ra (Hít vào 4s) $\to$ Giữ hơi (7s) $\to$ Thu nhỏ (Thở ra 8s).
- **Tiếp đất 5-4-3-2-1**: Dẫn hướng 5 giác quan kéo tâm trí khỏi cơn hoảng loạn và overthinking.
- **Thùng xả uất ức (Burn Note)**: Viết ra áp lực rồi bấm nút để câu chữ bốc cháy/tan biến.
- **Sổ tay cảm xúc (Journaling)**: Chọn thang điểm cảm xúc (1-5), viết tâm sự và lưu giữ an toàn trên máy (LocalStorage).

### 5. Kênh Cứu Trợ Khẩn Cấp (SOS Crisis Hub 24/7)
- Nút SOS đỏ cố định ở thanh điều hướng.
- Kết nối trực tiếp các hotline uy tín tại Việt Nam:
  - **Đường dây nóng Ngày Mai**: `096 306 1414`
  - **Tổng đài Quốc gia 111 (Bảo vệ trẻ em và thanh thiếu niên)**: `111` (Miễn phí 24/7)
  - **Viện Sức khỏe Tâm thần - BV Bạch Mai**: `024 3869 3731`

### 6. Kết Nối Chuyên Gia & Mạng Lưới Học Đường (Expert Hub)
- Hồ sơ các Thạc sĩ, Tiến sĩ Tâm lý lâm sàng và Chuyên gia hướng nghiệp.
- Modal đặt lịch tham vấn chuyên sâu.
- Biểu mẫu đăng ký liên kết dành cho các Trường THPT, Đại học và Tổ chức sức khỏe tinh thần.

