import json
import os


def _get_gemini_key():
    try:
        import streamlit as st
        key = st.secrets.get("GOOGLE_API_KEY") or os.getenv("GOOGLE_API_KEY")
        if not key:
            st.error("❌ GOOGLE_API_KEY not found. Add it in App Settings → Secrets.")
        return key
    except Exception:
        return os.getenv("GOOGLE_API_KEY")


def _gemini_generate(prompt: str, system: str) -> str:
    from google import genai
    from google.genai import types

    client = genai.Client(api_key=_get_gemini_key())
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config=types.GenerateContentConfig(
            system_instruction=system,
            temperature=0.1,
        ),
    )
    return response.text


def _parse_json(raw: str) -> dict:
    """Strip markdown fences if model adds them, then parse JSON."""
    raw = raw.strip()
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
        raw = raw.strip()
    return json.loads(raw)


# ── Task 1: Extract Resume Features ───────────────────────────────────────────
def extract_resume_features(resume_text: str) -> dict:

    system = "You are a resume parser. Output only raw JSON. No markdown. No explanation. No code fences."

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

    raw = _gemini_generate(prompt, system)
    return _parse_json(raw)


# ── Task 2: Calculate ATS Score ───────────────────────────────────────────────
def calculate_ats(resume_text: str, job_desc: str) -> dict:

    system = "You are an ATS calculator. Output only raw JSON. No markdown. No explanation. No code fences."

    prompt = f"""You are an expert ATS (Applicant Tracking System) evaluator. Score how well a resume matches a job description.

BASIC RULES:
- Do NOT do pure keyword matching — judge semantic similarity
- Treat case-insensitive duplicates as the same (python == Python)
- Similar tools count as equivalent (e.g. Power BI and Tableau are both visualization tools)
- Give actionable suggestions for what the candidate can add/fix to improve their score

STEP 1 — ANALYZE THE JOB DESCRIPTION:
- Required skills (must-have)
- Preferred skills (nice-to-have)
- Minimum years of experience (if not mentioned → assume fresher role)
- Required qualifications / degrees
- Key responsibilities

STEP 2 — ANALYZE THE RESUME:
1. Skills — match against required + preferred skills from JD
2. Experience — match roles, responsibilities, years
3. Projects — check for relevant tech stack or domain overlap
4. Education — check if qualification requirement is met

STEP 3 — SCORING (total = 100):
- Skills match     : 40 pts (required > preferred in weight)
- Experience match : 30 pts (years + relevance)
- Projects         : 20 pts (tech stack, domain, impact)
- Education        : 10 pts (degree, field of study)

Deduct points for: missing required skills, experience gap, unrelated domain.
Do NOT deduct if the role is fresher-level and candidate has 0 experience.

STEP 4 — Return strict JSON only. No markdown. No extra text.

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

    raw = _gemini_generate(prompt, system)
    return _parse_json(raw)