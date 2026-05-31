import streamlit as st
from utils.text_decor import head_formatting,sub_head_formatting
st.set_page_config(page_title="ResumeIQ", page_icon="📄", layout="wide")

# Main title
st.markdown(head_formatting(
    "ResumeIQ",
    "#17B517", "#38E638","#80EFCA",
    font="Inter",
    font_size="3.5rem",
    weight="800",
    letter_spacing="−1px"
), unsafe_allow_html=True)

# Subtitle — softer, smaller, not gradient
st.markdown(sub_head_formatting(text="Your AI-powered career assistant",
                                color="#17B517"), 
                                unsafe_allow_html=True)

st.divider()

# Section label
st.markdown(sub_head_formatting(text="Navigate using the sidebar to get started",
                                color="#00FF99",
                                font = "Montserrat",font_weight = '700'),
                                unsafe_allow_html=True)

# Feature cards
col_1, col_2, col_3, col_4 = st.columns(4)
with col_1:
    st.page_link("pages/1_Resume_Parser.py", label="Resume Parser", icon="📄")
with col_2:
    st.page_link("pages/2_ATS_Score.py", label="ATS Score", icon="🎯")
with col_3: 
    st.page_link("pages/3_Job_Postings.py", label="Job Postings", icon="💼")
