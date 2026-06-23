# app.py

import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import tempfile, os

from resume_parser import get_resume_text
from analyser import analyse_resume, SKILLS_DB
from scorer import calculate_score

# ── Page Config ──
st.set_page_config(
    page_title = "AI Resume Analyser",
    page_icon  = "📄",
    layout     = "wide"
)

# ── Custom CSS ──
st.markdown("""
    <style>
    .main-title {
        font-size: 42px;
        font-weight: bold;
        color: #2E86AB;
        text-align: center;
    }
    .score-box {
        background: #f0f8ff;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        font-size: 28px;
        font-weight: bold;
        color: #2E86AB;
    }
    .skill-tag {
        background: #28a745;
        color: white;
        padding: 4px 10px;
        border-radius: 15px;
        margin: 3px;
        display: inline-block;
        font-size: 13px;
    }
    .missing-tag {
        background: #dc3545;
        color: white;
        padding: 4px 10px;
        border-radius: 15px;
        margin: 3px;
        display: inline-block;
        font-size: 13px;
    }
    </style>
""", unsafe_allow_html=True)

# ── Title ──
st.markdown('<p class="main-title">📄 AI Resume Analyser</p>',
            unsafe_allow_html=True)
st.markdown("---")

# ── File Upload ──
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    uploaded_file = st.file_uploader(
        "📤 Upload Resume",
        type=["pdf", "docx"],
        help="Supports PDF and DOCX formats"
    )

# ── Analysis ──
if uploaded_file is not None:

    with st.spinner("🔍 Analysing your resume..."):

        file_type   = uploaded_file.name.split(".")[-1].lower()
        resume_text = get_resume_text(uploaded_file, file_type)
        analysis    = analyse_resume(resume_text)
        score_data  = calculate_score(analysis)        # ✅ No job_description

    st.success("✅ Analysis Complete!")
    st.markdown("---")

    # ── Row 1 - Basic Info ──
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("👤 Name",       analysis["name"])
    with col2:
        st.metric("📧 Email",      analysis["email"])
    with col3:
        st.metric("📞 Phone",      analysis["phone"])
    with col4:
        st.metric("💼 Experience", f"{analysis['experience_years']} Years")

    st.markdown("---")

    # ── Row 2 - Score + Breakdown ──
    col1, col2 = st.columns([1, 2])

    with col1:
        st.markdown(f"""
            <div class="score-box">
                🏆 Resume Score<br>
                {score_data['total_score']}/100<br>
                <small>{score_data['grade']}</small>
            </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        st.subheader("🎓 Education")
        for edu in analysis["education"]:
            st.write(f"✅ {edu}")

    with col2:
        st.subheader("📊 Score Breakdown")
        breakdown = score_data["breakdown"]
        fig = go.Figure(go.Bar(
            x = list(breakdown.values()),
            y = list(breakdown.keys()),
            orientation  = 'h',
            marker_color = ['#2E86AB', '#28a745', 
                           '#ffc107', '#dc3545'][:len(breakdown)]
        ))
        fig.update_layout(
            height = 250,
            margin = dict(l=0, r=0, t=0, b=0),
            xaxis  = dict(range=[0, 50])
        )
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # ── Row 3 - Skills Found ──
    st.subheader("✅ Skills Found")
    if analysis["skills"]:
        for category, skills in analysis["skills"].items():
            st.write(f"**{category}:**")
            skill_html = ""
            for skill in skills:
                skill_html += f'<span class="skill-tag">{skill}</span>'
            st.markdown(skill_html, unsafe_allow_html=True)
            st.write("")
    else:
        st.warning("⚠️ No matching skills found!")

    st.markdown("---")

    # ── Row 4 - Missing Skills ──
    st.subheader("❌ Skills You Should Add")
    if analysis["missing_skills"]:
        for category, skills in analysis["missing_skills"].items():
            st.write(f"**{category}:**")
            miss_html = ""
            for skill in skills:
                miss_html += f'<span class="missing-tag">+ {skill}</span>'
            st.markdown(miss_html, unsafe_allow_html=True)
            st.write("")

    st.markdown("---")

    # ── Row 5 - Radar Chart ──
    st.subheader("📈 Skills Coverage Chart")
    categories = list(SKILLS_DB.keys())
    values = []
    for cat in categories:
        found = len(analysis["skills"].get(cat, []))
        total = 7
        values.append(min(found / total * 100, 100))

    fig_radar = go.Figure(go.Scatterpolar(
        r          = values + [values[0]],
        theta      = categories + [categories[0]],
        fill       = 'toself',
        name       = 'Skills',
        line_color = '#2E86AB'
    ))
    fig_radar.update_layout(
        polar  = dict(radialaxis=dict(visible=True, range=[0, 100])),
        height = 400
    )
    st.plotly_chart(fig_radar, use_container_width=True)

    st.markdown("---")

    # ── Raw Text ──
    with st.expander("📃 View Raw Extracted Text"):
        st.text(resume_text)

else:
    st.markdown("""
        <div style='text-align: center; padding: 50px; color: gray;'>
            <h2>👆 Upload your resume to get started!</h2>
            <p>Supports PDF and DOCX formats</p>
            <p>✅ Completely FREE | 🔒 Privacy Safe | ⚡ Instant Results</p>
        </div>
    """, unsafe_allow_html=True)