from __future__ import annotations

import re

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


SKILLS = (
    "python", "java", "javascript", "typescript", "c++", "c#", "sql", "nosql",
    "pandas", "numpy", "scikit-learn", "machine learning", "deep learning", "nlp",
    "tensorflow", "pytorch", "data analysis", "data engineering", "power bi", "tableau",
    "excel", "aws", "azure", "gcp", "docker", "kubernetes", "git", "linux",
    "fastapi", "django", "flask", "streamlit", "react", "node.js", "html", "css",
    "rest api", "communication", "leadership", "project management", "agile", "testing",
    "sales", "marketing", "customer service", "recruiting", "human resources",
)


def _normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text.lower()).strip()


def _find_skills(text: str) -> set[str]:
    normalized = _normalize(text)
    found = set()
    for skill in SKILLS:
        pattern = rf"(?<!\w){re.escape(skill)}(?!\w)"
        if re.search(pattern, normalized):
            found.add(skill)
    return found


def _experience_signals(text: str) -> int:
    matches = re.findall(r"\b(\d{1,2})\s*\+?\s*(?:years?|yrs?)\b", text.lower())
    return max((int(value) for value in matches), default=0)


def _similarity(job_description: str, resume_text: str) -> float:
    try:
        matrix = TfidfVectorizer(stop_words="english", ngram_range=(1, 2)).fit_transform(
            [job_description, resume_text]
        )
    except ValueError:
        return 0.0
    return float(cosine_similarity(matrix[0:1], matrix[1:2])[0][0])


def analyze_resume(job_description: str, resume_text: str, name: str) -> dict[str, object]:
    job_skills = _find_skills(job_description)
    resume_skills = _find_skills(resume_text)
    matched_skills = sorted(job_skills & resume_skills)
    missing_skills = sorted(job_skills - resume_skills)
    skill_overlap = len(matched_skills) / len(job_skills) if job_skills else 0.0
    similarity = _similarity(_normalize(job_description), _normalize(resume_text))

    if job_skills:
        score = 0.55 * skill_overlap + 0.45 * similarity
    else:
        score = similarity

    if matched_skills:
        summary = f"Found {len(matched_skills)} of {len(job_skills)} listed job skills, with {similarity:.0%} text similarity."
    elif job_skills:
        summary = f"No listed job skills were detected. Text similarity is {similarity:.0%}; verify extraction and relevant experience manually."
    else:
        summary = f"No predefined job skills were detected. Text similarity is {similarity:.0%}."

    if missing_skills and skill_overlap < 0.75:
        focus_skills = ", ".join(missing_skills[:4])
        if len(missing_skills) > 4:
            focus_skills += f", and {len(missing_skills) - 4} more"
        improvement_tip = (
            f"If you genuinely have experience with {focus_skills}, make it visible in a specific project or work bullet. "
            "If not, don't claim it; build relevant experience first."
        )
    elif similarity < 0.35:
        improvement_tip = (
            "Rewrite your summary and most relevant bullets to connect your real experience to this role's "
            "responsibilities and terminology. Include a concrete result where possible, and use terms only when accurate."
        )
    else:
        improvement_tip = (
            "Your detected overlap is already strong. Keep relevant skills easy to scan and support each with "
            "a concise project or work example and a measurable result."
        )

    return {
        "name": name,
        "score": round(score * 100),
        "similarity": similarity,
        "skill_overlap": skill_overlap,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "job_skills": sorted(job_skills),
        "experience": _experience_signals(resume_text),
        "summary": summary,
        "improvement_tip": improvement_tip,
    }