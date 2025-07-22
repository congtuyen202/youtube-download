@echo off
title YouTube Downloader Setup
color 0B

echo.
echo ========================================
echo    YOUTUBE DOWNLOADER SETUP
echo ========================================
echo.

REM Create downloads folder
if not exist "downloads" (
    mkdir downloads
    echo Created downloads folder
)

REM Check Python
echo Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed!
    echo Please install Python from https://python.org
    echo Make sure to check "Add Python to PATH" during installation
    echo.
    pause
    exit /b 1
)

echo Python found ✓

REM Install yt-dlp
echo Installing yt-dlp...
pip install yt-dlp
if errorlevel 1 (
    echo ERROR: Failed to install yt-dlp
    echo Please check your internet connection
    pause
    exit /b 1
)

echo yt-dlp installed ✓

REM Test tkinter
echo Testing GUI support...
python -c "import tkinter" >nul 2>&1
if errorlevel 1 (
    echo WARNING: GUI not available, will use console version
    echo You can install tkinter later if needed
) else (
    echo GUI support available ✓
)

echo.
echo ========================================
echo    SETUP COMPLETE!
echo ========================================
echo.
echo Files in this folder:
echo - run_youtube_downloader.bat (Main launcher)
echo - youtube_downloader_console.py (Console version)
echo - youtube_downloader_gui.py (GUI version)
echo - dl.py (Core download logic)
echo - downloads/ (Video storage folder)
echo.
echo To start the downloader:
echo 1. Double-click "run_youtube_downloader.bat"
echo 2. Or run: python youtube_downloader_console.py
echo.
echo Press any key to test the downloader...
pause

REM Test the downloader
echo.
echo Testing downloader...
python youtube_downloader_console.py

echo.
echo Setup complete! You can now use the YouTube Downloader.
pause 