import streamlit as st
from utils.agents import search_job, JobList, get_interview_question

if "resume_data" not in st.session_state:
    st.warning("Resume data not found. Please upload your resume in 'Resume Parser' page.")
    st.stop()

data = st.session_state['resume_data']

st.header("💼 Jobs Found For Your Domain",text_alignment='center')

if "job_data" not in st.session_state:
    with st.spinner("🔍 Searching for jobs..."):
        st.session_state['job_data'] = search_job(resume_data=data)  # call ONCE, save it

job_res: JobList = st.session_state['job_data']  # always read from session

cols = st.columns(5)
for idx, job in enumerate(job_res.jobs):
    with cols[idx]:
        st.markdown(f"""
            <div style="
                border: 1px dashed #818080;
                border-radius: 10px;
                padding: 12px;
                height: 200px;
                display: flex;
                flex-direction: column;
                justify-content: space-between;
            ">
                <div>
                    <p style='font-size:13px; font-weight:bold; margin:0'>{job.title}</p>
                    <p style='font-size:12px; margin:4px 0'>🏢 {job.company}</p>
                    <p style='font-size:12px; margin:4px 0'>📍 {job.location}</p>
                </div>
                <a href='{job.apply_link}' target='_blank' style='
                    display:block;
                    text-align:center;
                    background:#1f77b4;
                    color:white;
                    padding:6px;
                    border-radius:6px;
                    text-decoration:none;
                    font-size:12px;
                '>Apply Now 🔗</a>
            </div>
        """, unsafe_allow_html=True)

st.divider()

st.header(":blue[</>] FREQUENT ASKED INTERVIEW QUESTIONS",text_alignment='center')
if "questions" not in st.session_state:
    questions = get_interview_question(resume_data=data)
    st.session_state['questions'] = questions

questions = st.session_state['questions']
st.write(questions)
st.divider()
st.subheader("ALL THE BEST 👍",text_alignment="center")
st.divider()
col_1, col_2, col_3 = st.columns(3)
with col_1:
    with st.container(border=True):
        st.page_link("Home.py", label="Home", icon="🏚️")
with col_2:
    with st.container(border=True):
        st.page_link("pages/1_Resume_Parser.py", label="Resume Parser", icon="📄")
with col_3:
    with st.container(border=True):
        st.page_link("pages/2_ATS_Score.py", label="ATS Score", icon="🎯")

st.divider()
