@echo off

call package

echo Deleting %USERPROFILE%/tool-homemade/bear_python_demo/package ...
rmdir /s/q "%USERPROFILE%/tool-homemade/bear_python_demo/package"
echo=

timeout /nobreak /t 3

echo Copying packages to %USERPROFILE%/tool-homemade/bear_python_demo/package ...
Xcopy "package" "%USERPROFILE%/tool-homemade/bear_python_demo/package" /E /H /I
echo=

start "" "%USERPROFILE%/bear-tent/tool-homemade/bear_python_demo"

timeout /nobreak /t 3