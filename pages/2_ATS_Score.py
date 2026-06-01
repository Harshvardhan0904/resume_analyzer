import streamlit as st
import pandas as pd
from utils.get_details import calculate_ats

st.set_page_config(page_title="ATS Calculator", page_icon="🎯", layout="wide")

st.markdown("""
    <style>
        .metric-card {
            background: linear-gradient(135deg, #1e3a5f, #2d6a9f);
            padding: 20px;
            border-radius: 12px;
            text-align: center;
            color: white;
        }
        .section-header {
            font-size: 20px;
            font-weight: 700;
            padding: 8px 16px;
            border-radius: 8px;
            margin-bottom: 10px;
        }
        .tag {
            display: inline-block;
            padding: 5px 14px;
            border-radius: 20px;
            font-size: 14px;
            font-weight: 500;
            margin: 4px;
        }
    </style>
""", unsafe_allow_html=True)


# ── Guard ──────────────────────────────────────────────────────────────────────


# ── Header ─────────────────────────────────────────────────────────────────────
st.markdown("# :blue[ATS Score Calculator]")
st.markdown("Paste a job description below to instantly check how well your resume matches.")
st.divider()

if "resume_data" not in st.session_state:
    st.warning("Resume data not found. Please upload your resume first.")
    st.stop()

data = st.session_state["resume_data"]
box =st.checkbox("Use AI + Custom Job description")
# ── JD Input ───────────────────────────────────────────────────────────────────
if box:
    jd_input = st.text_area(
        label="Job Description",
        placeholder="Paste the full job description here...",
        height=200,
    )
    st.button("calculate ATS")

    if not jd_input:
        st.info("👆 Enter a job description above to calculate your ATS score.")
        st.stop()

    # ── Calculate ──────────────────────────────────────────────────────────────────
    if "ats_data" not in st.session_state:
        with st.spinner("🔍 Analyzing your resume against the job description..."):
            output = calculate_ats(resume_text=data, job_desc=jd_input)
            st.session_state['ats_data'] = output
    output = st.session_state['ats_data']

    st.success("✅ Analysis complete!")
    st.divider()

    # ── Row 1 — Key Metrics ────────────────────────────────────────────────────────
    ats_score     = output.get("ats_score", "N/A")
    grade         = output.get("grade", "N/A")
    job_exp       = output.get("job_experience_required", "N/A")
    candidate_exp = output.get("candidate_experience", "N/A")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(label="🏆 ATS Score", value=f"{ats_score}%")
    with col2:
        st.metric(label="🎓 Grade", value=grade)
    with col3:
        st.metric(label="💼 Job Exp Required", value=job_exp)
    with col4:
        st.metric(label="🧑‍💻 Your Experience", value=candidate_exp)

    st.divider()

    # ── Row 2 — Score Breakdown + Matched Skills ───────────────────────────────────
    col_left, col_right = st.columns(2)

    with col_left:
        with st.container(border=True):
            col1 ,col2 = st.columns(2)
            with col1:
                st.markdown("#### 📊 Score Breakdown")
                breakdown_data = output.get("score_breakdown", {})
                if breakdown_data:
                    breakdown_df = pd.DataFrame(
                        breakdown_data.items(), columns=["Parameter", "Score"]
                    )
                    # Progress-bar style table
                    for _, row in breakdown_df.iterrows():
                        label = row["Parameter"]
                        score = row["Score"]
                        try:
                            pct = float(score)
                        except (ValueError, TypeError):
                            pct = 0
                        st.markdown(f"**{label}**")
                        st.progress(min(pct / 100, 1.0), text=f"{score}")
                else:
                    st.info("No breakdown data available.")
            with col2:
                st.markdown("### Points breakdown (100)")
                data = {
                    "Skills": 40,
                    "Experiance":30,
                    "Projects":20,
                    "Education":10

                }
                table_data = pd.DataFrame(data.items(),columns=["Parameter","Max score"])
                st.table(table_data)

    with col_right:
        with st.container(border=True):
            st.markdown("#### ✅ Matched Skills")
            matched = output.get("matched_skills", [])
            if matched:
                # Render as coloured pills
                pills_html = "".join(
                    f'<span class="tag" style="background:#d4edda;color:#155724;">{s}</span>'
                    for s in matched
                )
                st.markdown(pills_html, unsafe_allow_html=True)
            else:
                st.info("No matched skills found.")

    st.divider()

    # ── Row 3 — Missing Skills + Suggestions ──────────────────────────────────────
    col_miss, col_sug = st.columns(2)

    with col_miss:
        st.markdown("#### ❌ Missing Skills")
        missing = output.get("missing_skills", [])
        if missing:
            pills_html = "".join(
                f'<span class="tag" style="background:#f8d7da;color:#721c24;">{s}</span>'
                for s in missing
            )
            st.markdown(pills_html, unsafe_allow_html=True)
        else:
            st.success("No critical skills missing — great match!")

    with col_sug:
        st.markdown("#### 💡 Suggestions to Improve")
        suggestions = output.get("Suggestion", [])
        if suggestions:
            for i, tip in enumerate(suggestions, 1):
                st.markdown(f"{i}. {tip}")
        else:
            st.info("No suggestions available.")

    st.divider()
    st.info("Check out Job posting page for recent jobs posted related to you resume")
    st.divider()

    # ── Download Report ────────────────────────────────────────────────────────────
    report_lines = [
        f"ATS Score     : {ats_score}%",
        f"Grade         : {grade}",
        f"Job Exp Reqd  : {job_exp}",
        f"Candidate Exp : {candidate_exp}",
        "",
        "Score Breakdown:",
        *[f"  {k}: {v}" for k, v in output.get("score_breakdown", {}).items()],
        "",
        "Matched Skills : " + ", ".join(output.get("matched_skills", [])),
        "Missing Skills : " + ", ".join(output.get("missing_skills", [])),
        "",
        "Suggestions:",
        *[f"  {i+1}. {s}" for i, s in enumerate(output.get("Suggestion", []))],
    ]
    report_text = "\n".join(report_lines)

    st.download_button(
        label="⬇️ Download ATS Report",
        data=report_text,
        file_name="ats_report.txt",
        mime="text/plain",
        use_container_width=False,

    )

st.selectbox("Select interested feild",("Web dev","Data science","AI Engineer","Data Analyst"),accept_new_options=True)

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
        st.page_link("pages/3_Job_Postings.py", label="Job Postings", icon="💼")