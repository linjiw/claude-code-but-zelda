#!/bin/bash

echo "🎮 Zelda Sounds Interactive Test"
echo "================================"
echo ""
echo "Let's test each sound in context!"
echo ""

# Color codes
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to play sound and wait
play_and_describe() {
    local sound_type=$1
    local description=$2
    local zelda_name=$3
    
    echo -e "${BLUE}Playing:${NC} $description"
    echo -e "${YELLOW}Zelda sound:${NC} $zelda_name"
    python3 scripts/play_sound_async.py "$sound_type"
    sleep 2
    echo ""
}

echo "Press Enter to start the test..."
read

echo -e "${GREEN}=== SUCCESS SOUNDS ===${NC}"
echo ""

play_and_describe "success" \
    "✅ Command executed successfully" \
    "Cooking Success"

play_and_describe "todo_complete" \
    "💝 Todo item marked complete" \
    "GetHeart"

play_and_describe "test_pass" \
    "🏆 All tests passing" \
    "GetMedium (Puzzle Solved)"

echo -e "${RED}=== ERROR SOUNDS ===${NC}"
echo ""

play_and_describe "error" \
    "❌ Command failed" \
    "Cooking Fail"

play_and_describe "warning" \
    "⚠️ Warning or alert" \
    "Assassin Appear"

play_and_describe "test_fail" \
    "💀 Test failure" \
    "Game Over"

echo -e "${BLUE}=== PROGRESS SOUNDS ===${NC}"
echo ""

play_and_describe "progress" \
    "💎 Quick progress update" \
    "GetSmall (Rupee)"

play_and_describe "start" \
    "▶️ Starting new action" \
    "ZonauBlockMaster Bridge"

play_and_describe "complete" \
    "🎯 Major achievement" \
    "GetLarge"

echo -e "${GREEN}=== RAPID FIRE TEST ===${NC}"
echo "Multiple sounds at once (like busy coding session):"
echo ""

for i in {1..5}; do
    echo -e "${YELLOW}Action $i...${NC}"
    python3 scripts/play_sound_async.py progress &
    sleep 0.2
done

sleep 2

echo ""
echo -e "${GREEN}✨ Test Complete!${NC}"
echo ""
echo "What you should have noticed:"
echo "1. Each sound matches its context (success=positive, error=negative)"
echo "2. Sounds play instantly without delay"
echo "3. Multiple sounds can overlap (rapid fire test)"
echo "4. Each has distinct Zelda game feel"
echo ""
echo "Now try in Claude Code:"
echo "  - Run: ls (hear success)"
echo "  - Run: cat /fake (hear error)"
echo "  - Ask Claude to create a todo list"
echo ""
echo "🎮 Happy coding with Zelda sounds!"