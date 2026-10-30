---
title: ResumeIQ
sdk: docker
app_port: 7860
---

# ResumeIQ

ResumeIQ is a lightweight Streamlit prototype for comparing PDF resumes with a job description. It extracts selectable PDF text, ranks resumes using an explainable heuristic, and shows matched skills, skills to strengthen, and candidate improvement suggestions.

## Run locally

```powershell
cd Ai_Resume_tracker
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
streamlit run app.py
```

## Deploy without GitHub

This project is configured for a Docker-based Hugging Face Space.

1. Sign in to Hugging Face and create a new Space with the Docker SDK.
2. Set the Space visibility to Public only if you intend anyone with the URL to access it.
3. Use the Space's browser-based file upload to add `Dockerfile`, `README.md`, `app.py`, `resume_engine.py`, and `requirements.txt` from this folder. No GitHub account or repository is needed.
4. Wait for the Space to build, then open its public URL.

Public hosting sends uploaded resumes to the hosting provider's servers. This prototype has no authentication or access control; use synthetic/demo resumes only unless you first add appropriate access controls, retention limits, and privacy protections.

## How scoring works

When predefined job skills are detected, the score combines skill overlap (55%) and TF-IDF cosine similarity (45%). If no predefined skills are detected, the score uses text similarity alone. The skills list and weights are in `resume_engine.py` and should be adapted and validated for the role and organization. The app uses `pypdf` for PDF text extraction.

This is a prototype, not a validated hiring assessment. Scores can reflect resume wording, incomplete PDF extraction, and limitations in the built-in skill vocabulary. Do not use the score as the sole basis for screening or hiring. Review source resumes, apply consistent job-related criteria, and follow applicable privacy and employment laws. The app does not intentionally score demographic or protected characteristics, but that does not establish that its outcomes are bias-free.