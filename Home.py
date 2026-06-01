import streamlit as st
from utils.text_decor import head_formatting,sub_head_formatting
import base64
st.set_page_config(page_title="ResumeIQ", page_icon="📄", layout="wide",initial_sidebar_state='auto')


st.markdown(head_formatting(
    "Resume.IQ",
    "#2200FF", "#0574D6","#036AE8",
    font="Bebas Neue",
    font_size="5.5rem",
    weight="800",
    letter_spacing="−1px"
), unsafe_allow_html=True)

# Subtitle — softer, smaller, not gradient
st.markdown(sub_head_formatting(text="Finding the right job can be overwhelming. Candidates often spend hours optimizing resumes, searching for opportunities, and preparing for interviews. Our AI-powered Career Assistant streamlines this journey by providing ATS analysis, personalized job recommendations, and skill-based interview preparation in one place",
                                color="rgb(136, 136, 136)"), 
                                unsafe_allow_html=True)

st.divider()

# Section label
st.markdown("### Navigate using the sidebar to get started",text_alignment='center')

# Feature cards
col_1, col_2, col_3 = st.columns(3)
with col_1:
    st.page_link("pages/1_Resume_Parser.py", label="Resume Parser", icon="📄",)
with col_2:
    st.page_link("pages/2_ATS_Score.py", label="ATS Score", icon="🎯")
with col_3: 
    st.page_link("pages/3_Job_Postings.py", label="Job Postings", icon="💼")
