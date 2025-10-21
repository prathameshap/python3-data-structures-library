#!/bin/bash

echo "================================================"
echo "  Logic Apps Tools Setup (Mac/Linux)"
echo "================================================"
echo ""

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Check Node.js
if ! command -v node &> /dev/null; then
    echo -e "${RED}ERROR: Node.js not installed${NC}"
    echo "Install: https://nodejs.org/"
    exit 1
fi
echo -e "${GREEN}SUCCESS:${NC} Node.js: $(node --version)"

# Check .NET
if ! command -v dotnet &> /dev/null; then
    echo -e "${YELLOW}WARNING: .NET Core SDK not installed${NC}"
    echo "Install: https://dotnet.microsoft.com/download/dotnet/3.1"
else
    echo -e "${GREEN}SUCCESS:${NC} .NET Core: $(dotnet --version)"
fi

# Check/Install Azure Functions Core Tools
if ! command -v func &> /dev/null; then
    echo -e "${YELLOW}WARNING: Azure Functions Core Tools not found${NC}"
    echo "Installing..."
    
    if [[ "$OSTYPE" == "darwin"* ]]; then
        if command -v brew &> /dev/null; then
            brew tap azure/functions
            brew install azure-functions-core-tools@3
        fi
    else
        npm install -g azure-functions-core-tools@3 --unsafe-perm true
    fi
    
    if command -v func &> /dev/null; then
        echo -e "${GREEN}SUCCESS:${NC} Azure Functions Core Tools installed"
    fi
else
    echo -e "${GREEN}SUCCESS:${NC} Azure Functions Core Tools: $(func --version)"
fi

# Check/Install Azurite
if ! command -v azurite &> /dev/null; then
    echo ""
    read -p "Install Azurite (local storage emulator)? (Y/n): " -n 1 -r
    echo ""
    if [[ ! $REPLY =~ ^[Nn]$ ]]; then
        npm install -g azurite
        if command -v azurite &> /dev/null; then
            echo -e "${GREEN}SUCCESS:${NC} Azurite installed"
        fi
    fi
else
    echo -e "${GREEN}SUCCESS:${NC} Azurite found"
fi

echo ""
echo -e "${GREEN}================================================"
echo "   SUCCESS: Logic Apps Tools Setup Complete!"
echo "================================================${NC}"
echo ""
echo "Next steps:"
echo "  1. Open VS Code"
echo "  2. Install extensions: Azure Logic Apps (Standard)"
echo "  3. Create local.settings.json"
echo "  4. Run: func start"
echo ""