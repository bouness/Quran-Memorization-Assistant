#!/usr/bin/env bash
set -e

echo "🧹 Cleaning previous builds..."
rm -rf dist build installer_output

# Create installer output directory
mkdir -p installer_output

echo "📦 Installing Python dependencies..."
python3 -m pip install --upgrade pip
pip3 install -r requirements.txt

echo "🔧 Installing Nuitka..."
pip3 install nuitka

echo "🏗️ Building application with Nuitka..."

python3 -m nuitka \
    --standalone \
    --assume-yes-for-downloads \
    --enable-plugin=pyside6 \
    --include-qt-plugins=multimedia,platforms,imageformats \
    --include-data-dir=assets=assets \
    --include-data-file=version.py=version.py \
    --output-dir=dist \
    app.py

echo "✅ Nuitka build complete!"

# Verify build output
if [ -d "dist/app.dist" ]; then
    echo "✅ Build created successfully!"
    echo "📦 Build location: dist/app.dist"
    du -sh dist/app.dist
else
    echo "❌ ERROR: Build output not found"
    ls -la dist || true
    exit 1
fi

echo "🎉 Linux build process completed successfully!"