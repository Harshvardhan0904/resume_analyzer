import json
from agno.agent import Agent
from agno.models.google import Gemini
from agno.tools.websearch import WebSearchTools
from pydantic import BaseModel
from typing import List
from dotenv import load_dotenv

load_dotenv()
MODEL = Gemini(id="gemini-2.5-flash")
class Job(BaseModel):
    title: str
    company: str
    location: str
    apply_link: str

class JobList(BaseModel):
    jobs: List[Job]

def search_job(resume_data: str) -> JobList:
    job_search_agent = Agent(
        model=MODEL,
        tools=[WebSearchTools()],
        description="""You are a job search agent for India-based roles.
        Given a resume, find 5 recent job postings matching the candidate's experience level.
        
        Return ONLY a valid JSON object in this exact format, nothing else:
        {
            "jobs": [
                {
                    "title": "...",
                    "company": "...",
                    "location": "...",
                    "apply_link": "..."
                }
            ]
        }
        Rules:
        - Jobs must be in India only
        - Company name must be clearly mentioned
        - No extra text, no markdown, no code blocks
        """
    )
    
    res = job_search_agent.run(input=f"Resume: {resume_data}")
    content = res.content
    print("Raw content:", content)
    
    # clean markdown code blocks if present
    content = content.strip().removeprefix("```json").removeprefix("```").removesuffix("```").strip()
    
    data = json.loads(content)
    return JobList(**data)

def get_interview_question(resume_data):
    agent = Agent(
        model= MODEL,
        tools= [WebSearchTools()],
        description="Based on the resume provided give atleast 20 most asked interview questions "
        "Dive the question into 4 parts "
        "1 DSA type "
        "2 Core topic of the Job"
        "3 System Desing"
        "4 AI topics"
        "Only return what is asked no extra text, paragrah or explaintion"
    )
    response = agent.run(input= f"Here is the resume {resume_data} and for this give the important interview questions asked")
    response = response.content
    return response