#!/bin/bash
# TT-Search Setup Script

set -e

echo "🎬 TT-Search Setup"
echo "=================="
echo ""

# Check Node.js
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js 18.0 or higher."
    exit 1
fi

NODE_VERSION=$(node -v | cut -d'v' -f2 | cut -d'.' -f1)
if [ "$NODE_VERSION" -lt 18 ]; then
    echo "❌ Node.js version must be 18.0 or higher. Current: $(node -v)"
    exit 1
fi

echo "✓ Node.js $(node -v) found"

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.10 or higher."
    exit 1
fi

PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
echo "✓ Python $PYTHON_VERSION found"

# Install Node.js dependencies
echo ""
echo "📦 Installing Node.js dependencies..."
npm install

# Install Python dependencies
echo ""
echo "🐍 Installing Python dependencies..."
pip install -r requirements.txt

# Install Playwright browsers
echo ""
echo "🎭 Installing Playwright browsers..."
python3 -m playwright install chromium

# Create data directories
echo ""
echo "📁 Creating data directories..."
mkdir -p data/{videos,users,hashtags,analytics,temp}

# Build TypeScript
echo ""
echo "🔨 Building TypeScript..."
npm run build

echo ""
echo "✅ Setup complete!"
echo ""
echo "Quick start:"
echo "  tt-search --help"
echo "  tt-search search 'ai technology' --limit 50"
echo "  tt-search interactive"
echo ""
echo "For more information, see README.md"
