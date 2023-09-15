@echo off

rmdir /s/q package

echo Donwload dependencies.
call py -m pip download -d package .

echo Packaging...
call py -m pip wheel -w package .

echo Delete ../../../tool-homemade/bear_demo/package .
rmdir /s/q "../../../tool-homemade/bear_demo/package"

echo Copy packages to ../../../tool-homemade/bear_demo/package .
Xcopy "package" "../../../tool-homemade/bear_demo/package" /E /H /I