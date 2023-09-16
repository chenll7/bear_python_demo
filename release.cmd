@echo off

rmdir /s/q package

echo Donwloading dependencies...
call py -m pip download -d package .
echo=

echo Packaging...
call py -m pip wheel -w package .
echo=

echo Deleting ../../../tool-homemade/bear_python_demo/package ...
rmdir /s/q "../../../tool-homemade/bear_python_demo/package"
echo=

timeout /nobreak /t 3

echo Copying packages to ../../../tool-homemade/bear_python_demo/package ...
Xcopy "package" "../../../tool-homemade/bear_python_demo/package" /E /H /I
echo=