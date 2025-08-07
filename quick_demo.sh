#!/bin/bash

# Zelda Claude Code - Quick Demo Script for GIF Recording
# Record this with any screen recorder, then convert to GIF!

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
BOLD='\033[1m'
NC='\033[0m' # No Color

# Clear screen
clear

# Title
echo -e "${BOLD}${CYAN}"
echo "============================================"
echo "      🎮 ZELDA CLAUDE CODE DEMO 🎮"
echo "============================================"
echo -e "${NC}"
sleep 2

# Show the main feature
echo -e "${GREEN}✨ Turn coding into a Zelda adventure!${NC}\n"
sleep 1

echo -e "${YELLOW}Every command plays sounds:${NC}"
echo "  ✅ Success → Puzzle solved!"
echo "  ❌ Error → Take damage!"
echo "  🔥 Combo → Secret found!"
echo "  🏆 Achievement → Item get!"
sleep 3

clear

# Demo commands in Claude Code
echo -e "${BOLD}${BLUE}📊 Check Your Stats:${NC}"
echo -e "${CYAN}$ @zelda stats${NC}"
sleep 1
echo -e "
${BOLD}📊 Zelda Coding Statistics${NC}

Session Stats:
- Commands: 42
- Success Rate: 92.8% 
- Current Streak: 7 🔥

All-Time Stats:
- Total Commands: 1,337
- Longest Streak: 28 🔥
- Achievements: 8/11
"
sleep 3

clear

# Show achievements
echo -e "${BOLD}${BLUE}🏆 View Achievements:${NC}"
echo -e "${CYAN}$ @zelda achievements${NC}"
sleep 1
echo -e "
${BOLD}🏆 Achievements${NC}

Progress: 8/11 (72%)
[████████████████░░░░]

✅ First Steps
✅ Apprentice Coder
✅ Combo Novice
✅ Perfectionist
🔒 Master Coder (87/100)
🔒 Combo Legend (15/20)
"
sleep 3

clear

# Show combo
echo -e "${BOLD}${BLUE}🔥 Check Current Combo:${NC}"
echo -e "${CYAN}$ @zelda combo${NC}"
sleep 1
echo -e "
${BOLD}⚡ Combo Status${NC}

Current Streak: 7 🔥
Highest Today: 15
All-Time Best: 28

${YELLOW}You're on fire! Keep it up!${NC}
"
sleep 3

clear

# Play sounds demo
echo -e "${BOLD}${PURPLE}🔊 Hear The Sounds:${NC}\n"
sleep 1

echo -e "${GREEN}✓ Test passed!${NC}"
python3 scripts/play_sound.py success 2>/dev/null &
sleep 1.5

echo -e "${GREEN}✓ Build successful!${NC}"
python3 scripts/play_sound.py puzzle_solved 2>/dev/null &
sleep 1.5

echo -e "${RED}✗ Error detected!${NC}"
python3 scripts/play_sound.py error 2>/dev/null &
sleep 1.5

echo -e "${YELLOW}🏆 Achievement unlocked!${NC}"
python3 scripts/play_sound.py achievement 2>/dev/null &
sleep 2

clear

# Installation
echo -e "${BOLD}${GREEN}🚀 Quick Installation:${NC}\n"
echo "$ git clone github.com/linjiw/claude-code-but-zelda"
echo "$ cd claude-code-but-zelda"
echo "$ ./install.sh"
echo ""
echo -e "${GREEN}✅ Done! (30 seconds)${NC}"
sleep 3

echo -e "\n${BOLD}${YELLOW}May the Triforce guide your code! 🗡️✨${NC}\n"
sleep 2

# End screen
clear
echo -e "${BOLD}${CYAN}"
echo "============================================"
echo "   🎮 github.com/linjiw/claude-code-but-zelda"
echo "============================================"
echo -e "${NC}"