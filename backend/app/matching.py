import json
from typing import List, Dict, Tuple

def parse_json_list(raw_val) -> List[str]:
    if not raw_val:
        return []
    if isinstance(raw_val, list):
        return raw_val
    try:
        data = json.loads(raw_val)
        return data if isinstance(data, list) else []
    except Exception:
        return [item.strip() for item in str(raw_val).split(",") if item.strip()]

def calculate_jaccard_similarity(list_a: List[str], list_b: List[str]) -> float:
    set_a = set(item.strip().lower() for item in list_a if item.strip())
    set_b = set(item.strip().lower() for item in list_b if item.strip())
    
    if not set_a and not set_b:
        return 0.5
    if not set_a or not set_b:
        return 0.2
        
    intersection = len(set_a.intersection(set_b))
    union = len(set_a.union(set_b))
    return intersection / union if union > 0 else 0.0

def calculate_life_stage_similarity(stage_a: str, stage_b: str) -> float:
    stage_a = (stage_a or "").strip().lower()
    stage_b = (stage_b or "").strip().lower()
    
    if stage_a == stage_b:
        return 1.0
        
    adjacent_pairs = [
        {"học sinh thpt", "sinh viên"},
        {"sinh viên", "mới đi làm"},
        {"mới đi làm", "chuyển ngành / chông chênh"}
    ]
    
    for pair in adjacent_pairs:
        if stage_a in pair and stage_b in pair:
            return 0.75
            
    return 0.40

def calculate_user_match(survey_current, survey_candidate) -> Tuple[int, str]:
    """
    Tính điểm tương đồng giữa hai người dùng (0 - 100%) và tạo lý do thấu cảm.
    """
    issues_a = parse_json_list(survey_current.primary_issues)
    issues_b = parse_json_list(survey_candidate.primary_issues)
    goals_a = parse_json_list(survey_current.goals)
    goals_b = parse_json_list(survey_candidate.goals)

    # 1. Trùng lặp vấn đề gặp phải (Trọng số 40%)
    issue_sim = calculate_jaccard_similarity(issues_a, issues_b)

    # 2. Giai đoạn cuộc sống / độ tuổi (Trọng số 25%)
    stage_sim = calculate_life_stage_similarity(survey_current.life_stage, survey_candidate.life_stage)

    # 3. Mục tiêu kết nối (Trọng số 20%)
    goal_sim = calculate_jaccard_similarity(goals_a, goals_b)

    # 4. Hình thức trò chuyện ưu tiên (Trọng số 15%)
    fmt_a = survey_current.preferred_format
    fmt_b = survey_candidate.preferred_format
    if fmt_a == fmt_b:
        format_sim = 1.0
    elif "both" in (fmt_a, fmt_b):
        format_sim = 0.9
    else:
        format_sim = 0.6

    raw_score = (issue_sim * 0.40) + (stage_sim * 0.25) + (goal_sim * 0.20) + (format_sim * 0.15)
    
    # Scale score to realistic high-empathy range (60% - 98%)
    scaled_score = int(55 + (raw_score * 43))
    scaled_score = min(98, max(50, scaled_score))

    # Xây dựng lý do tương đồng bằng tiếng Việt tự nhiên
    reasons = []
    common_issues = set(i.lower() for i in issues_a).intersection(set(i.lower() for i in issues_b))
    if common_issues:
        first_issue = list(common_issues)[0].capitalize()
        reasons.append(f"Cùng trăn trở về {first_issue}")
        
    if survey_current.life_stage and survey_current.life_stage.lower() == survey_candidate.life_stage.lower():
        reasons.append(f"Cùng là {survey_current.life_stage.lower()}")
    elif stage_sim >= 0.75:
        reasons.append("Giai đoạn trải nghiệm tương đồng")

    common_goals = set(g.lower() for g in goals_a).intersection(set(g.lower() for g in goals_b))
    if common_goals:
        reasons.append("Có chung mong muốn tìm người lắng nghe chân thành")

    if not reasons:
        reasons.append("Có tần số cảm xúc và mong muốn chia sẻ tương thích")

    match_reason_str = " · ".join(reasons)
    return scaled_score, match_reason_str

def calculate_group_match(survey_current, group) -> Tuple[int, str]:
    """
    Tính độ phù hợp giữa người dùng và một Nhóm (0 - 100%).
    """
    user_issues = [i.lower() for i in parse_json_list(survey_current.primary_issues)]
    group_tags = [t.lower() for t in parse_json_list(group.tags)]
    
    match_count = 0
    reasons = []
    
    # Check category match
    if any(issue in group.category.lower() or group.category.lower() in issue for issue in user_issues):
        match_count += 3
        reasons.append(f"Chủ đề '{group.category}' đúng với trăn trở hiện tại của bạn")

    # Check tags overlap
    common_tags = set(user_issues).intersection(set(group_tags))
    if common_tags:
        match_count += len(common_tags) * 2
        reasons.append(f"Chung chủ đề: {', '.join(list(common_tags)[:2])}")

    # Micro-group preference
    if group.is_micro_group and survey_current.preferred_format in ["small_group", "both"]:
        match_count += 2
        reasons.append("Nhóm nhỏ 2–5 người an toàn, ấm cúng và ít phán xét")
    elif not group.is_micro_group and survey_current.preferred_format in ["both", "community"]:
        match_count += 1
        reasons.append("Cộng đồng cởi mở, nhiều góc nhìn đa chiều")

    base_percentage = 60 + min(36, match_count * 7)
    if not reasons:
        reasons.append("Không gian đồng cảm phù hợp để lắng nghe kinh nghiệm")

    return int(base_percentage), " · ".join(reasons)

