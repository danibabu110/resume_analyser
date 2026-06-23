# analyser.py

import spacy
import re

nlp = spacy.load("en_core_web_sm")

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

# ✅ FIXED NAME EXTRACTION
def extract_name(text):
    doc = nlp(text[:500])
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            name = ent.text.strip()
            if "@" not in name and not name.replace(" ", "").isdigit():
                if 2 <= len(name.split()) <= 4:
                    return name

    lines = [line.strip() for line in text.split("\n") if line.strip()]
    
    if lines:
        first_line = lines[0]
        
        if "@" in first_line:
            for line in lines[1:5]:
                if "@" not in line and not any(c.isdigit() for c in line):
                    cleaned = clean_name(line)
                    if cleaned:
                        return cleaned
            return "Not Found"
        
        cleaned = clean_name(first_line)
        if cleaned:
            return cleaned
    
    return "Not Found"


def clean_name(text):
    text = re.sub(r'[\w\.-]+@[\w\.-]+\.\w+', '', text)
    text = re.sub(r'[\+\(]?[1-9][0-9 .\-\(\)]{8,}[0-9]', '', text)
    text = re.sub(r'[!@#$%^&*()_+={}\[\]|\\:;"\'<>,?/~`]', '', text)
    text = " ".join(text.split())
    
    words = text.split()
    if 2 <= len(words) <= 4:
        if all(w.isalpha() for w in words):
            return text.title()
    
    return None


def extract_email(text):
    emails = re.findall(r'[\w\.-]+@[\w\.-]+\.\w+', text)
    return emails[0] if emails else "Not Found"


def extract_phone(text):
    phones = re.findall(
        r'[\+\(]?[1-9][0-9 .\-\(\)]{8,}[0-9]',
        text
    )
    if phones:
        return phones[0].strip()
    return "Not Found"


def extract_skills(text):
    text_lower = text.lower()
    found = {}
    for category, skills in SKILLS_DB.items():
        matched = [s for s in skills if s in text_lower]
        if matched:
            found[category] = matched
    return found


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


def extract_experience(text):
    experience = re.findall(
        r'(\d+)\+?\s*(?:years?|yrs?)(?:\s*of)?\s*(?:experience)?',
        text.lower()
    )
    if experience:
        return max([int(x) for x in experience])
    return 0


def get_missing_skills(found_skills):
    missing = {}
    for category, skills in SKILLS_DB.items():
        found_in_cat = found_skills.get(category, [])
        missing_in_cat = [s for s in skills if s not in found_in_cat]
        if missing_in_cat:
            missing[category] = missing_in_cat[:3]
    return missing


def analyse_resume(text):
    skills = extract_skills(text)
    return {
        "name"            : extract_name(text),
        "email"           : extract_email(text),
        "phone"           : extract_phone(text),
        "education"       : extract_education(text),
        "experience_years": extract_experience(text),
        "skills"          : skills,
        "missing_skills"  : get_missing_skills(skills)
    }