# Contributing to Zelda Claude Code

Thank you for your interest in contributing to Zelda Claude Code! This guide will help you get started.

## 🎮 Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/YOUR_USERNAME/claude-code-but-zelda.git`
3. Create a feature branch: `git checkout -b feature/your-feature-name`
4. Make your changes
5. Test thoroughly (see Testing section)
6. Commit your changes: `git commit -m "feat: add amazing feature"`
7. Push to your fork: `git push origin feature/your-feature-name`
8. Open a Pull Request

## 🧪 Testing

Before submitting a PR, ensure all tests pass:

```bash
# Run all tests
python test_suite.py
python test_cross_platform_hook.py
python test_integration.py
python test_zelda_system.py

# Test on your specific platform
CI=true python test_cross_platform_hook.py

# Test sound playback
./demo_sounds.sh
```

### Platform-Specific Testing

#### Windows
- Ensure PowerShell execution works
- Test with both Windows PowerShell and PowerShell Core (if available)
- Verify `winsound` module compatibility

#### macOS
- Test with `afplay` command
- Verify no permission issues with audio playback

#### Linux
- Test with available audio players (`aplay`, `paplay`, `ffplay`)
- Ensure PulseAudio/ALSA compatibility

## 📝 Commit Guidelines

We follow conventional commits specification:

- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation changes
- `style:` Code style changes (formatting, etc.)
- `refactor:` Code refactoring
- `test:` Test additions or changes
- `chore:` Maintenance tasks

Examples:
```
feat: add combo system for consecutive successful commands
fix: resolve Windows FileNotFoundError during sound playback
docs: update installation instructions for Linux users
```

## 🔊 Adding New Sounds

1. Place WAV files in the `sounds/` directory
2. Use 16-bit, 44.1kHz format for best compatibility
3. Keep file sizes reasonable (< 2MB per sound)
4. Update sound mappings in `hooks/zelda_hook.py`
5. Test across all platforms

## 🐛 Reporting Issues

When reporting issues, please include:

1. **Environment details:**
   - OS and version
   - Python version
   - Node.js version
   - Claude Code version

2. **Steps to reproduce**

3. **Error messages/logs**

4. **Expected vs actual behavior**

## 🏗️ Architecture Guidelines

### Hook System
- Hooks must be non-blocking
- Always fail silently (don't interrupt Claude Code)
- Support stdin JSON input
- Exit with code 0 on success

### Sound Playback
- Must work cross-platform (Windows, macOS, Linux)
- Async/non-blocking playback
- Multiple fallback methods for reliability
- No external dependencies beyond standard OS tools

### File Structure
```
zelda_claude/
├── hooks/           # Claude Code hook scripts
├── scripts/         # Utility scripts
├── sounds/          # Audio files (WAV format)
├── tests/           # Test files
└── .github/         # GitHub Actions workflows
```

## 🚀 Release Process

Releases are automated via GitHub Actions:

1. **Manual Release:**
   - Go to Actions → "Publish to NPM"
   - Choose version bump type (patch/minor/major)
   - Run workflow

2. **GitHub Release:**
   - Create a new release on GitHub
   - Tag with semantic version (e.g., v3.0.2)
   - Workflow automatically publishes to NPM

## 📦 NPM Publishing

Only maintainers can publish to NPM. The process:

1. Tests must pass on all platforms
2. Version bump via workflow or manual
3. Automatic publish on release/tag
4. Post-publish verification runs automatically

## 🤝 Code of Conduct

- Be respectful and inclusive
- Welcome newcomers and help them get started
- Focus on constructive feedback
- Celebrate the fun, creative nature of this project!

## 💡 Feature Ideas

We welcome creative additions that enhance the Zelda theme:

- New achievement types
- Boss battle modes for complex tasks
- Dungeon themes for different coding sessions
- Item collection mechanics
- Easter eggs and secrets

## 📬 Contact

- Issues: [GitHub Issues](https://github.com/linjiw/claude-code-but-zelda/issues)
- Discussions: [GitHub Discussions](https://github.com/linjiw/claude-code-but-zelda/discussions)

## 🙏 Thank You!

Every contribution, no matter how small, helps make Claude Code more epic! Whether it's fixing a typo, adding a feature, or reporting a bug, we appreciate your help in making coding more adventurous! 🗡️✨