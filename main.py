from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel
import json
import os
import re

app = FastAPI()

with open("candidates.json", "r") as f:
    candidates = json.load(f)

class JDRequest(BaseModel):
    job_description: str

def calculate_match(candidate, jd_lower):
    skills = [s.lower() for s in candidate["skills"]]
    matching = [s for s in skills if s in jd_lower]
    skill_score = min(60, len(matching) * 15)
    exp_score = min(25, candidate["experience_years"] * 3)
    location_score = 10 if any(loc in jd_lower for loc in [candidate["location"].split(",")[0].lower()]) else 5
    total = skill_score + exp_score + location_score
    return min(98, total), matching

def calculate_interest(candidate):
    base = 65
    if candidate["notice_period"] == "15 days":
        base += 15
    elif candidate["notice_period"] == "30 days":
        base += 10
    elif candidate["notice_period"] == "45 days":
        base += 5
    if candidate["experience_years"] >= 5:
        base += 8
    return min(98, base)

def generate_conversation(candidate, jd):
    role = candidate["title"]
    name = candidate["name"].split()[0]
    notice = candidate["notice_period"]
    salary = candidate["expected_salary"]
    
    conversations = [
        f"Recruiter: Hi {name}! I came across your profile and think you'd be a great fit for a {role} position we have open. Are you currently exploring opportunities?\n"
        f"Candidate: Hi! Thanks for reaching out. Yes, I'm selectively open to the right opportunity. Could you tell me more about the role?\n"
        f"Recruiter: Absolutely! It's a fantastic role with great growth potential. Your skills in {', '.join(candidate['skills'][:3])} are exactly what we need. The compensation is also very competitive.\n"
        f"Candidate: That does sound interesting! I'm currently at {salary} and my notice period is {notice}. If the role and company are the right fit, I'd love to have a detailed conversation."
    ]
    return conversations[0]

def get_match_reason(candidate, matching_skills, match_score):
    name = candidate["name"].split()[0]
    if match_score >= 75:
        return f"{name} is an excellent match with {len(matching_skills)} directly relevant skills ({', '.join(matching_skills[:3])}) and {candidate['experience_years']} years of solid experience."
    elif match_score >= 50:
        return f"{name} is a good match with {len(matching_skills)} relevant skills and {candidate['experience_years']} years of experience, though some key requirements may need upskilling."
    else:
        return f"{name} has {candidate['experience_years']} years of experience but only {len(matching_skills)} skills directly match the job requirements."

@app.get("/")
def read_root():
    return FileResponse("index.html")

@app.post("/analyze")
def analyze(request: JDRequest):
    jd = request.job_description
    jd_lower = jd.lower()
    results = []

    for candidate in candidates:
        match_score, matching_skills = calculate_match(candidate, jd_lower)
        interest_score = calculate_interest(candidate)
        total_score = round((match_score * 0.6) + (interest_score * 0.4), 1)
        match_reason = get_match_reason(candidate, matching_skills, match_score)
        conversation = generate_conversation(candidate, jd)

        results.append({
            "name": candidate["name"],
            "title": candidate["title"],
            "skills": candidate["skills"],
            "experience": candidate["experience_years"],
            "location": candidate["location"],
            "notice_period": candidate["notice_period"],
            "expected_salary": candidate["expected_salary"],
            "match_score": match_score,
            "interest_score": interest_score,
            "total_score": total_score,
            "match_reason": match_reason,
            "conversation": conversation
        })

    results.sort(key=lambda x: x["total_score"], reverse=True)
    return {"candidates": results}