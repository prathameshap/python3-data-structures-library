#!/bin/bash

echo "================================================"
echo "  Git Hooks Setup (Mac/Linux)"
echo "================================================"
echo ""

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Get repository root
REPO_ROOT=$(git rev-parse --show-toplevel 2>/dev/null)

if [ -z "$REPO_ROOT" ]; then
    echo -e "${RED} ERROR: Not a git repository${NC}"
    exit 1
fi

DEV_TOOLS_DIR="$REPO_ROOT/.dev-tools"

if [ ! -d "$DEV_TOOLS_DIR" ]; then
    echo -e "${RED} ERROR: .dev-tools directory not found${NC}"
    exit 1
fi

# Check if already installed
if [ -f "$REPO_ROOT/.git/hooks/commit-msg" ] && grep -q "pre-commit" "$REPO_ROOT/.git/hooks/commit-msg" 2>/dev/null; then
    echo -e "${YELLOW} INFO: Hooks appear to be already installed.${NC}"
    echo ""
    read -p "Reinstall anyway? (y/N): " -n 1 -r
    echo ""
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Skipping installation."
        exit 0
    fi
fi

# Check Python
if ! command -v python3 &> /dev/null; then
    echo -e "${RED} ERROR: Python 3 is not installed${NC}"
    echo ""
    echo "Install Python 3:"
    echo "  Mac: brew install python3"
    echo "  Linux: sudo apt-get install python3"
    exit 1
fi

echo -e "${GREEN}✓${NC} Python 3 found: $(python3 --version)"

# Install pre-commit
if command -v pre-commit &> /dev/null; then
    echo -e "${GREEN}✓${NC} pre-commit already installed"
else
    echo ""
    echo "📦 Installing pre-commit framework..."
    if pip3 install --user pre-commit > /dev/null 2>&1; then
        echo -e "${GREEN}✓${NC} pre-commit installed"
    else
        if command -v brew &> /dev/null; then
            brew install pre-commit
        else
            python3 -m pip install --user pre-commit
        fi
    fi
fi

# Copy config
echo ""
echo "🔧 Configuring hooks..."
cp "$DEV_TOOLS_DIR/config/pre-commit-config.yaml" "$REPO_ROOT/.pre-commit-config.yaml"
echo -e "${GREEN}✓${NC} Configuration copied"

# Make scripts executable
chmod +x "$DEV_TOOLS_DIR/hooks/"*.py
echo -e "${GREEN}✓${NC} Scripts made executable"

# Install hooks
cd "$REPO_ROOT"
echo ""
echo "🔗 Installing Git hooks..."
pre-commit install > /dev/null 2>&1
pre-commit install --hook-type commit-msg > /dev/null 2>&1
pre-commit install --hook-type pre-push > /dev/null 2>&1
echo -e "${GREEN}✓${NC} Hooks installed"

echo ""
echo -e "${GREEN}================================================"
echo "   SUCCESS: Setup Complete!"
echo "================================================${NC}"
echo ""
echo "Hooks installed:"
echo "  • commit-msg : Validates commit message format"
echo "  • pre-commit : Validates Logic App workflows"
echo "  • pre-push   : Validates branch naming"
echo ""
echo " INFO: Hooks only run on dev/feature branches, NOT on release"
echo ""
echo "Test your setup:"
echo "  git commit --allow-empty -m 'TEST-123 | test commit'"
echo ""