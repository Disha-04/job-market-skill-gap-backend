from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd

app = FastAPI(title="Job Market Skill Gap API")
@app.get("/")
def root():
    return {"message": "Backend is running!"}

# Allow frontend to call the API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load CSV
df = pd.read_csv("outputs_roles_with_skills.csv")

@app.get("/health")
def health():
    return {"status": "ok", "rows": len(df)}

@app.get("/api/summary")
def summary():
    da = df[df["role_category"] == "Data Analyst"]
    ai = df[df["role_category"] == "AI / ML Engineer"]

    return {
        "total_jobs": len(df),
        "data_analyst_count": len(da),
        "ai_ml_count": len(ai),
    }

@app.get("/api/skills")
def skills():
    skill_map = {}

    for row in df["skills_found"].dropna():
        skills = row.strip("[]").replace("'", "").split(",")
        for s in skills:
            s = s.strip()
            if s:
                skill_map[s] = skill_map.get(s, 0) + 1

    top = sorted(skill_map.items(), key=lambda x: x[1], reverse=True)
    return {"top_skills": top[:15]}