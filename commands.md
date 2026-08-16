# Environment
source .venv/bin/activate


# Initializing
python -m backend.cognitive_engine
python -m backend.scheduler --test
python app.py
streamlit run streamlit_app.py

# Git
git status
git add .
git commit -m ""
git push