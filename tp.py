import pandas as pd
ats_data = {
    'ats_score': 73, 
    'grade': 'B', 
    'job_experience_required': 'fresher', 
    'candidate_experience': '1.5 years', 
    'score_breakdown': {'skills': 34, 'experience': 26, 'projects': 11, 'education': 2}, 
    'matched_skills': ['Python', 'Excel', 'SQL', 'Power BI'], 
    'missing_skills': ['Java'], 
    'strengths': ['Hands-on experience with end-to-end AI systems using Python, ML, NLP, and computer vision', 'Practical analytical skills', 'Capstone projects for real-time project exposure'], 
    'weaknesses': [], 'reasons': []
            }

# ATS SCORE
data = {k:ats_data.get(k,'') for k in ['ats_score','grade','job_experience_required',
                                       'candidate_experience','score_breakdown','matched_skills',
                                       'missing_skills','strengths','weaknesses','reasons'
                                       ]}
df = pd.DataFrame(data.items(), columns=["Field", "Value"])
print(df)