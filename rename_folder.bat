@echo off
echo Renaming project folder from Neuro-Care-main to TumorTrace...
cd ..
rename "Neuro-Care-main" "TumorTrace"
if %errorlevel% equ 0 (
    echo Successfully renamed to TumorTrace!
    cd TumorTrace
    echo Starting Flask app...
    python app.py
) else (
    echo Failed to rename folder. Please close all programs using this folder and try again.
    pause
)
