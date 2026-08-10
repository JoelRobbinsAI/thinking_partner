# Environment
source .venv/bin/activate


# Initializing
python -m backend.cognitive_engine
python -m backend.scheduler --test
python app.py

# Git
git status
git add .
git commit -m ""
git push