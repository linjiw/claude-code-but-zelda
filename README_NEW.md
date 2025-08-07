# 🎮 Zelda Claude Code

> Transform your coding experience into a Zelda adventure - with sounds, achievements, and stats!

[![Version](https://img.shields.io/badge/version-2.0-brightgreen)](.)
[![Integration](https://img.shields.io/badge/integration-Claude%20Code-blue)](.)
[![Sounds](https://img.shields.io/badge/sounds-25%2B-orange)](.)

## ✨ What is this?

Zelda Claude Code makes coding feel like playing Zelda! Every command plays a sound, successful streaks earn combos, and you unlock achievements as you code. Everything works seamlessly inside Claude Code - no external tools needed!

## 🚀 Installation (30 seconds!)

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/zelda-claude-code.git
cd zelda-claude-code

# Run the installer
./install.sh

# Restart Claude Code
exit
claude
```

That's it! Everything is now integrated into Claude Code.

## 🎮 How to Use

**Everything is done inside Claude Code using `@zelda` commands:**

```
@zelda stats          # View your coding statistics
@zelda achievements   # Check achievement progress  
@zelda combo         # See current combo streak
@zelda config        # View/change settings
@zelda help          # Show all commands
```

### Examples

Check your stats anytime:
```
@zelda stats
```

Adjust volume:
```
@zelda config volume 75
```

Disable combo sounds:
```
@zelda config sounds.combo false
```

## 🎵 What You'll Hear

| Event | Sound | When |
|-------|-------|------|
| ✅ Success | Cooking Success | Commands work |
| ❌ Error | Cooking Fail | Commands fail |
| 📝 Todo Complete | GetHeart | Marking todos done |
| 🔥 Combo 3x | Item Small | 3 successes in a row |
| 🔥 Combo 5x | Heart Get | 5 successes in a row |
| 🔥 Combo 10x | Achievement | 10 successes in a row! |
| 🏆 Achievement | Achievement | Unlocking achievements |
| 🔍 Search | Discovery | Finding search results |

## 🏆 Features

### 📊 **Statistics Tracking**
- Total commands executed
- Success rate percentage
- Longest streak record
- Favorite tools
- Session tracking

### ⚡ **Combo System**
Build streaks of successful commands:
- 🥉 Bronze (3 commands)
- 🥈 Silver (5 commands)  
- 🥇 Gold (10 commands)
- 💎 Platinum (20 commands)
- 🔥 Master (50 commands!)

### 🎖️ **Achievements**
Unlock 25+ achievements across categories:
- **Milestones**: First command, 10, 50, 100, 500+ commands
- **Combos**: Streak achievements
- **Perfectionist**: Error-free sessions
- **Explorer**: Using different tools

### ⚙️ **Customization**
Configure everything without leaving Claude Code:
- Sound volume
- Enable/disable features
- Notification preferences

## 📁 Simple Structure

```
zelda-claude-code/
├── install.sh           # One-click installer
├── zelda_core.py       # All logic in one file
├── hooks/
│   └── zelda_hook.py   # Claude Code integration
└── sounds/             # Your Zelda sounds
```

## 🤔 FAQ

**Q: Do I need to run Python scripts?**
A: No! Everything is done through `@zelda` commands in Claude Code.

**Q: How do I check my stats?**
A: Type `@zelda stats` in Claude Code.

**Q: Can I disable sounds?**
A: Yes! Type `@zelda config sounds.enabled false`

**Q: Where is data stored?**
A: In `~/.zelda/` (hidden folder in your home directory)

**Q: How do I update?**
A: Pull the latest changes and run `./install.sh` again

## 🎯 Philosophy

Our goal is **complete integration** with Claude Code. You should never need to:
- Leave Claude Code to check stats
- Run Python scripts manually
- Edit JSON files
- Use external tools

Everything happens naturally as you code!

## 🛠️ Troubleshooting

If sounds aren't playing:
1. Make sure you restarted Claude Code after installation
2. Check volume: `@zelda config volume 100`
3. Verify sounds are enabled: `@zelda config sounds.enabled true`

If commands don't work:
1. Make sure you're using the `@zelda` prefix
2. Restart Claude Code
3. Re-run `./install.sh`

## 🤝 Contributing

Contributions welcome! The codebase is now simplified:
- `zelda_core.py` - All logic
- `hooks/zelda_hook.py` - Claude Code integration
- `sounds/` - Sound files

## 📜 License

MIT - Use freely!

## 🙏 Credits

- Sound effects from The Legend of Zelda series
- Built for Claude Code by Anthropic
- Inspired by the desire to make coding more fun!

---

**Ready to transform your coding into an adventure?** Install now and may the Triforce guide your code! 🗡️✨