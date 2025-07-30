#!/bin/bash

# install_zsh.sh - Script to install zsh on Windows
# This script supports multiple installation methods

set -e  # Exit on any error

echo "🚀 Starting zsh installation on Windows..."

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to install via Chocolatey
install_via_chocolatey() {
    echo "📦 Installing zsh via Chocolatey..."
    if command_exists choco; then
        choco install zsh -y
        echo "✅ zsh installed successfully via Chocolatey"
        return 0
    else
        echo "❌ Chocolatey not found"
        return 1
    fi
}

# Function to install via winget
install_via_winget() {
    echo "📦 Installing zsh via winget..."
    if command_exists winget; then
        winget install --id=GnuWin32.Zsh -e
        echo "✅ zsh installed successfully via winget"
        return 0
    else
        echo "❌ winget not found"
        return 1
    fi
}

# Function to install via MSYS2
install_via_msys2() {
    echo "📦 Installing zsh via MSYS2..."
    if command_exists pacman; then
        pacman -S zsh --noconfirm
        echo "✅ zsh installed successfully via MSYS2"
        return 0
    else
        echo "❌ MSYS2 (pacman) not found"
        return 1
    fi
}

# Function to install via Cygwin
install_via_cygwin() {
    echo "📦 Installing zsh via Cygwin..."
    if command_exists cygcheck; then
        # Try to install via setup.exe if available
        if [ -f "/cygdrive/c/cygwin64/setup-x86_64.exe" ]; then
            /cygdrive/c/cygwin64/setup-x86_64.exe -q -P zsh
            echo "✅ zsh installed successfully via Cygwin"
            return 0
        else
            echo "❌ Cygwin setup.exe not found"
            return 1
        fi
    else
        echo "❌ Cygwin not found"
        return 1
    fi
}

# Function to download and install manually
install_manually() {
    echo "📥 Downloading zsh manually..."
    
    # Create temporary directory
    TEMP_DIR=$(mktemp -d)
    cd "$TEMP_DIR"
    
    # Download zsh for Windows
    echo "Downloading zsh for Windows..."
    curl -L -o zsh.zip "https://github.com/msys2/msys2-installer/releases/download/2024-01-13/msys2-x86_64-20240113.exe"
    
    echo "⚠️  Manual installation requires more steps:"
    echo "1. Run the downloaded msys2 installer"
    echo "2. Open MSYS2 terminal"
    echo "3. Run: pacman -S zsh"
    echo "4. Add zsh to your PATH"
    
    # Cleanup
    cd - > /dev/null
    rm -rf "$TEMP_DIR"
    
    return 1
}

# Main installation logic
echo "🔍 Checking available package managers..."

# Try different installation methods in order of preference
if install_via_chocolatey; then
    echo "🎉 zsh installation completed successfully!"
elif install_via_winget; then
    echo "🎉 zsh installation completed successfully!"
elif install_via_msys2; then
    echo "🎉 zsh installation completed successfully!"
elif install_via_cygwin; then
    echo "🎉 zsh installation completed successfully!"
else
    echo "⚠️  No automatic installation method found"
    install_manually
fi

# Verify installation
echo "🔍 Verifying zsh installation..."
if command_exists zsh; then
    echo "✅ zsh is now installed and available!"
    echo "📍 zsh location: $(which zsh)"
    echo "📋 zsh version: $(zsh --version)"
    echo ""
    echo "💡 To use zsh as your default shell:"
    echo "   1. Add zsh to your PATH if not already done"
    echo "   2. Run: zsh"
    echo "   3. Or set it as default in your terminal settings"
else
    echo "❌ zsh installation verification failed"
    echo "💡 You may need to restart your terminal or add zsh to your PATH"
fi

echo ""
echo "📚 For more information, visit: https://ohmyz.sh/" 