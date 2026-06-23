# scorer.py

def calculate_score(analysis_result):          # ✅ Removed job_description parameter
    score = 0
    breakdown = {}

    # ── Contact Info Score (20 points) ──
    contact_score = 0
    if analysis_result["email"] != "Not Found":
        contact_score += 10
    if analysis_result["phone"] != "Not Found":
        contact_score += 10
    breakdown["Contact Info"] = contact_score
    score += contact_score

    # ── Skills Score (50 points) ──
    total_skills = sum(
        len(v) for v in analysis_result["skills"].values()
    )
    skill_score = min(total_skills * 5, 50)
    breakdown["Skills"] = skill_score
    score += skill_score

    # ── Education Score (15 points) ──
    edu_score = 0
    edu = [e.lower() for e in analysis_result["education"]]
    if any(e in edu for e in ["phd"]):
        edu_score = 15
    elif any(e in edu for e in ["m.tech", "mtech", "msc", "mba", "master"]):
        edu_score = 12
    elif any(e in edu for e in ["b.tech", "btech", "bsc", "be", "bachelor"]):
        edu_score = 10
    elif any(e in edu for e in ["diploma", "12th"]):
        edu_score = 5
    breakdown["Education"] = edu_score
    score += edu_score

    # ── Experience Score (15 points) ──
    exp = analysis_result["experience_years"]
    if exp >= 5:
        exp_score = 15
    elif exp >= 3:
        exp_score = 10
    elif exp >= 1:
        exp_score = 7
    else:
        exp_score = 3
    breakdown["Experience"] = exp_score
    score += exp_score

    # ❌ REMOVED Job Match Section completely

    return {
        "total_score" : min(score, 100),
        "breakdown"   : breakdown,
        "grade"       : get_grade(score)
    }

def get_grade(score):
    if score >= 80:
        return "🌟 Excellent"
    elif score >= 60:
        return "👍 Good"
    elif score >= 40:
        return "⚠️ Average"
    else:
        return "❌ Needs Improvement"