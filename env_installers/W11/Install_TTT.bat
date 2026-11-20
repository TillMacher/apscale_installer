@echo off
setlocal EnableExtensions
title Install the TTT environment

REM ==========================================================================
REM  Settings
REM ==========================================================================
set "ENV_NAME=TTT"
set "ENV_URL=https://raw.githubusercontent.com/TillMacher/TaxonTableTools2/main/environments/taxontabletools2_env.yml"
set "POST_CMD="
set "CHECK_MODULE=taxontabletools2"
set "START_CMD=taxontabletools2"
set "DISK_SPACE=1.5 GB"
set "TOOLS=TaxonTableTools2"

echo ============================================================
echo   Installing the %ENV_NAME% conda environment
echo ============================================================
echo.

REM ==========================================================================
REM  1. Find Miniconda / Anaconda
REM ==========================================================================
set "ROOT="
if defined CONDA_EXE if exist "%CONDA_EXE%" for %%I in ("%CONDA_EXE%\..\..") do set "ROOT=%%~fI"
for %%D in ("%USERPROFILE%\miniconda3" "%USERPROFILE%\anaconda3" "%USERPROFILE%\miniforge3" "%LOCALAPPDATA%\miniconda3" "%LOCALAPPDATA%\anaconda3" "%LOCALAPPDATA%\miniforge3" "%ProgramData%\miniconda3" "%ProgramData%\anaconda3" "%ProgramData%\miniforge3" "C:\miniconda3" "C:\anaconda3") do (
    if not defined ROOT if exist "%%~D\Scripts\activate.bat" set "ROOT=%%~D"
)
if not defined ROOT (
    echo [x] Miniconda was not found.
    echo     Please install Miniconda first:
    echo     https://repo.anaconda.com/miniconda/Miniconda3-latest-Windows-x86_64.exe
    goto :fail
)
echo [+] Found conda in: %ROOT%

REM ==========================================================================
REM  Disclaimer
REM ==========================================================================
echo.
echo ------------------------------------------------------------
echo   Before you continue
echo ------------------------------------------------------------
echo   This will install: %TOOLS%
echo.
echo   Disk space needed:  about %DISK_SPACE%
echo   Install location:   %ROOT%\envs\%ENV_NAME%
echo   Internet:           required during the installation
echo   Duration:           about 5-15 minutes
echo.
echo   The software is provided "as is", without warranty of any kind.
echo ------------------------------------------------------------
echo.
choice /C YN /N /M "Do you want to continue? [y/n]: "
if errorlevel 2 (
    echo.
    echo Installation cancelled. Nothing was changed.
    echo.
    pause
    exit /b 0
)
echo.
call "%ROOT%\Scripts\activate.bat" "%ROOT%"

REM ==========================================================================
REM  2. Download the latest environment file
REM ==========================================================================
set "YML=%TEMP%\%ENV_NAME%_env.yml"
echo [+] Downloading the environment file...
curl -fsSL "%ENV_URL%" -o "%YML%"
if errorlevel 1 (
    echo [x] Download failed. Please check your internet connection.
    goto :fail
)

REM ==========================================================================
REM  3. Create or update the environment
REM ==========================================================================
call conda env list | findstr /B /C:"%ENV_NAME% " >nul
if errorlevel 1 (
    echo [+] Creating the environment. This can take 5-15 minutes...
    echo.
    call conda env create -n %ENV_NAME% -f "%YML%"
) else (
    echo [+] The environment already exists. Updating it. This can take a few minutes...
    echo.
    call conda env update -n %ENV_NAME% -f "%YML%" --prune
)
if errorlevel 1 (
    echo [x] Installing the environment failed. See the messages above.
    echo     Tip: close this window and simply run the installer again.
    goto :fail
)

REM ==========================================================================
REM  4. Extra setup step (optional)
REM ==========================================================================
if not "%POST_CMD%"=="" (
    echo.
    echo [+] Running: %POST_CMD%
    call conda run --no-capture-output -n %ENV_NAME% %POST_CMD%
    if errorlevel 1 echo [!] "%POST_CMD%" reported a problem. See the messages above.
)

REM ==========================================================================
REM  5. Check the installation
REM ==========================================================================
call conda run -n %ENV_NAME% python -c "import %CHECK_MODULE%" >nul 2>&1
if errorlevel 1 (
    echo [x] The environment was created, but %CHECK_MODULE% could not be loaded.
    goto :fail
)

del "%YML%" >nul 2>&1
echo.
echo ============================================================
echo   Done! The %ENV_NAME% environment is ready.
echo.
echo   To start, open "Anaconda Powershell Prompt (miniconda3)"
echo   and type:
echo.
echo       conda activate %ENV_NAME%
echo       %START_CMD%
echo ============================================================
echo.
pause
exit /b 0

:fail
echo.
echo Installation did not complete.
echo.
pause
exit /b 1
