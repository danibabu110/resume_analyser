# analyser.py  ← Replace entire file

import re

# ─────────────────────────────────────
# SKILLS DATABASE
# ─────────────────────────────────────
SKILLS_DB = {
    "Programming"  : ["python", "java", "c++", "javascript", "r", "sql", "php"],
    "ML/AI"        : ["machine learning", "deep learning", "nlp", "computer vision",
                      "tensorflow", "keras", "pytorch", "scikit-learn"],
    "Data"         : ["pandas", "numpy", "matplotlib", "tableau", "power bi",
                      "data analysis", "data visualization", "excel"],
    "Web"          : ["html", "css", "react", "django", "flask", "nodejs"],
    "Cloud"        : ["aws", "azure", "google cloud", "docker", "kubernetes"],
    "Soft Skills"  : ["leadership", "communication", "teamwork",
                      "problem solving", "management"]
}

# ─────────────────────────────────────
# EXTRACT NAME (No spaCy - Regex Only)
# ─────────────────────────────────────
def extract_name(text):
    lines = [line.strip() for line in text.split("\n") if line.strip()]

    for line in lines[:5]:  # Check first 5 lines only
        # Skip if line has email
        if "@" in line:
            continue
        # Skip if line has phone number
        if re.search(r'\d{10}', line):
            continue
        # Skip if line is too long (not a name)
        if len(line) > 40:
            continue
        # Skip if line has special characters
        if re.search(r'[!#$%^&*()_+={}\[\]|\\:;"<>?/~`]', line):
            continue

        # Clean the line
        cleaned = re.sub(r'[,.\-]', '', line).strip()

        # Check if it looks like a name (2-4 words, all alphabetic)
        words = cleaned.split()
        if 2 <= len(words) <= 4:
            if all(w.isalpha() for w in words):
                return cleaned.title()

    return "Not Found"

# ─────────────────────────────────────
# EXTRACT EMAIL
# ─────────────────────────────────────
def extract_email(text):
    emails = re.findall(r'[\w\.-]+@[\w\.-]+\.\w+', text)
    return emails[0] if emails else "Not Found"

# ─────────────────────────────────────
# EXTRACT PHONE
# ─────────────────────────────────────
def extract_phone(text):
    phones = re.findall(
        r'[\+\(]?[1-9][0-9 .\-\(\)]{8,}[0-9]',
        text
    )
    if phones:
        return phones[0].strip()
    return "Not Found"

# ─────────────────────────────────────
# EXTRACT SKILLS
# ─────────────────────────────────────
def extract_skills(text):
    text_lower = text.lower()
    found = {}
    for category, skills in SKILLS_DB.items():
        matched = [s for s in skills if s in text_lower]
        if matched:
            found[category] = matched
    return found

# ─────────────────────────────────────
# EXTRACT EDUCATION
# ─────────────────────────────────────
def extract_education(text):
    education_keywords = [
        "b.tech", "btech", "b.e", "be", "m.tech", "mtech",
        "mba", "bsc", "msc", "phd", "bachelor", "master",
        "degree", "diploma", "12th", "10th", "graduation"
    ]
    text_lower = text.lower()
    found_edu = []
    for keyword in education_keywords:
        if keyword in text_lower:
            found_edu.append(keyword.upper())
    return found_edu if found_edu else ["Not Found"]

# ─────────────────────────────────────
# EXTRACT EXPERIENCE
# ─────────────────────────────────────
def extract_experience(text):
    experience = re.findall(
        r'(\d+)\+?\s*(?:years?|yrs?)(?:\s*of)?\s*(?:experience)?',
        text.lower()
    )
    if experience:
        return max([int(x) for x in experience])
    return 0

# ─────────────────────────────────────
# MISSING SKILLS
# ─────────────────────────────────────
def get_missing_skills(found_skills):
    missing = {}
    for category, skills in SKILLS_DB.items():
        found_in_cat = found_skills.get(category, [])
        missing_in_cat = [s for s in skills if s not in found_in_cat]
        if missing_in_cat:
            missing[category] = missing_in_cat[:3]
    return missing

# ─────────────────────────────────────
# MAIN ANALYSE FUNCTION
# ─────────────────────────────────────
def analyse_resume(text):
    skills = extract_skills(text)
    return {
        "name"             : extract_name(text),
        "email"            : extract_email(text),
        "phone"            : extract_phone(text),
        "education"        : extract_education(text),
        "experience_years" : extract_experience(text),
        "skills"           : skills,
        "missing_skills"   : get_missing_skills(skills)
    }