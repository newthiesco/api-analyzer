#!/bin/bash
# build.sh - Fixed for Rust compilation issues on Render.com

set -euo pipefail

echo "========================================="
echo "Starting build process - Rust-free version"
echo "========================================="

# Environment info
echo "Python version: $(python --version)"
echo "Current directory: $(pwd)"

# Upgrade pip first
echo "Upgrading pip..."
pip install --upgrade pip

# Install wheel first to ensure binary packages are used
echo "Installing wheel..."
pip install wheel

# Check requirements.txt
echo "Requirements file contents:"
cat requirements.txt

# Install dependencies using --no-build-isolation to avoid Rust issues
echo "Installing dependencies..."
pip install --no-build-isolation -r requirements.txt

# Verify installation
echo "Verifying package installation..."
python -c "
import fastapi, uvicorn, requests, pydantic
print('✅ All packages imported successfully')
print(f'Pydantic version: {pydantic.VERSION}')
"

echo "========================================="
echo "Build completed successfully!"
echo "========================================="