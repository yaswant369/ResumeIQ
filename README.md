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

## Deploy on Streamlit Community Cloud

Streamlit Community Cloud deploys directly from GitHub; Docker is not required.

1. Sign in at [share.streamlit.io](https://share.streamlit.io) with the GitHub account that can access this repository.
2. Select **Create app**, then choose `yaswant369/ResumeIQ`, branch `main`, and main file path `app.py`.
3. Select **Deploy** and wait for the build to finish.
4. Open the generated `*.streamlit.app` URL to use the app.

The app is public once deployed. Uploaded resumes are processed by the hosting provider, and this prototype has no authentication or access control. Use synthetic/demo resumes only unless you first add appropriate access controls, retention limits, and privacy protections.

## How scoring works

When predefined job skills are detected, the score combines skill overlap (55%) and TF-IDF cosine similarity (45%). If no predefined skills are detected, the score uses text similarity alone. The skills list and weights are in `resume_engine.py` and should be adapted and validated for the role and organization. The app uses `pypdf` for PDF text extraction.

This is a prototype, not a validated hiring assessment. Scores can reflect resume wording, incomplete PDF extraction, and limitations in the built-in skill vocabulary. Do not use the score as the sole basis for screening or hiring. Review source resumes, apply consistent job-related criteria, and follow applicable privacy and employment laws. The app does not intentionally score demographic or protected characteristics, but that does not establish that its outcomes are bias-free.
