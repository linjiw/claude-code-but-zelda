#!/usr/bin/env python3
"""
Fix Claude Code hooks configuration to match actual tool usage
"""

import json
from pathlib import Path

def update_claude_settings():
    """Update Claude settings with all possible tool hooks"""
    
    settings_path = Path.home() / '.config' / 'claude' / 'settings.json'
    hooks_dir = Path(__file__).parent / 'hooks'
    
    # Define comprehensive hook mappings for ALL tools
    comprehensive_hooks = {
        "hooks": {
            # User interactions
            "user-prompt-submit-hook": str(hooks_dir / "on_success.sh"),
            "assistant-message-done-hook": str(hooks_dir / "on_success.sh"),
            
            # Tool-specific hooks - covering ALL tools Claude Code uses
            "tool-result-hook": {
                # Shell/System tools
                "Bash": {
                    "success": str(hooks_dir / "on_success.sh"),
                    "error": str(hooks_dir / "on_error.sh")
                },
                "Shell": {
                    "success": str(hooks_dir / "on_success.sh"),
                    "error": str(hooks_dir / "on_error.sh")
                },
                
                # File operations
                "List": {  # ls command uses this!
                    "success": str(hooks_dir / "on_success.sh"),
                    "error": str(hooks_dir / "on_error.sh")
                },
                "LS": {  # Alternative name
                    "success": str(hooks_dir / "on_success.sh"),
                    "error": str(hooks_dir / "on_error.sh")
                },
                "Read": {  # cat command uses this!
                    "success": str(hooks_dir / "on_success.sh"),
                    "error": str(hooks_dir / "on_error.sh")
                },
                "Write": {
                    "success": str(hooks_dir / "on_success.sh"),
                    "error": str(hooks_dir / "on_error.sh")
                },
                "Edit": {
                    "success": str(hooks_dir / "on_success.sh"),
                    "error": str(hooks_dir / "on_error.sh")
                },
                "MultiEdit": {
                    "success": str(hooks_dir / "on_success.sh"),
                    "error": str(hooks_dir / "on_error.sh")
                },
                
                # Search tools
                "Grep": {
                    "success": str(hooks_dir / "on_success.sh"),
                    "error": str(hooks_dir / "on_error.sh")
                },
                "Glob": {
                    "success": str(hooks_dir / "on_success.sh"),
                    "error": str(hooks_dir / "on_error.sh")
                },
                "Find": {
                    "success": str(hooks_dir / "on_success.sh"),
                    "error": str(hooks_dir / "on_error.sh")
                },
                
                # Task management
                "TodoWrite": {
                    "success": str(hooks_dir / "on_todo_complete.sh"),
                    "error": str(hooks_dir / "on_error.sh")
                },
                "Task": {
                    "success": str(hooks_dir / "on_success.sh"),
                    "error": str(hooks_dir / "on_error.sh")
                },
                
                # Web tools
                "WebSearch": {
                    "success": str(hooks_dir / "on_success.sh"),
                    "error": str(hooks_dir / "on_error.sh")
                },
                "WebFetch": {
                    "success": str(hooks_dir / "on_success.sh"),
                    "error": str(hooks_dir / "on_error.sh")
                },
                
                # Development tools
                "Test": {
                    "success": str(hooks_dir / "on_test_pass.sh"),
                    "error": str(hooks_dir / "on_test_fail.sh")
                },
                "Run": {
                    "success": str(hooks_dir / "on_success.sh"),
                    "error": str(hooks_dir / "on_error.sh")
                },
                "Execute": {
                    "success": str(hooks_dir / "on_success.sh"),
                    "error": str(hooks_dir / "on_error.sh")
                }
            }
        }
    }
    
    # Backup existing settings
    if settings_path.exists():
        backup_path = settings_path.with_suffix('.json.backup_comprehensive')
        with open(settings_path) as f:
            current = json.load(f)
        with open(backup_path, 'w') as f:
            json.dump(current, f, indent=2)
        print(f"Backed up to: {backup_path}")
    
    # Write comprehensive settings
    with open(settings_path, 'w') as f:
        json.dump(comprehensive_hooks, f, indent=2)
    
    print(f"✅ Updated Claude settings with comprehensive hooks")
    print(f"📍 Settings file: {settings_path}")
    
    # Show what tools are now covered
    tools = list(comprehensive_hooks['hooks']['tool-result-hook'].keys())
    print(f"\n📦 Tools configured ({len(tools)} total):")
    for tool in sorted(tools):
        print(f"  • {tool}")
    
    return True

if __name__ == "__main__":
    update_claude_settings()
    print("\n🎮 Now restart Claude Code or start a new session to apply changes!")
    print("\nTest with:")
    print("  claude")
    print("  > ls        # Should play success sound")
    print("  > cat /fake # Should play error sound")