@echo off

cd /D "%~dp0"

call py ./helper/script/create_updater.py for-data

pause