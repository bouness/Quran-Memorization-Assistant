@echo off
setlocal enabledelayedexpansion

REM Build script for QMA on Windows

echo 🧹 Cleaning previous builds...
rmdir /s /q dist 2>nul
rmdir /s /q build 2>nul
rmdir /s /q installer_output 2>nul

REM Create installer output directory
mkdir installer_output 2>nul

REM Install application dependencies
echo 📦 Installing Python dependencies...
python -m pip install --upgrade pip
pip install -r requirements.txt
if !errorlevel! neq 0 (
    echo ❌ ERROR: Failed to install Python dependencies
    exit /b !errorlevel!
)

REM Install build tool (Nuitka)
echo 🔧 Installing Nuitka...
pip install nuitka
if !errorlevel! neq 0 (
    echo ❌ ERROR: Failed to install Nuitka
    exit /b !errorlevel!
)

REM Build with Nuitka
echo 🏗️ Building application with Nuitka...
python -m nuitka ^
    --standalone ^
    --assume-yes-for-downloads ^
    --windows-console-mode=disable ^
    --enable-plugin=pyside6 ^
    --include-qt-plugins=multimedia,platforms,imageformats ^
    --include-data-dir=assets=assets ^
    --include-data-file=version.py=version.py ^
    --windows-icon-from-ico=assets/icon.ico ^
    --output-dir=dist ^
    app.py
if !errorlevel! neq 0 (
    echo ❌ ERROR: Nuitka build failed with error code !errorlevel!
    exit /b !errorlevel!
)

echo ✅ Nuitka build complete!

REM === Install Inno Setup if not present ===
echo 🔍 Checking for Inno Setup...
set "ISCC_PATH="
if exist "C:\Program Files (x86)\Inno Setup 6\ISCC.exe" (
    set "ISCC_PATH=C:\Program Files (x86)\Inno Setup 6\ISCC.exe"
    echo ✅ Found Inno Setup at: !ISCC_PATH!
) else if exist "C:\Program Files\Inno Setup 6\ISCC.exe" (
    set "ISCC_PATH=C:\Program Files\Inno Setup 6\ISCC.exe"
    echo ✅ Found Inno Setup at: !ISCC_PATH!
) else (
    echo 📦 Inno Setup not found, installing via Chocolatey...
    choco install innosetup -y --no-progress
    if exist "C:\Program Files (x86)\Inno Setup 6\ISCC.exe" (
        set "ISCC_PATH=C:\Program Files (x86)\Inno Setup 6\ISCC.exe"
        echo ✅ Inno Setup installed at: !ISCC_PATH!
    ) else (
        echo ❌ ERROR: Failed to install Inno Setup
        exit /b 1
    )
)

REM === Build installer with Inno Setup ===
echo 🚀 Building installer with Inno Setup...
echo Using Inno Setup at: !ISCC_PATH!
echo Running: "!ISCC_PATH!" app.iss

"!ISCC_PATH!" app.iss
if !errorlevel! neq 0 (
    echo ❌ ERROR: Inno Setup failed with error code !errorlevel!
    echo 📁 Inno Setup output directory contents:
    dir installer_output 2>nul || echo installer_output directory doesn't exist
    exit /b !errorlevel!
)

REM === Verify installer was created ===
if exist installer_output\QMAInstaller.exe (
    echo ✅ Installer created successfully!
    echo 📦 Installer location: installer_output\QMAInstaller.exe
    dir installer_output\QMAInstaller.exe
    echo File size: 
    for /f "tokens=3" %%a in ('dir installer_output\QMAInstaller.exe ^| find "QMAInstaller.exe"') do echo %%a
) else (
    echo ❌ ERROR: Installer file was not created
    echo 📁 Contents of installer_output directory:
    dir installer_output 2>nul || echo installer_output directory doesn't exist
    echo 📁 Current directory contents:
    dir
    exit /b 1
)

echo 🎉 Build process completed successfully!
