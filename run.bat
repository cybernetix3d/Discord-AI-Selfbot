@echo off
CLS
title Installing AI Selfbot...
set PATH=%PATH%;%~dp0
if not exist bot-env (
    echo 'bot-env' folder not found. Installing...
    python -m venv bot-env
    call .\bot-env\Scripts\activate.bat
    pip install -r requirements.txt

    cls

    echo Installed.
)

call .\bot-env\Scripts\activate.bat
echo Starting bot...
title AI Selfbot
python "main.py"
cmd /k
