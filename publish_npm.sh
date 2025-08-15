#!/bin/bash

# Zelda Claude Code - NPM Publishing Script
# This script helps publish the package to npm

set -e

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${GREEN}🎮 Zelda Claude Code - NPM Publishing Script${NC}"
echo "============================================"

# Check if logged in to npm
echo -e "\n${YELLOW}Checking npm login status...${NC}"
if npm whoami >/dev/null 2>&1; then
    USER=$(npm whoami)
    echo -e "${GREEN}✅ Logged in as: $USER${NC}"
else
    echo -e "${RED}❌ Not logged in to npm${NC}"
    echo "Please run: npm login"
    exit 1
fi

# Get current version
CURRENT_VERSION=$(node -p "require('./package.json').version")
echo -e "\n${YELLOW}Current version: $CURRENT_VERSION${NC}"

# Check if version tag already exists
if git tag | grep -q "^v$CURRENT_VERSION$"; then
    echo -e "${YELLOW}⚠️  Version v$CURRENT_VERSION already tagged${NC}"
    echo "Consider bumping version with: npm version patch/minor/major"
    read -p "Continue anyway? (y/N) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Run tests
echo -e "\n${YELLOW}Running tests...${NC}"
python3 test_npm_ready.py || {
    echo -e "${YELLOW}⚠️  Some tests failed${NC}"
    read -p "Continue anyway? (y/N) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
}

# Build and check package
echo -e "\n${YELLOW}Building package...${NC}"
npm pack --dry-run

echo -e "\n${YELLOW}Package contents look good?${NC}"
read -p "Proceed with publishing? (y/N) " -n 1 -r
echo

if [[ $REPLY =~ ^[Yy]$ ]]; then
    # Publish to npm
    echo -e "\n${YELLOW}Publishing to npm...${NC}"
    npm publish
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✅ Successfully published version $CURRENT_VERSION to npm!${NC}"
        
        # Create git tag
        echo -e "\n${YELLOW}Creating git tag...${NC}"
        git tag -a "v$CURRENT_VERSION" -m "Release version $CURRENT_VERSION"
        git push origin "v$CURRENT_VERSION"
        echo -e "${GREEN}✅ Tagged version v$CURRENT_VERSION${NC}"
        
        echo -e "\n${GREEN}🎉 Publishing complete!${NC}"
        echo "View package at: https://www.npmjs.com/package/zelda-claude-code"
        echo "Install with: npm install -g zelda-claude-code@$CURRENT_VERSION"
    else
        echo -e "${RED}❌ Publishing failed${NC}"
        exit 1
    fi
else
    echo "Publishing cancelled"
    exit 0
fi