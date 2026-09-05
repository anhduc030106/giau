import json
from sqlalchemy.orm import Session
from .models import User, Survey, Group, Expert

def seed_database(db: Session):
    # Kiểm tra nếu đã có dữ liệu thì không nạp lại
    if db.query(User).filter(User.username == "mam_nho142").first():
        return

    # 1. Khởi tạo danh sách người dùng mẫu (Candidate Users)
    sample_users = [
        {
            "username": "mam_nho142",
            "email": "mamnho@tamgiao.vn",
            "display_name": "Minh Anh",
            "anonymous_alias": "Mầm Nhỏ #142",
            "avatar_url": "https://api.dicebear.com/7.x/bottts/svg?seed=mamnho",
            "is_anonymous": True,
            "survey": {
                "age_bracket": "18-22",
                "life_stage": "Sinh viên",
                "primary_issues": ["Áp lực học tập", "Cô đơn", "Tự ti năng lực"],
                "goals": ["Tìm người lắng nghe", "Tìm bạn cùng học tập"],
                "preferred_format": "both",
                "story_summary": "Mình là sinh viên năm nhất xa nhà, môi trường đại học quá khác biệt làm mình thường xuyên tự ti và thấy bản thân tụt lại phía sau so với bạn bè.",
                "urgency_level": 2,
                "personality_style": "Trầm tính, biết lắng nghe"
            }
        },
        {
            "username": "dom_dom89",
            "email": "domdom@tamgiao.vn",
            "display_name": "Hoàng Long",
            "anonymous_alias": "Đom Đóm #89",
            "avatar_url": "https://api.dicebear.com/7.x/bottts/svg?seed=domdom",
            "is_anonymous": True,
            "survey": {
                "age_bracket": "23-27",
                "life_stage": "Mới đi làm",
                "primary_issues": ["Burnout công việc", "Áp lực gia đình", "Lo âu tương lai"],
                "goals": ["Chia sẻ kinh nghiệm", "Giải tỏa áp lực"],
                "preferred_format": "one_to_one",
                "story_summary": "Đi làm công sở 1 năm nhưng ngày nào cũng thấy kiệt sức, bố mẹ ở quê luôn kỳ vọng mình phải thành đạt gửi tiền về, nhiều đêm chỉ biết khóc một mình.",
                "urgency_level": 2,
                "personality_style": "Cởi mở, sâu sắc"
            }
        },
        {
            "username": "may_trang215",
            "email": "maytrang@tamgiao.vn",
            "display_name": "Bảo Ngọc",
            "anonymous_alias": "Mây Trắng #215",
            "avatar_url": "https://api.dicebear.com/7.x/bottts/svg?seed=maytrang",
            "is_anonymous": True,
            "survey": {
                "age_bracket": "18-22",
                "life_stage": "Sinh viên",
                "primary_issues": ["Đổ vỡ tình cảm", "Overthinking", "Cô đơn"],
                "goals": ["Tìm người lắng nghe", "Chữa lành bản thân"],
                "preferred_format": "small_group",
                "story_summary": "Vừa chia tay mối tình 3 năm, cảm giác trống rỗng và mất đi một phần cuộc sống. Mình muốn tìm những bạn cùng hoàn cảnh để động viên nhau bước tiếp.",
                "urgency_level": 3,
                "personality_style": "Tình cảm, thấu cảm"
            }
        },
        {
            "username": "gio_mua304",
            "email": "giomua@tamgiao.vn",
            "display_name": "Đình Phong",
            "anonymous_alias": "Gió Mùa #304",
            "avatar_url": "https://api.dicebear.com/7.x/bottts/svg?seed=giomua",
            "is_anonymous": True,
            "survey": {
                "age_bracket": "15-18",
                "life_stage": "Học sinh THPT",
                "primary_issues": ["Áp lực thi cử", "Mâu thuẫn gia đình", "Tự ti ngoại hình"],
                "goals": ["Tìm người có kinh nghiệm", "Giảm căng thẳng"],
                "preferred_format": "both",
                "story_summary": "Lớp 12 với chuỗi ngày học thêm kín lịch. Bố mẹ so sánh mình với con nhà người ta khiến mình không dám về nhà.",
                "urgency_level": 2,
                "personality_style": "Ít nói, chân thành"
            }
        },
        {
            "username": "huong_duong77",
            "email": "huongduong@tamgiao.vn",
            "display_name": "Phương Thảo",
            "anonymous_alias": "Hướng Dương #77",
            "avatar_url": "https://api.dicebear.com/7.x/bottts/svg?seed=huongduong",
            "is_anonymous": True,
            "survey": {
                "age_bracket": "18-22",
                "life_stage": "Sinh viên",
                "primary_issues": ["Áp lực học tập", "Phát triển bản thân"],
                "goals": ["Hỗ trợ người khác", "Chia sẻ kinh nghiệm vượt qua"],
                "preferred_format": "one_to_one",
                "story_summary": "Năm nhất mình từng suýt trầm cảm vì nợ môn, nhưng giờ năm ba mình đã cân bằng lại được. Mình ở đây để lắng nghe và sẵn sàng chia sẻ cách mình đã vượt qua.",
                "urgency_level": 1,
                "personality_style": "Tích cực, ấm áp"
            }
        }
    ]

    for item in sample_users:
        u = User(
            username=item["username"],
            email=item["email"],
            hashed_password="123456",
            display_name=item["display_name"],
            anonymous_alias=item["anonymous_alias"],
            avatar_url=item["avatar_url"],
            is_anonymous=item["is_anonymous"]
        )
        db.add(u)
        db.commit()
        db.refresh(u)

        s_data = item["survey"]
        s = Survey(
            user_id=u.id,
            age_bracket=s_data["age_bracket"],
            life_stage=s_data["life_stage"],
            primary_issues=json.dumps(s_data["primary_issues"], ensure_ascii=False),
            goals=json.dumps(s_data["goals"], ensure_ascii=False),
            preferred_format=s_data["preferred_format"],
            story_summary=s_data["story_summary"],
            urgency_level=s_data["urgency_level"],
            personality_style=s_data["personality_style"]
        )
        db.add(s)

    # 2. Khởi tạo danh sách Nhóm (Groups)
    sample_groups = [
        {
            "name": "Trạm Trú Ẩn: Áp Lực Học Tập Năm Nhất",
            "description": "Nhóm nhỏ 2-5 bạn sinh viên năm nhất cùng giãi bày về cảm giác chới với trước giảng đường, thi cử và cách thích nghi.",
            "category": "Áp lực học tập",
            "is_micro_group": True,
            "max_members": 5,
            "current_members": 3,
            "icon": "🌱",
            "tags": json.dumps(["Áp lực học tập", "Sinh viên", "Cô đơn"], ensure_ascii=False)
        },
        {
            "name": "Nhóm Nhỏ: Chữa Lành Tổn Thương Sau Chia Tay",
            "description": "Vòng tròn 2-5 người cùng sẻ chia câu chuyện tan vỡ, khích lệ nhau tập trung yêu lấy chính mình.",
            "category": "Đổ vỡ tình cảm",
            "is_micro_group": True,
            "max_members": 5,
            "current_members": 4,
            "icon": "🕊️",
            "tags": json.dumps(["Đổ vỡ tình cảm", "Cô đơn", "Overthinking"], ensure_ascii=False)
        },
        {
            "name": "Vòng Tròn Lắng Nghe: Kỳ Vọng Từ Gia Đình",
            "description": "Nơi những người con chịu gánh nặng 'con nhà người ta' cùng ngồi lại, không phán xét, trao nhau cái ôm ấm áp.",
            "category": "Áp lực gia đình",
            "is_micro_group": True,
            "max_members": 5,
            "current_members": 2,
            "icon": "🕯️",
            "tags": json.dumps(["Áp lực gia đình", "Mâu thuẫn gia đình", "Tự ti"], ensure_ascii=False)
        },
        {
            "name": "Sinh Viên & Khủng Hoảng Tuổi 20",
            "description": "Cộng đồng chia sẻ các băn khoăn về định hướng nghề nghiệp, kỹ năng sống và cách duy trì sức khỏe tinh thần.",
            "category": "Phát triển bản thân",
            "is_micro_group": False,
            "max_members": 200,
            "current_members": 142,
            "icon": "🎓",
            "tags": json.dumps(["Sinh viên", "Phát triển bản thân", "Áp lực học tập"], ensure_ascii=False)
        },
        {
            "name": "Xả Căng Thẳng Sau Giờ Làm & Burnout",
            "description": "Dành cho các bạn trẻ mới đi làm đối mặt với deadline, sếp khó tính và mong muốn tìm lại sự cân bằng.",
            "category": "Burnout công việc",
            "is_micro_group": False,
            "max_members": 150,
            "current_members": 88,
            "icon": "💼",
            "tags": json.dumps(["Burnout công việc", "Lo âu tương lai", "Mới đi làm"], ensure_ascii=False)
        },
        {
            "name": "Trạm Thiền Thư Giãn & Tiếp Đất Mỗi Tối",
            "description": "Cùng nhau thực hành hít thở sâu, tắt điện thoại 30 phút và giải tỏa năng lượng tiêu cực trước khi ngủ.",
            "category": "Sức khỏe tinh thần",
            "is_micro_group": False,
            "max_members": 300,
            "current_members": 215,
            "icon": "🌙",
            "tags": json.dumps(["Overthinking", "Cô đơn", "Sức khỏe tinh thần"], ensure_ascii=False)
        }
    ]

    for g_item in sample_groups:
        g = Group(
            name=g_item["name"],
            description=g_item["description"],
            category=g_item["category"],
            is_micro_group=g_item["is_micro_group"],
            max_members=g_item["max_members"],
            current_members=g_item["current_members"],
            icon=g_item["icon"],
            tags=g_item["tags"]
        )
        db.add(g)

    # 3. Khởi tạo danh sách Chuyên gia (Experts) có biểu phí dịch vụ và trợ giá học đường
    sample_experts = [
        {
            "name": "ThS. Lê Hoàng Yến",
            "title": "Thạc sĩ Tâm lý Lâm sàng",
            "specialty": "Tham vấn học đường & Khủng hoảng thanh thiếu niên",
            "bio": "8 năm kinh nghiệm công tác tại Phòng Tham vấn Tâm lý Học đường THPT & Đại học. Đồng hành cùng hơn 1.200 học sinh, sinh viên vượt qua áp lực thi cử và trầm cảm nhẹ.",
            "rating": 4.9,
            "reviews_count": 84,
            "experience_years": 8,
            "available_time": "Thứ 2, 4, 6 (18:30 - 21:00)",
            "avatar_url": "https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?w=150&auto=format&fit=crop&q=80",
            "organization": "Trung tâm Tham vấn Tâm lý Sư Phạm",
            "fee_per_session": 350000,
            "student_fee": 190000,
            "session_duration": "60 phút"
        },
        {
            "name": "TS. Nguyễn Minh Triết",
            "title": "Tiến sĩ Tâm lý học - Trị liệu Gia đình",
            "specialty": "Hàn gắn mâu thuẫn phụ huynh & Khủng hoảng tuổi trưởng thành",
            "bio": "Tốt nghiệp ĐH Paris 8, chuyên sâu về giải tỏa căng thẳng gia đình, xóa bỏ khoảng cách thế hệ và giúp người trẻ tìm lại kết nối với cha mẹ.",
            "rating": 5.0,
            "reviews_count": 112,
            "experience_years": 12,
            "available_time": "Thứ 3, 5, 7 (19:00 - 21:30)",
            "avatar_url": "https://images.unsplash.com/photo-1537368910025-700350fe46c7?w=150&auto=format&fit=crop&q=80",
            "organization": "Viện Sức khỏe Tinh thần & Hành vi",
            "fee_per_session": 480000,
            "student_fee": 290000,
            "session_duration": "60 phút"
        },
        {
            "name": "ThS. Đỗ Thu Trang",
            "title": "Chuyên gia Hướng nghiệp & Sức khỏe Tinh thần",
            "specialty": "Burnout công sở, Rối loạn lo âu xã hội (Imposter Syndrome)",
            "bio": "Hỗ trợ các bạn trẻ mới ra trường vượt qua cảm giác hoang mang, tự ti năng lực và xây dựng ranh giới lành mạnh trong môi trường công việc.",
            "rating": 4.8,
            "reviews_count": 67,
            "experience_years": 6,
            "available_time": "Thứ 7, CN (09:00 - 16:00)",
            "avatar_url": "https://images.unsplash.com/photo-1580489944761-15a19d654956?w=150&auto=format&fit=crop&q=80",
            "organization": "Mạng lưới Career & Mental Health VN",
            "fee_per_session": 300000,
            "student_fee": 180000,
            "session_duration": "45 phút"
        }
    ]

    for exp_item in sample_experts:
        e = Expert(
            name=exp_item["name"],
            title=exp_item["title"],
            specialty=exp_item["specialty"],
            bio=exp_item["bio"],
            rating=exp_item["rating"],
            reviews_count=exp_item["reviews_count"],
            experience_years=exp_item["experience_years"],
            available_time=exp_item["available_time"],
            avatar_url=exp_item["avatar_url"],
            organization=exp_item["organization"],
            fee_per_session=exp_item["fee_per_session"],
            student_fee=exp_item["student_fee"],
            session_duration=exp_item["session_duration"]
        )
        db.add(e)

    db.commit()
