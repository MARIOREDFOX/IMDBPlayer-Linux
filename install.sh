#!/bin/bash

echo "Installing IMDB Movie Player..."

# Check for dependencies
echo "Checking dependencies..."
if ! command -v python3 &> /dev/null; then
    echo "Python3 not found. Please install Python3 first."
    exit 1
fi

# Install Python packages
pip3 install Pillow --user

# Copy desktop file
cp ~/IMDBPlayer-Linux/imdb-player.desktop ~/.local/share/applications/

# Update desktop database
update-desktop-database ~/.local/share/applications/ 2>/dev/null || true

echo "Installation complete!"
echo "You can now run IMDB Movie Player from your applications menu"
echo "Or run: ~/IMDBPlayer-Linux/run.sh"
