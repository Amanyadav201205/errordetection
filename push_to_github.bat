@echo off
title Push Simulator to GitHub
echo ======================================================================
echo Push Interactive Simulator to GitHub
echo ======================================================================
echo.
echo Step 1: Create a new repository on GitHub:
echo         https://github.com/new
echo.
echo Step 2: Copy your repository URL
echo         (Example: https://github.com/your-username/network-simulator.git)
echo.
set /p REPO_URL="Enter your GitHub Repository URL: "

if "%REPO_URL%"=="" (
    echo No URL entered. Aborting.
    pause
    exit /b
)

echo.
echo Configuring remote and pushing to GitHub...
git branch -M main
git remote remove origin >nul 2>&1
git remote add origin %REPO_URL%
git push -u origin main

echo.
if errorlevel 1 (
    echo Push failed. Please check your GitHub URL and credentials.
) else (
    echo ======================================================================
    echo SUCCESS! Your code is now on GitHub!
    echo.
    echo TO LAUNCH AS A PUBLIC WEBSITE (GitHub Pages):
    echo 1. Go to your GitHub repository in your browser
    echo 2. Click "Settings" (top menu)
    echo 3. Click "Pages" on the left menu
    echo 4. Under "Branch", select "main" and click "Save"
    echo 5. In 1-2 minutes, GitHub will give you a public link like:
    echo    https://your-username.github.io/your-repository/
    echo ======================================================================
)
pause
