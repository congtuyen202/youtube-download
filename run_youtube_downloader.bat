@echo off
title YouTube Video Downloader
color 0A

echo.
echo ========================================
echo    YOUTUBE VIDEO DOWNLOADER
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed!
    echo Please install Python from https://python.org
    echo.
    pause
    exit /b 1
)

REM Check if yt-dlp is installed
python -c "import yt_dlp" >nul 2>&1
if errorlevel 1 (
    echo Installing yt-dlp...
    pip install yt-dlp
    if errorlevel 1 (
        echo ERROR: Failed to install yt-dlp
        pause
        exit /b 1
    )
)

echo Starting YouTube Downloader...
echo.

REM Try GUI first, fallback to console
python youtube_downloader_gui.py 2>nul
if errorlevel 1 (
    echo GUI failed, starting console version...
    python youtube_downloader_console.py
)

echo.
echo Thank you for using YouTube Downloader!
pause 