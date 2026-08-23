@echo off
if not exist build mkdir build

blender.exe --command extension build --source-dir ./src/ba_toolkit --output-dir ./build

if %errorlevel% neq 0 (
    echo Build failed!
    exit /b 1
)

echo Build done