py "-3.11" -m venv venv

Write-Output Copying pip.ini
Copy-Item -Path "$env:USERPROFILE/.pip/pip.ini" -Destination "venv/pip.ini"