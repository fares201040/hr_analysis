@echo off
setlocal enabledelayedexpansion

REM install_zsh.bat - Script to install zsh on Windows
REM This script supports multiple installation methods

echo 🚀 Starting zsh installation on Windows...

REM Function to check if a command exists
:command_exists
where %1 >nul 2>&1
if %errorlevel% equ 0 (
    exit /b 0
) else (
    exit /b 1
)

REM Function to install via Chocolatey
:install_via_chocolatey
echo 📦 Installing zsh via Chocolatey...
call :command_exists choco
if %errorlevel% equ 0 (
    choco install zsh -y
    echo ✅ zsh installed successfully via Chocolatey
    exit /b 0
) else (
    echo ❌ Chocolatey not found
    exit /b 1
)

REM Function to install via winget
:install_via_winget
echo 📦 Installing zsh via winget...
call :command_exists winget
if %errorlevel% equ 0 (
    winget install --id=GnuWin32.Zsh -e
    echo ✅ zsh installed successfully via winget
    exit /b 0
) else (
    echo ❌ winget not found
    exit /b 1
)

REM Function to install via MSYS2
:install_via_msys2
echo 📦 Installing zsh via MSYS2...
call :command_exists pacman
if %errorlevel% equ 0 (
    pacman -S zsh --noconfirm
    echo ✅ zsh installed successfully via MSYS2
    exit /b 0
) else (
    echo ❌ MSYS2 (pacman) not found
    exit /b 1
)

REM Function to download and install manually
:install_manually
echo 📥 Downloading zsh manually...

REM Create temporary directory
set TEMP_DIR=%TEMP%\zsh_install_%RANDOM%
mkdir "%TEMP_DIR%"
cd /d "%TEMP_DIR%"

REM Download zsh for Windows
echo Downloading zsh for Windows...
powershell -Command "Invoke-WebRequest -Uri 'https://github.com/msys2/msys2-installer/releases/download/2024-01-13/msys2-x86_64-20240113.exe' -OutFile 'msys2-installer.exe'"

echo ⚠️  Manual installation requires more steps:
echo 1. Run the downloaded msys2 installer
echo 2. Open MSYS2 terminal
echo 3. Run: pacman -S zsh
echo 4. Add zsh to your PATH

REM Cleanup
cd /d "%~dp0"
rmdir /s /q "%TEMP_DIR%"
exit /b 1

REM Main installation logic
echo 🔍 Checking available package managers...

REM Try different installation methods in order of preference
call :install_via_chocolatey
if %errorlevel% equ 0 (
    echo 🎉 zsh installation completed successfully!
    goto :verify
)

call :install_via_winget
if %errorlevel% equ 0 (
    echo 🎉 zsh installation completed successfully!
    goto :verify
)

call :install_via_msys2
if %errorlevel% equ 0 (
    echo 🎉 zsh installation completed successfully!
    goto :verify
)

echo ⚠️  No automatic installation method found
call :install_manually

:verify
REM Verify installation
echo 🔍 Verifying zsh installation...
call :command_exists zsh
if %errorlevel% equ 0 (
    echo ✅ zsh is now installed and available!
    where zsh
    zsh --version
    echo.
    echo 💡 To use zsh as your default shell:
    echo    1. Add zsh to your PATH if not already done
    echo    2. Run: zsh
    echo    3. Or set it as default in your terminal settings
) else (
    echo ❌ zsh installation verification failed
    echo 💡 You may need to restart your terminal or add zsh to your PATH
)

echo.
echo 📚 For more information, visit: https://ohmyz.sh/
pause 