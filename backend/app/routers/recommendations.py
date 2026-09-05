from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import User, Survey, Group
from ..schemas import UserMatchRecommendation, GroupMatchRecommendation
from ..matching import calculate_user_match, calculate_group_match, parse_json_list

router = APIRouter(prefix="/api/recommendations", tags=["Recommendations"])

@router.get("/users/{user_id}", response_model=List[UserMatchRecommendation])
def get_user_recommendations(user_id: int, db: Session = Depends(get_db)):
    current_user_survey = db.query(Survey).filter(Survey.user_id == user_id).first()
    if not current_user_survey:
        # Nếu chưa làm khảo sát, trả về danh sách ứng viên mặc định điểm tương đồng tiêu chuẩn
        other_surveys = db.query(Survey).filter(Survey.user_id != user_id).all()
        results = []
        for s in other_surveys:
            u = s.user
            results.append(UserMatchRecommendation(
                user_id=u.id,
                display_name=u.display_name,
                anonymous_alias=u.anonymous_alias,
                is_anonymous=u.is_anonymous,
                avatar_url=u.avatar_url or f"https://api.dicebear.com/7.x/bottts/svg?seed={u.username}",
                age_bracket=s.age_bracket,
                life_stage=s.life_stage,
                primary_issues=parse_json_list(s.primary_issues),
                story_summary=s.story_summary,
                similarity_score=75,
                match_reasons="Đồng cảm và sẵn sàng lắng nghe câu chuyện của bạn",
                urgency_level=s.urgency_level
            ))
        return results

    # Tìm tất cả những người dùng khác có bản khảo sát
    candidate_surveys = db.query(Survey).filter(Survey.user_id != user_id).all()
    recommendations = []

    for c_survey in candidate_surveys:
        cand_user = c_survey.user
        if not cand_user:
            continue

        score, reasons = calculate_user_match(current_user_survey, c_survey)

        recommendations.append(UserMatchRecommendation(
            user_id=cand_user.id,
            display_name=cand_user.display_name,
            anonymous_alias=cand_user.anonymous_alias,
            is_anonymous=cand_user.is_anonymous,
            avatar_url=cand_user.avatar_url or f"https://api.dicebear.com/7.x/bottts/svg?seed={cand_user.username}",
            age_bracket=c_survey.age_bracket,
            life_stage=c_survey.life_stage,
            primary_issues=parse_json_list(c_survey.primary_issues),
            story_summary=c_survey.story_summary,
            similarity_score=score,
            match_reasons=reasons,
            urgency_level=c_survey.urgency_level
        ))

    # Sắp xếp giảm dần theo điểm tương đồng
    recommendations.sort(key=lambda x: x.similarity_score, reverse=True)
    return recommendations

@router.get("/groups/{user_id}", response_model=List[GroupMatchRecommendation])
def get_group_recommendations(user_id: int, db: Session = Depends(get_db)):
    current_user_survey = db.query(Survey).filter(Survey.user_id == user_id).first()
    all_groups = db.query(Group).all()

    recommendations = []

    for group in all_groups:
        if current_user_survey:
            score, reasons = calculate_group_match(current_user_survey, group)
        else:
            score = 70
            reasons = "Nhóm mở dành cho tất cả thành viên quan tâm"

        recommendations.append(GroupMatchRecommendation(
            id=group.id,
            name=group.name,
            description=group.description,
            category=group.category,
            is_micro_group=group.is_micro_group,
            max_members=group.max_members,
            current_members=group.current_members,
            icon=group.icon or "🌱",
            match_percentage=score,
            match_reasons=reasons
        ))

    recommendations.sort(key=lambda x: x.match_percentage, reverse=True)
    return recommendations

