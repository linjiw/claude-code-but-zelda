# 🎮 Zelda Sounds for Claude Code

> Add legendary Zelda sound effects to your Claude Code workflow!

[![Tests](https://img.shields.io/badge/tests-passing-brightgreen)](VALIDATION_REPORT.md)
[![Performance](https://img.shields.io/badge/latency-21ms-blue)](VALIDATION_REPORT.md)
[![Platform](https://img.shields.io/badge/platform-macOS%20%7C%20Linux-lightgrey)]()

## 🎵 What You'll Hear

| Event | Sound | From |
|-------|-------|------|
| ✅ Command Success | Cooking Success | Zelda TOTK |
| ❌ Command Error | Cooking Fail | Zelda TOTK |
| 📝 Todo Complete | GetHeart | Zelda TOTK |
| 🧪 Test Pass | Puzzle Solved | Zelda TOTK |
| 💀 Test Fail | Game Over | Zelda TOTK |
| ⚠️ Need Input | Assassin Appear | Zelda TOTK |
| 🎯 Task Complete | GetLarge | Zelda TOTK |

## 🚀 Quick Install (One Command!)

```bash
# Clone and install
git clone https://github.com/YOUR_USERNAME/zelda-claude-sounds.git
cd zelda-claude-sounds
./install_zelda_sounds.sh
```

That's it! The installer handles everything automatically.

## 📖 Manual Installation

<details>
<summary>Click for step-by-step manual installation</summary>

### Prerequisites
- Claude Code installed
- Python 3.6+
- macOS (afplay) or Linux (aplay)

### Step 1: Clone Repository
```bash
git clone https://github.com/YOUR_USERNAME/zelda-claude-sounds.git
cd zelda-claude-sounds
```

### Step 2: Configure Hooks
```bash
python3 configure_claude_hooks.py
```

### Step 3: Restart Claude Code
```bash
# Exit if running
exit

# Start fresh
claude
```

### Step 4: Verify
```bash
# In Claude Code
> /hooks  # Should show PostToolUse, Notification, Stop hooks
> ls      # Should play success sound
```

</details>

## 🎯 Testing Your Installation

### Quick Test
```bash
# Test all sounds
./test-sounds

# Or in Claude Code:
> ls          # Success sound
> cat /fake   # Error sound
```

### Full Validation
```bash
# Run comprehensive tests
python3 test_claude_integration.py

# Expected output:
# Tests Run: 15
# Tests Passed: 15
# Success Rate: 100.0%
```

## 🛠️ Configuration

### Hook Events

The system responds to these Claude Code events:

| Event | When It Triggers | Sound |
|-------|-----------------|-------|
| **PostToolUse** | After any tool executes | Success/Error based on result |
| **Notification** | Claude needs your input | Warning sound |
| **Stop** | Claude finishes responding | Completion sound |

### Customizing Sounds

Replace any `.wav` file in the `sounds/` directory:

```bash
sounds/
├── success.wav      # Command success
├── error.wav        # Command failure
├── todo_complete.wav # Todo marked done
├── warning.wav      # Alerts
└── ...
```

## 🔧 Troubleshooting

<details>
<summary>No sounds playing?</summary>

1. **Check hooks are loaded:**
   ```bash
   # In Claude Code
   > /hooks
   ```

2. **Restart Claude Code completely:**
   ```bash
   exit
   claude
   ```

3. **Test sound system:**
   ```bash
   afplay sounds/success.wav  # macOS
   aplay sounds/success.wav   # Linux
   ```

4. **Check debug log:**
   ```bash
   cat /tmp/claude_hook_debug.log
   ```

</details>

<details>
<summary>Hooks not showing in /hooks?</summary>

1. **Verify settings location:**
   ```bash
   cat ~/.claude/settings.json | grep hooks
   ```

2. **Re-run configuration:**
   ```bash
   python3 configure_claude_hooks.py
   ```

3. **Restart Claude Code**

</details>

<details>
<summary>Performance issues?</summary>

- Sounds play asynchronously (21ms average)
- No impact on Claude Code performance
- If experiencing delays, check system audio settings

</details>

## 📊 Performance

Validated performance metrics:
- **Average latency:** 21ms
- **Maximum latency:** 48ms
- **Concurrent sounds:** Handled perfectly
- **CPU impact:** <1%
- **Blocking:** Never (fully async)

See [VALIDATION_REPORT.md](VALIDATION_REPORT.md) for detailed metrics.

## 🗑️ Uninstall

```bash
# Remove hooks but keep sounds
./uninstall

# Or completely remove
rm -rf zelda-claude-sounds
```

## 📚 Documentation

- [**CLAUDE_HOOKS_GUIDE.md**](CLAUDE_HOOKS_GUIDE.md) - How hooks work
- [**VALIDATION_REPORT.md**](VALIDATION_REPORT.md) - Test results & metrics
- [**TROUBLESHOOTING.md**](TROUBLESHOOTING.md) - Common issues
- [**TESTING_GUIDE.md**](TESTING_GUIDE.md) - How to test

## 🤝 Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Run tests: `python3 test_claude_integration.py`
4. Submit a pull request

## 📝 License

MIT License - Use freely!

## 🙏 Credits

- Sound effects from The Legend of Zelda: Tears of the Kingdom
- Built for Claude Code by Anthropic
- Community contributions welcome

## ⚡ Quick Commands

```bash
./install_zelda_sounds.sh  # One-click install
./test-sounds              # Test all sounds
./demo_sounds.sh           # Demo sequence
./uninstall                # Remove hooks
python3 test_claude_integration.py  # Run tests
```

## 🎮 Enjoy Your Legendary Coding Experience!

Every command now has the magic of Hyrule! 🗡️✨

---

**Questions?** Open an issue on GitHub
**Working great?** Star the repo! ⭐