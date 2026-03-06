#!/bin/bash
set -e

# === Clean previous builds ===
rm -rf dist build package
rm -f QMA-linux.tar.gz
mkdir -p dist

# === Install application dependencies ===
python3 -m pip install --upgrade pip
pip install -r requirements.txt

# === Install build tool (Nuitka) ===
pip install nuitka

# === Build with Nuitka ===
python3 -m nuitka \
    --standalone \
    --assume-yes-for-downloads \
    --enable-plugin=pyside6 \
    --include-qt-plugins=multimedia,platforms,imageformats \
    --include-data-dir=assets=assets \
    --include-data-file=version.py=version.py \
    --output-dir=dist \
    app.py

# === Make executable permissions ===
chmod +x dist/app.dist/app.bin

# === Prepare package directory ===
echo "Preparing package..."
mkdir -p package/QMA
cp -r dist/app.dist/* package/QMA/
cp -r assets package/QMA/ || true
cp version.py package/QMA/ || true
cp -r installer package/QMA/

# === Create tarball ===
echo "Creating distribution tarball..."
tar -czf QMA-linux.tar.gz -C package QMA

echo
echo "✅ Linux build complete!"
echo "Created: QMA-linux.tar.gz"
echo "To install:"
echo "  1. tar -xzf QMA-linux.tar.gz"
echo "  2. sudo ./QMA/installer/install.sh"
