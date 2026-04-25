# 🎯 TalentLens AI
### AI-Powered Talent Scouting & Engagement Agent

## 🚀 What it does
TalentLens AI helps recruiters find the best candidates instantly. Paste a Job Description and the AI will:
- Match candidates based on skills and experience
- Simulate conversational outreach to assess interest
- Rank candidates on two dimensions: Match Score and Interest Score
- Provide explainable reasons for every ranking

## 🏗️ Architecture
JD Input → Skill Extractor → Candidate Matcher → Interest Simulator → Ranked Output
## 📊 Scoring Logic
- **Match Score (60% weight):** Skills overlap + Experience + Location match
- **Interest Score (40% weight):** Notice period + Experience level + Location preference
- **Total Score:** (Match × 0.6) + (Interest × 0.4)

## 🛠️ Tech Stack
- **Backend:** Python, FastAPI
- **Frontend:** HTML, CSS, JavaScript
- **Server:** Uvicorn
- **Data:** JSON-based candidate pool

## ⚙️ How to Run Locally
1. Clone the repo:
git clone https://github.com/Harshitha-Devareddy/talentlens-ai.git
2. Install dependencies:
pip install fastapi uvicorn python-dotenv
3. Run the server:
uvicorn main:app --reload
4. Open browser and go to:
http://127.0.0.1:8000
## 📥 Sample Input
We are looking for a Senior Python Developer with 4+ years of experience
in FastAPI, Machine Learning, and SQL. Must be based in Hyderabad or Bangalore.
## 📤 Sample Output
- Aisha Sharma — Match: 85, Interest: 83, Total: 84.2 ⭐ TOP MATCH
- Sneha Reddy — Match: 67, Interest: 80, Total: 72.2
- Rahul Mehta — Match: 55, Interest: 80, Total: 65.0

## 🎯 Submission
- **Hackathon:** Catalyst by deccan.ai
- **Developer:** Harshitha Devareddy