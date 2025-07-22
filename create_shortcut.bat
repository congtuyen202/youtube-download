@echo off
title Create YouTube Downloader Shortcut
color 0D

echo.
echo ========================================
echo    CREATING DESKTOP SHORTCUT
echo ========================================
echo.

REM Get current directory
set CURRENT_DIR=%~dp0
set SHORTCUT_NAME=YouTube Downloader

REM Create VBS script to create shortcut
echo Set oWS = WScript.CreateObject("WScript.Shell") > "%TEMP%\CreateShortcut.vbs"
echo sLinkFile = "%USERPROFILE%\Desktop\%SHORTCUT_NAME%.lnk" >> "%TEMP%\CreateShortcut.vbs"
echo Set oLink = oWS.CreateShortcut(sLinkFile) >> "%TEMP%\CreateShortcut.vbs"
echo oLink.TargetPath = "%CURRENT_DIR%run_youtube_downloader.bat" >> "%TEMP%\CreateShortcut.vbs"
echo oLink.WorkingDirectory = "%CURRENT_DIR%" >> "%TEMP%\CreateShortcut.vbs"
echo oLink.Description = "YouTube Video Downloader" >> "%TEMP%\CreateShortcut.vbs"
echo oLink.IconLocation = "%CURRENT_DIR%run_youtube_downloader.bat,0" >> "%TEMP%\CreateShortcut.vbs"
echo oLink.Save >> "%TEMP%\CreateShortcut.vbs"

REM Run the VBS script
cscript //nologo "%TEMP%\CreateShortcut.vbs"

REM Clean up
del "%TEMP%\CreateShortcut.vbs"

echo.
echo ========================================
echo    SHORTCUT CREATED SUCCESSFULLY!
echo ========================================
echo.
echo Shortcut location: %USERPROFILE%\Desktop\%SHORTCUT_NAME%.lnk
echo.
echo You can now:
echo 1. Double-click the desktop shortcut to start
echo 2. Or use the shortcut in the Start Menu
echo.
pause 