@echo off
cd /d "%~dp0"
py -3 -m venv .venv
.venv\Scripts\python -m pip install -r requirements.txt
start "" http://localhost:7860
.venv\Scripts\python app.py
pause
