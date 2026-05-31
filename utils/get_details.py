import ollama
import json
from utils.read_resume import read_resume

#task 1
def extract_resume_features(resume_text):
    prompt = f"""You are a precise resume parser. Extract information from the resume below and return ONLY a valid JSON object with no markdown, no code blocks, no extra text before or after.

Rules:
- For skills: dig into every subsection (e.g. "Programming Languages", "Frameworks", "Tools", "Soft Skills") and flatten all skills into a single list
- If a field is missing, use null for strings or [] for arrays
- Keep descriptions concise but complete
- Extract ALL certifications and projects, even if briefly mentioned

Return this exact structure:
{{
    "name": "",
    "email": "",
    "phone": "",
    "linkedin": "",
    "summary": "",
    "skills": [],
    "experience": [
        {{
            "company": "",
            "role": "",
            "duration": "",
            "description": ""
        }}
    ],
    "education": [
        {{
            "institution": "",
            "degree": "",
            "year": ""
        }}
    ],
    "certifications": [],
    "projects": [
        {{
            "name": "",
            "description": "",
            "technologies": []
        }}
    ]
}}

Resume:
{resume_text}
"""

    response = ollama.chat(
        model="llama3.2",
        messages=[
            {
                "role": "system",
                "content": "You are a resume parser. Output only raw JSON. No markdown. No explanation. No code fences."
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    raw = response["message"]["content"].strip()

    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]

    clean = raw[raw.find("{"):raw.rfind("}") + 1]
    data = json.loads(clean)
    return data

#task 2 - Calculate ats score
def calculate_ats(resume_text, job_desc):
    prompt = f"""You are an expert ATS (Applicant Tracking System) evaluator. Your job is to score how well a resume matches a job description.
BASIC RULE 
    - Done match keyword by keyword match if the things are similar 
    - For same word or skill they are same if they are in lower case or upper case dont mark them sprate
    - Some skills are similar (ex : Power BI and Tablue are same since the both are used for visualization)
    - Give suggestion for improvement like what things can be fixed in resume to make it more better for the Job description
STEP 1 — ANALYZE THE JOB DESCRIPTION:
Extract the following from the job description:
- Required skills (must-have)
- Preferred skills (nice-to-have)
- Minimum years of experience required (if not mentioned, assume  = fresher role)
- Required qualifications / degrees
- Key responsibilities (to match against experience)

STEP 2 — ANALYZE THE RESUME IN THIS ORDER:
1. Skills — match against required and preferred skills from JD
2. Experience — match roles, responsibilities, and years of experience
3. Projects — check for relevant tech stack or domain overlap
4. Education — check if qualification requirement is met

STEP 3 — SCORING BREAKDOWN (total = 100):
- Skills match         : 40 points  (required skills carry more weight than preferred)
- Experience match     : 30 points  (years + relevance of past roles)
- Projects relevance   : 20 points  (tech stack, domain, impact)
- Education match      : 10 points  (degree, field of study)

Deduct points for:
- Skills that are in the Job description but not in resume uploded by the user
- Experience gap (e.g. JD needs 3 years, candidate has 1) but if its for fresher and user has more then give point dont deduct
- Unrelated domain or industry

STEP 4 — RETURN strict JSON only. No markdown. No explanation outside the JSON.

{{
    "ats_score": <integer 0-100>,
    "grade": "<A / B / C / D / F>",
    "job_experience_required": "<e.g. 2 years / fresher>",
    "candidate_experience": "<e.g. 1.5 years / fresher>",
    "score_breakdown": {{
        "skills": <0-40>,
        "experience": <0-30>,
        "projects": <0-20>,
        "education": <0-10>
    }},
    "matched_skills": [],
    "missing_skills": [],
    "strengths": [],
    "weaknesses": [],
    "Suggestion": []
}}

Resume:
{resume_text}

Job Description:
{job_desc}
"""

    response = ollama.chat(
        model="llama3.2",
        messages=[
            {
                "role": "system",
                "content": "You are a ATS calculator. Output only raw JSON. No markdown. No explanation. No code fences."
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    raw = response["message"]["content"].strip()

    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]

    clean = raw[raw.find("{"):raw.rfind("}") + 1]
    data = json.loads(clean)
    return data