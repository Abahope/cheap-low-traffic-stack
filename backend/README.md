# Backend

# Install

Install poetry (I do a global install: https://python-poetry.org/docs/)
Install python 3.11 (I use pyenv: https://github.com/pyenv/pyenv)

cd into /backend then:
poetry install

This should create a .venv that includes uvicorn

# Run

Activate your poetry/python virtual environment:
source .venv/bin/activate

cd into /backend/src then:
uvicorn cheap.main:app --reload
