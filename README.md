# AI Math Differentiator — starter project

An educational website that changes one Grade 9 mathematics task for three learner needs.

## What it does

- **Foundation:** Easier example with guiding questions.
- **Standard:** Grade-level independent problem.
- **Advanced:** Multi-step or applied challenge.
- At each level, Gemini dynamically generates an adapted problem, a hint, a worked solution, and feedback on student answers.

## Stack

- Python / Streamlit — app and secure server-side UI
- Google Gemini API (`gemini-3.5-flash-lite`) — dynamic differentiation and guidance

## Run locally (optional)

```bash
pip install -r requirements.txt
```

Create `.streamlit/secrets.toml` (do NOT upload it to GitHub):

```toml
GEMINI_API_KEY = "YOUR_PERSONAL_KEY"
```

Then run:

```bash
streamlit run app.py
```

## Deploy

1. Make a **public** GitHub repository containing `app.py`, `requirements.txt`, and `README.md`.
2. Open https://share.streamlit.io and create an app from the repo's `main` branch; app entry point: `app.py`.
3. In **Advanced settings → Secrets**, add the TOML line `GEMINI_API_KEY = "..."` using your personal key.
4. Deploy, test all three levels, and share the `.streamlit.app` URL.

## Prompt strategy

For every level, the model is told to preserve the central concept while modifying task complexity. Follow-up prompts request a partial hint, a checked solution, or formative feedback, avoiding automatic disclosure of solutions in the initial task.

## Important

This repository is a **starter template**. Adapt the core task, prompts, presentation, and documentation in your own words, test the mathematics, and comply with your course's originality policy. Do not put API keys in source code or commits.
