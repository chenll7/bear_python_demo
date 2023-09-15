@echo off

rmdir /s/q package

call py -m pip download -d package .

call py -m pip wheel -w package .

echo Delete ../../../tool-homemade/bear_demo/package
rmdir /s/q "../../../tool-homemade/bear_demo/package"

Xcopy "package" "../../../tool-homemade/bear_demo/package" /E /H /I

rem py -m pip install --no-index --find-links=./package bear_demo