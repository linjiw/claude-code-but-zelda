#!/bin/bash

echo "🔐 GitHub Secret Setup Helper"
echo "============================"
echo ""
echo "📋 You have existing NPM tokens available:"
npm token list
echo ""
echo "To use one of these tokens (or create a new one):"
echo ""
echo "1. If you need to see the full token, create a new one:"
echo "   npm token create --read-only=false"
echo ""
echo "2. Opening GitHub Secrets page in your browser..."
echo "   https://github.com/linjiw/claude-code-but-zelda/settings/secrets/actions"
echo ""

# Try to open the URL in the default browser
if command -v open &> /dev/null; then
    # macOS
    open "https://github.com/linjiw/claude-code-but-zelda/settings/secrets/actions"
elif command -v xdg-open &> /dev/null; then
    # Linux
    xdg-open "https://github.com/linjiw/claude-code-but-zelda/settings/secrets/actions"
elif command -v start &> /dev/null; then
    # Windows
    start "https://github.com/linjiw/claude-code-but-zelda/settings/secrets/actions"
else
    echo "Please manually open the URL above in your browser"
fi

echo ""
echo "3. Click 'New repository secret'"
echo "4. Name: NPM_TOKEN"
echo "5. Value: Your npm token (starts with npm_)"
echo "6. Click 'Add secret'"
echo ""
echo "✅ Once added, the GitHub Actions workflows will be able to publish to NPM!"