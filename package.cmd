@echo off

rmdir /s/q package
rmdir /s/q build

echo Donwloading dependencies...
call py -m pip download -d package .
echo=

echo Packaging...
call py -m pip wheel -w package .
echo=