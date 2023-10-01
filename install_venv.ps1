py -m venv venv

echo Copying pip.ini
Copy-Item -Path "$env:USERPROFILE/.pip/pip.ini" -Destination "venv/pip.ini"