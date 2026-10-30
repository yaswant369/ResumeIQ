from __future__ import annotations

from html import escape
from io import BytesIO
from pathlib import Path

import streamlit as st
from pypdf import PdfReader

from resume_engine import analyze_resume


st.set_page_config(
    page_title="ResumeIQ | Candidate screening",
    page_icon=":material/person_search:",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@500;600;700;800&display=swap');
    :root {
        --line: color-mix(in srgb, currentColor 16%, transparent);
        --teal: #087e72;
        --coral: #e77e63;
    }
    html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
    .stApp { background: transparent; }
    [data-testid="stHeader"] { background: transparent; }
    [data-testid="stSidebar"] { background: color-mix(in srgb, currentColor 4%, transparent); border-right: 1px solid var(--line); }
    [data-testid="stSidebar"] > div { padding-top: 1.4rem; }
    h1, h2, h3 { font-family: 'Manrope', sans-serif !important; color: inherit; letter-spacing: 0 !important; }
    h1 { font-size: 2rem !important; font-weight: 800 !important; }
    h2 { font-size: 1.35rem !important; font-weight: 700 !important; }
    p, label, [data-testid="stMarkdownContainer"] { letter-spacing: 0 !important; overflow-wrap: anywhere; }
    .brand { display:flex; align-items:center; gap:10px; margin: 0 0 1.7rem 0; }
    .brand-mark { width:34px; height:34px; display:grid; place-items:center; border-radius:9px; background:var(--teal); color:white; font:800 17px 'Manrope'; }
    .brand-name { font:800 19px 'Manrope'; letter-spacing:0 !important; }
    .brand-name span { color:var(--teal); }
    .eyebrow { color:inherit; opacity:.76; text-transform:uppercase; font-weight:700; font-size:.72rem; }
    .intro { color:inherit; opacity:.76; margin-top:-.55rem; margin-bottom:1.55rem; }
    .metric { background:color-mix(in srgb, currentColor 4%, transparent); color:inherit; border:1px solid var(--line); border-radius:8px; padding:16px 18px; min-height:104px; }
    .metric-label { color:inherit; opacity:.76; font-size:.78rem; font-weight:600; }
    .metric-value { font:800 1.65rem 'Manrope'; color:inherit; margin-top:5px; }
    .metric-note { color:inherit; opacity:.72; font-size:.74rem; margin-top:2px; }
    .section-heading { display:flex; justify-content:space-between; align-items:baseline; margin:1.6rem 0 .35rem; }
    .candidate { background:color-mix(in srgb, currentColor 4%, transparent); color:inherit; border:1px solid var(--line); border-radius:8px; padding:16px 18px; margin:10px 0; }
    .candidate-top { display:flex; justify-content:space-between; align-items:center; gap:16px; flex-wrap:wrap; }
    .candidate-top > div:first-child { flex:1 1 12rem; min-width:0; }
    .candidate-name { font:700 1rem 'Manrope'; overflow-wrap:anywhere; }
    .candidate-meta { color:inherit; opacity:.72; font-size:.78rem; margin-top:3px; }
    .score { color:inherit; font:800 1.25rem 'Manrope'; white-space:nowrap; }
    .score-track { height:6px; background:color-mix(in srgb, currentColor 14%, transparent); border-radius:8px; margin:13px 0 10px; overflow:hidden; }
    .score-fill { height:100%; background:var(--teal); border-radius:8px; }
    .skill-label { color:inherit; opacity:.76; font-size:.72rem; font-weight:700; text-transform:uppercase; }
    .skill-list { color:inherit; font-size:.82rem; margin-top:4px; overflow-wrap:anywhere; }
    .notice { border-left:3px solid var(--coral); padding:9px 12px; background:color-mix(in srgb, var(--coral) 12%, transparent); color:inherit; font-size:.82rem; line-height:1.5; overflow-wrap:anywhere; border-radius:0 6px 6px 0; }
    div.stButton > button[kind="primary"] { background:var(--teal); border:0; border-radius:6px; min-height:44px; font-weight:700; }
    div.stButton > button[kind="primary"]:hover { background:#06675d; border:0; }
    div[data-testid="stMetric"] { background:color-mix(in srgb, currentColor 4%, transparent); border:1px solid var(--line); border-radius:8px; padding:14px; }
    [data-testid="stExpander"] { background:color-mix(in srgb, currentColor 4%, transparent); border:1px solid var(--line); border-radius:7px; }
    @media (max-width: 700px) { h1 { font-size:1.65rem !important; } .candidate { padding:14px; } }
    </style>
    """,
    unsafe_allow_html=True,
)


def extract_pdf_text(file_bytes: bytes) -> str:
    reader = PdfReader(BytesIO(file_bytes))
    return "\n".join(page.extract_text() or "" for page in reader.pages).strip()


def render_candidate(candidate: dict[str, object], rank: int) -> None:
    score = int(candidate["score"])
    name = str(candidate["name"])
    experience = int(candidate["experience"])
    experience_text = f"{experience} years mentioned" if experience else "No experience duration detected"
    safe_name = escape(name)
    matched = candidate["matched_skills"]
    missing = candidate["missing_skills"]
    matched_text = ", ".join(escape(str(skill)) for skill in matched)
    missing_text = ", ".join(escape(str(skill)) for skill in missing)
    improvement_tip = escape(str(candidate["improvement_tip"]))
    st.markdown(
        f"""
        <div class="candidate">
          <div class="candidate-top">
            <div><div class="candidate-name">{rank:02d} &nbsp; {safe_name}</div>
                        <div class="candidate-meta">{experience_text}</div></div>
            <div class="score">{score}%</div>
          </div>
          <div class="score-track"><div class="score-fill" style="width:{score}%"></div></div>
          <div class="skill-label">Skills found in both</div>
          <div class="skill-list">{matched_text or 'No listed skills found in both documents'}</div>
          <div class="skill-label" style="margin-top:10px">Skills to strengthen from the job description</div>
          <div class="skill-list">{missing_text or 'No missing listed skills detected'}</div>
          <div class="skill-label" style="margin-top:10px">Best next step</div>
          <div class="skill-list">{improvement_tip}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    with st.expander(f"Review {name}"):
        st.markdown(f"**Summary:** {candidate['summary']}")
        st.caption(
            f"Text similarity: {candidate['similarity']:.0%} · "
            f"Skill overlap: {candidate['skill_overlap']:.0%} · "
            "Scores are heuristic and should be reviewed by a person."
        )


with st.sidebar:
    st.markdown(
        '<div class="brand"><div class="brand-mark">R</div><div class="brand-name">Resume<span>IQ</span></div></div>',
        unsafe_allow_html=True,
    )
    st.markdown('<div class="eyebrow">New screening</div>', unsafe_allow_html=True)
    job_description = st.text_area(
        "Job description",
        height=240,
        placeholder="Paste the role description, responsibilities, and required skills...",
        help="The description is processed locally by this app and is not sent to an external AI service.",
    )
    uploaded_files = st.file_uploader(
        "Candidate resumes",
        type=["pdf"],
        accept_multiple_files=True,
        help="Upload searchable PDF resumes. Scanned image-only PDFs may not contain extractable text.",
    )
    minimum_score = st.slider("Minimum match score", min_value=0, max_value=100, value=0, step=5)
    analyze_clicked = st.button("Analyze resumes", type="primary", use_container_width=True)
    st.markdown("---")
    st.caption("Screening support only. Review original resumes and use consistent, job-related criteria for every candidate.")


st.markdown('<div class="eyebrow">Recruiting workspace</div>', unsafe_allow_html=True)
st.title("Candidate screening")
st.markdown('<p class="intro">Turn a stack of resumes into a clear, reviewable shortlist.</p>', unsafe_allow_html=True)

if analyze_clicked:
    if not job_description.strip():
        st.session_state.pop("screening_results", None)
        st.session_state["screening_errors"] = []
        st.error("Add a job description before analyzing resumes.")
    elif not uploaded_files:
        st.session_state.pop("screening_results", None)
        st.session_state["screening_errors"] = []
        st.error("Upload at least one PDF resume to continue.")
    else:
        results: list[dict[str, object]] = []
        errors: list[str] = []
        with st.spinner("Reading resumes and comparing job-related content..."):
            for uploaded_file in uploaded_files:
                try:
                    resume_text = extract_pdf_text(uploaded_file.getvalue())
                    if not resume_text:
                        errors.append(f"{uploaded_file.name}: no selectable text found")
                        continue
                    results.append(analyze_resume(job_description, resume_text, Path(uploaded_file.name).stem))
                except Exception as error:
                    errors.append(f"{uploaded_file.name}: {error}")
        st.session_state["screening_results"] = sorted(results, key=lambda item: int(item["score"]), reverse=True)
        st.session_state["screening_errors"] = errors

results = st.session_state.get("screening_results", [])
errors = st.session_state.get("screening_errors", [])

if results:
    filtered_results = [candidate for candidate in results if int(candidate["score"]) >= minimum_score]
    average_score = round(sum(int(candidate["score"]) for candidate in results) / len(results))
    high_matches = sum(int(candidate["score"]) >= 70 for candidate in results)
    job_skills = results[0]["job_skills"]

    metric_columns = st.columns(4)
    metrics = [
        ("Resumes analyzed", str(len(results)), "Readable PDF files"),
        ("Strong matches", str(high_matches), "Score of 70% or higher"),
        ("Average match", f"{average_score}%", "Across analyzed resumes"),
        ("Skills identified", str(len(job_skills)), "From the job description"),
    ]
    for column, (label, value, note) in zip(metric_columns, metrics):
        with column:
            st.markdown(
                f'<div class="metric"><div class="metric-label">{label}</div><div class="metric-value">{value}</div><div class="metric-note">{note}</div></div>',
                unsafe_allow_html=True,
            )

    st.markdown('<div class="section-heading"><h2>Ranked candidates</h2></div>', unsafe_allow_html=True)
    if job_skills:
        st.caption("Job skills detected: " + " · ".join(job_skills))
    else:
        st.info("No skills from the built-in skills list were detected in the job description. Ranking relies more heavily on text similarity.")
    below_threshold = [candidate for candidate in results if int(candidate["score"]) < minimum_score]
    if filtered_results:
        st.markdown('<div class="section-heading"><h2>Meeting the minimum score</h2></div>', unsafe_allow_html=True)
        for rank, candidate in enumerate(filtered_results, start=1):
            render_candidate(candidate, rank)
    if below_threshold:
        st.markdown('<div class="section-heading"><h2>Below minimum: improvement opportunities</h2></div>', unsafe_allow_html=True)
        st.caption("These candidates remain visible with the job skills their resumes did not show, so they can see what to strengthen.")
        for rank, candidate in enumerate(below_threshold, start=len(filtered_results) + 1):
            render_candidate(candidate, rank)

if errors:
    with st.expander(f"Files needing attention ({len(errors)})"):
        for error in errors:
            st.write(f"- {error}")

if not results:
    st.markdown(
        """
        <div class="metric" style="margin-top:12px;padding:22px">
          <div class="eyebrow">Ready when you are</div>
          <h2 style="margin:8px 0 4px">Add a role and its resumes</h2>
          <div style="color:#647574">Your ranked results and skill-gap notes will appear here after analysis.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
else:
    st.markdown(
        '<div class="notice" style="margin-top:18px">A match score is a prioritization signal, not a hiring decision. It can miss context, and text extraction may be incomplete. Review source documents and assess candidates consistently.</div>',
        unsafe_allow_html=True,
    )