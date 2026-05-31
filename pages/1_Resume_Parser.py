import streamlit as st  
import pandas as pd 
from utils.text_decor import head_formatting, sub_head_formatting
from utils.read_resume import read_resume
from utils.get_details import extract_resume_features

# ── Header ─────────────────────────────────────────────────
st.markdown(head_formatting(
    "Resume Parser",
    "#B55100", "#CA5B00", "#FF9437",
    font="Inter",
    font_size="3.5rem",
    weight="800",
    letter_spacing="-1px"
), unsafe_allow_html=True)

st.markdown("<p style='font-size:16px; color:gray;'>Upload your resume and let AI extract key information instantly.</p>", unsafe_allow_html=True)
st.divider()

# ── Feature Cards ──────────────────────────────────────────
c1, c2, c3 = st.columns(3)
with c1:
    st.info("📊 **ATS Score**\n\nMatch your resume against any job description")
with c2:
    st.success("💼 **Job Matches**\n\nFind live job openings that fit your profile")
with c3:
    st.warning("🎯 **Interview Prep**\n\nGet role-specific questions based on your resume")

st.divider()

# ── Upload ─────────────────────────────────────────────────
file = st.file_uploader("📂 Upload your resume", type=['.pdf', '.docx'])

if not file:
    st.markdown("""
        <div style='text-align:center; padding:40px; color:gray;'>
            <h3>👆 Upload your resume to get started</h3>
            <p>Supported formats: PDF, DOCX</p>
        </div>
    """, unsafe_allow_html=True)
    st.stop()

# ── Parse ──────────────────────────────────────────────────
with st.spinner("📖 Reading resume..."):
    text = read_resume(file)
with st.spinner("🤖 Extracting features..."):
    res = extract_resume_features(text)

st.session_state["resume_data"] = res
for key in ['job_data', 'ats_results', 'questions']:
    st.session_state.pop(key, None)

st.success("✅ Resume parsed successfully!")

# ── Metrics Row ────────────────────────────────────────────
skills_count  = len(res.get("skills", []))
exp_count     = len(res.get("experience", []))
projects_count= len(res.get("projects", []))
certs_count   = len(res.get("certifications", []))

m1, m2, m3, m4 = st.columns(4)
m1.metric("🛠 Skills",         skills_count)
m2.metric("💼 Experience",     f"{exp_count} roles")
m3.metric("🚀 Projects",       projects_count)
m4.metric("📜 Certifications", certs_count)

st.divider()

# ── Basic Info ─────────────────────────────────────────────
st.markdown("### 👤 Basic Info")
basic = {k: res.get(k, "") for k in ["name", "email", "phone", "summary"]}
st.table(pd.DataFrame(basic.items(), columns=["Field", "Value"]))

# ── Skills ─────────────────────────────────────────────────
st.markdown("### 🛠 Skills")
skills = res.get("skills", [])
if skills:
    pills_html = " ".join([
        f"<span style='background:#FF9437;color:white;padding:4px 12px;border-radius:20px;font-size:13px;margin:3px;display:inline-block'>{s}</span>"
        for s in skills
    ])
    st.markdown(pills_html, unsafe_allow_html=True)
st.divider()

# ── Experience ─────────────────────────────────────────────
st.markdown("### 💼 Experience")
st.table(pd.DataFrame(res.get("experience", [])))
st.divider()

# ── Education ──────────────────────────────────────────────
st.markdown("### 🎓 Education")
st.table(pd.DataFrame(res.get("education", [])))
st.divider()

# ── Certifications ─────────────────────────────────────────
if res.get("certifications"):
    st.markdown("### 📜 Certifications")
    st.table(pd.DataFrame(res.get("certifications", []), columns=["Certification"]))
    st.divider()

# ── Projects ───────────────────────────────────────────────
if res.get("projects"):
    st.markdown("### 🚀 Projects")
    st.table(pd.DataFrame(res.get("projects", [])))