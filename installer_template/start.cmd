@echo off

if not exist "venv/Scripts/python.exe" (
    echo venv/Scripts/python.exe not found! Please run install.cmd first.
    pause
    exit
)

call "venv/Scripts/python" -m bear_python_demo.entry main