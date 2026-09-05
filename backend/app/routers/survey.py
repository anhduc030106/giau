import json
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Survey, User
from ..schemas import SurveyCreate, SurveyResponse
from ..matching import parse_json_list

router = APIRouter(prefix="/api/survey", tags=["Survey"])

@router.post("/{user_id}", response_model=SurveyResponse)
def submit_survey(user_id: int, survey_in: SurveyCreate, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Không tìm thấy người dùng.")

    existing_survey = db.query(Survey).filter(Survey.user_id == user_id).first()
    
    issues_json = json.dumps(survey_in.primary_issues, ensure_ascii=False)
    goals_json = json.dumps(survey_in.goals, ensure_ascii=False)

    if existing_survey:
        existing_survey.age_bracket = survey_in.age_bracket
        existing_survey.life_stage = survey_in.life_stage
        existing_survey.primary_issues = issues_json
        existing_survey.goals = goals_json
        existing_survey.preferred_format = survey_in.preferred_format
        existing_survey.story_summary = survey_in.story_summary or ""
        existing_survey.urgency_level = survey_in.urgency_level
        existing_survey.personality_style = survey_in.personality_style or "Lắng nghe"
        db.commit()
        db.refresh(existing_survey)
        target = existing_survey
    else:
        new_survey = Survey(
            user_id=user_id,
            age_bracket=survey_in.age_bracket,
            life_stage=survey_in.life_stage,
            primary_issues=issues_json,
            goals=goals_json,
            preferred_format=survey_in.preferred_format,
            story_summary=survey_in.story_summary or "",
            urgency_level=survey_in.urgency_level,
            personality_style=survey_in.personality_style or "Lắng nghe"
        )
        db.add(new_survey)
        db.commit()
        db.refresh(new_survey)
        target = new_survey

    return SurveyResponse(
        id=target.id,
        user_id=target.user_id,
        age_bracket=target.age_bracket,
        life_stage=target.life_stage,
        primary_issues=parse_json_list(target.primary_issues),
        goals=parse_json_list(target.goals),
        preferred_format=target.preferred_format,
        story_summary=target.story_summary,
        urgency_level=target.urgency_level,
        personality_style=target.personality_style,
        created_at=target.created_at
    )

@router.get("/{user_id}", response_model=SurveyResponse)
def get_survey(user_id: int, db: Session = Depends(get_db)):
    survey = db.query(Survey).filter(Survey.user_id == user_id).first()
    if not survey:
        raise HTTPException(status_code=404, detail="Người dùng chưa thực hiện khảo sát.")

    return SurveyResponse(
        id=survey.id,
        user_id=survey.user_id,
        age_bracket=survey.age_bracket,
        life_stage=survey.life_stage,
        primary_issues=parse_json_list(survey.primary_issues),
        goals=parse_json_list(survey.goals),
        preferred_format=survey.preferred_format,
        story_summary=survey.story_summary,
        urgency_level=survey.urgency_level,
        personality_style=survey.personality_style,
        created_at=survey.created_at
    )

