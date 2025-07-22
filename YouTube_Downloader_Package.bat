@echo off
title YouTube Downloader Package Creator
color 0E

echo.
echo ========================================
echo    CREATING YOUTUBE DOWNLOADER PACKAGE
echo ========================================
echo.

REM Create package folder
set PACKAGE_NAME=YouTube_Downloader_v1.0
if exist "%PACKAGE_NAME%" (
    rmdir /s /q "%PACKAGE_NAME%"
)

mkdir "%PACKAGE_NAME%"
cd "%PACKAGE_NAME%"

echo Creating package structure...

REM Copy all necessary files
copy "..\youtube_downloader_console.py" "youtube_downloader_console.py"
copy "..\youtube_downloader_gui.py" "youtube_downloader_gui.py"
copy "..\dl.py" "dl.py"
copy "..\requirements.txt" "requirements.txt"
copy "..\README.md" "README.md"
copy "..\install_tcl_tk.bat" "install_tcl_tk.bat"

REM Create launcher
echo @echo off > "START_DOWNLOADER.bat"
echo title YouTube Video Downloader >> "START_DOWNLOADER.bat"
echo color 0A >> "START_DOWNLOADER.bat"
echo. >> "START_DOWNLOADER.bat"
echo echo ======================================== >> "START_DOWNLOADER.bat"
echo echo    YOUTUBE VIDEO DOWNLOADER >> "START_DOWNLOADER.bat"
echo echo ======================================== >> "START_DOWNLOADER.bat"
echo echo. >> "START_DOWNLOADER.bat"
echo. >> "START_DOWNLOADER.bat"
echo REM Check if Python is installed >> "START_DOWNLOADER.bat"
echo python --version ^>nul 2^>^&1 >> "START_DOWNLOADER.bat"
echo if errorlevel 1 ^( >> "START_DOWNLOADER.bat"
echo     echo ERROR: Python is not installed! >> "START_DOWNLOADER.bat"
echo     echo Please install Python from https://python.org >> "START_DOWNLOADER.bat"
echo     echo. >> "START_DOWNLOADER.bat"
echo     pause >> "START_DOWNLOADER.bat"
echo     exit /b 1 >> "START_DOWNLOADER.bat"
echo ^) >> "START_DOWNLOADER.bat"
echo. >> "START_DOWNLOADER.bat"
echo REM Check if yt-dlp is installed >> "START_DOWNLOADER.bat"
echo python -c "import yt_dlp" ^>nul 2^>^&1 >> "START_DOWNLOADER.bat"
echo if errorlevel 1 ^( >> "START_DOWNLOADER.bat"
echo     echo Installing yt-dlp... >> "START_DOWNLOADER.bat"
echo     pip install yt-dlp >> "START_DOWNLOADER.bat"
echo     if errorlevel 1 ^( >> "START_DOWNLOADER.bat"
echo         echo ERROR: Failed to install yt-dlp >> "START_DOWNLOADER.bat"
echo         pause >> "START_DOWNLOADER.bat"
echo         exit /b 1 >> "START_DOWNLOADER.bat"
echo     ^) >> "START_DOWNLOADER.bat"
echo ^) >> "START_DOWNLOADER.bat"
echo. >> "START_DOWNLOADER.bat"
echo echo Starting YouTube Downloader... >> "START_DOWNLOADER.bat"
echo echo. >> "START_DOWNLOADER.bat"
echo. >> "START_DOWNLOADER.bat"
echo REM Try GUI first, fallback to console >> "START_DOWNLOADER.bat"
echo python youtube_downloader_gui.py 2^>nul >> "START_DOWNLOADER.bat"
echo if errorlevel 1 ^( >> "START_DOWNLOADER.bat"
echo     echo GUI failed, starting console version... >> "START_DOWNLOADER.bat"
echo     python youtube_downloader_console.py >> "START_DOWNLOADER.bat"
echo ^) >> "START_DOWNLOADER.bat"
echo. >> "START_DOWNLOADER.bat"
echo echo. >> "START_DOWNLOADER.bat"
echo echo Thank you for using YouTube Downloader! >> "START_DOWNLOADER.bat"
echo pause >> "START_DOWNLOADER.bat"

REM Create setup script
echo @echo off > "SETUP.bat"
echo title YouTube Downloader Setup >> "SETUP.bat"
echo color 0B >> "SETUP.bat"
echo. >> "SETUP.bat"
echo echo ======================================== >> "SETUP.bat"
echo echo    YOUTUBE DOWNLOADER SETUP >> "SETUP.bat"
echo echo ======================================== >> "SETUP.bat"
echo echo. >> "SETUP.bat"
echo. >> "SETUP.bat"
echo REM Create downloads folder >> "SETUP.bat"
echo if not exist "downloads" ^( >> "SETUP.bat"
echo     mkdir downloads >> "SETUP.bat"
echo     echo Created downloads folder >> "SETUP.bat"
echo ^) >> "SETUP.bat"
echo. >> "SETUP.bat"
echo REM Check Python >> "SETUP.bat"
echo echo Checking Python installation... >> "SETUP.bat"
echo python --version ^>nul 2^>^&1 >> "SETUP.bat"
echo if errorlevel 1 ^( >> "SETUP.bat"
echo     echo ERROR: Python is not installed! >> "SETUP.bat"
echo     echo Please install Python from https://python.org >> "SETUP.bat"
echo     echo Make sure to check "Add Python to PATH" during installation >> "SETUP.bat"
echo     echo. >> "SETUP.bat"
echo     pause >> "SETUP.bat"
echo     exit /b 1 >> "SETUP.bat"
echo ^) >> "SETUP.bat"
echo. >> "SETUP.bat"
echo echo Python found ✓ >> "SETUP.bat"
echo. >> "SETUP.bat"
echo REM Install yt-dlp >> "SETUP.bat"
echo echo Installing yt-dlp... >> "SETUP.bat"
echo pip install yt-dlp >> "SETUP.bat"
echo if errorlevel 1 ^( >> "SETUP.bat"
echo     echo ERROR: Failed to install yt-dlp >> "SETUP.bat"
echo     echo Please check your internet connection >> "SETUP.bat"
echo     pause >> "SETUP.bat"
echo     exit /b 1 >> "SETUP.bat"
echo ^) >> "SETUP.bat"
echo. >> "SETUP.bat"
echo echo yt-dlp installed ✓ >> "SETUP.bat"
echo. >> "SETUP.bat"
echo echo Setup complete! You can now use the YouTube Downloader. >> "SETUP.bat"
echo pause >> "SETUP.bat"

REM Create downloads folder
mkdir downloads

REM Create README for package
echo # YouTube Video Downloader Package > "PACKAGE_README.txt"
echo. >> "PACKAGE_README.txt"
echo ## Quick Start >> "PACKAGE_README.txt"
echo. >> "PACKAGE_README.txt"
echo 1. **First time setup:** Double-click `SETUP.bat` >> "PACKAGE_README.txt"
echo 2. **Start downloader:** Double-click `START_DOWNLOADER.bat` >> "PACKAGE_README.txt"
echo. >> "PACKAGE_README.txt"
echo ## Files included: >> "PACKAGE_README.txt"
echo - `START_DOWNLOADER.bat` - Main launcher (double-click to start) >> "PACKAGE_README.txt"
echo - `SETUP.bat` - First-time setup (install dependencies) >> "PACKAGE_README.txt"
echo - `youtube_downloader_console.py` - Console version >> "PACKAGE_README.txt"
echo - `youtube_downloader_gui.py` - GUI version >> "PACKAGE_README.txt"
echo - `dl.py` - Core download logic >> "PACKAGE_README.txt"
echo - `downloads/` - Folder where videos are saved >> "PACKAGE_README.txt"
echo - `README.md` - Detailed instructions >> "PACKAGE_README.txt"
echo. >> "PACKAGE_README.txt"
echo ## Requirements: >> "PACKAGE_README.txt"
echo - Python 3.7+ (will be installed automatically if needed) >> "PACKAGE_README.txt"
echo - Internet connection for downloading videos >> "PACKAGE_README.txt"
echo. >> "PACKAGE_README.txt"
echo ## Features: >> "PACKAGE_README.txt"
echo - Download single videos with quality options >> "PACKAGE_README.txt"
echo - Download entire playlists >> "PACKAGE_README.txt"
echo - Download multiple videos at once >> "PACKAGE_README.txt"
echo - Download videos from channels >> "PACKAGE_README.txt"
echo - Preview channel videos before downloading >> "PACKAGE_README.txt"
echo - Check available video qualities >> "PACKAGE_README.txt"
echo. >> "PACKAGE_README.txt"
echo ## Support: >> "PACKAGE_README.txt"
echo If you encounter issues: >> "PACKAGE_README.txt"
echo 1. Make sure Python is installed >> "PACKAGE_README.txt"
echo 2. Run SETUP.bat again >> "PACKAGE_README.txt"
echo 3. Check your internet connection >> "PACKAGE_README.txt"
echo 4. Try the console version if GUI fails >> "PACKAGE_README.txt"

cd ..

echo.
echo ========================================
echo    PACKAGE CREATED SUCCESSFULLY!
echo ========================================
echo.
echo Package folder: %PACKAGE_NAME%
echo.
echo To distribute:
echo 1. Zip the "%PACKAGE_NAME%" folder
echo 2. Share the zip file
echo.
echo Users can then:
echo 1. Extract the zip
echo 2. Double-click "SETUP.bat" (first time)
echo 3. Double-click "START_DOWNLOADER.bat" (to use)
echo.
pause 