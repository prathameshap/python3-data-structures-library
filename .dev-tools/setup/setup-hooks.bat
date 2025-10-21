@echo off
echo ================================================
echo   Git Hooks Setup (Windows)
echo ================================================
echo.

set "SCRIPT_DIR=%~dp0"

where powershell >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: PowerShell is not available
    pause
    exit /b 1
)

powershell -ExecutionPolicy Bypass -File "%SCRIPT_DIR%setup-hooks.ps1"

if %ERRORLEVEL% EQU 0 (
    echo.
    echo Press any key to exit...
) else (
    echo.
    echo Setup failed.
    echo Press any key to exit...
)

pause >nul