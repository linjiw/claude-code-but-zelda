#!/usr/bin/env python3
"""
Demo script for Zelda Claude Code
Run this and record your screen to create a demo GIF!
"""

import time
import subprocess
import sys
import json
from pathlib import Path

# Add colors for terminal output
class Colors:
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    BOLD = '\033[1m'
    END = '\033[0m'

def print_slow(text, delay=0.03):
    """Print text with typewriter effect"""
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    print()

def clear_screen():
    """Clear the terminal screen"""
    print("\033[2J\033[H")

def run_zelda_command(command):
    """Simulate running a @zelda command"""
    print(f"{Colors.CYAN}$ {command}{Colors.END}")
    time.sleep(0.5)
    
    # Call the actual hook
    input_data = json.dumps({
        "hook_event_name": "UserPromptSubmit",
        "prompt": command
    })
    
    result = subprocess.run(
        ["python3", "hooks/zelda_hook.py"],
        input=input_data,
        capture_output=True,
        text=True
    )
    
    if result.returncode == 0 and result.stdout:
        output = json.loads(result.stdout)
        if output.get('decision') == 'block':
            # Parse and display the markdown nicely
            response = output.get('reason', '')
            print(response)
    
    time.sleep(1.5)

def simulate_coding():
    """Simulate some coding actions with sounds"""
    commands = [
        ("Bash", True, "Running tests..."),
        ("Edit", True, "Editing file..."),
        ("Read", True, "Reading documentation..."),
        ("Bash", True, "Building project..."),
        ("TodoWrite", True, "Completing todo..."),
    ]
    
    for tool, success, description in commands:
        print(f"\n{Colors.YELLOW}→ {description}{Colors.END}")
        time.sleep(0.5)
        
        # Simulate tool execution
        input_data = json.dumps({
            "hook_event_name": "PostToolUse",
            "tool_name": tool,
            "tool_status": "success" if success else "error"
        })
        
        subprocess.run(
            ["python3", "hooks/zelda_hook.py"],
            input=input_data,
            capture_output=True,
            text=True
        )
        
        if success:
            print(f"{Colors.GREEN}✓ Success!{Colors.END}")
        else:
            print(f"{Colors.RED}✗ Error!{Colors.END}")
        
        time.sleep(1)

def main():
    """Run the full demo"""
    clear_screen()
    
    # Title screen
    print(Colors.BOLD + Colors.CYAN)
    print("="*60)
    print("         🎮 ZELDA CLAUDE CODE DEMO 🎮")
    print("     Transform Coding Into An Adventure!")
    print("="*60)
    print(Colors.END)
    time.sleep(2)
    
    # Show installation
    print(f"\n{Colors.GREEN}📦 Installation (30 seconds!):{Colors.END}")
    print_slow("$ git clone https://github.com/linjiw/claude-code-but-zelda.git")
    print_slow("$ cd claude-code-but-zelda")
    print_slow("$ ./install.sh")
    print(f"{Colors.GREEN}✓ Installation complete!{Colors.END}")
    time.sleep(2)
    
    # Demo 1: Check stats
    print(f"\n{Colors.PURPLE}━━━ Demo 1: Check Your Stats ━━━{Colors.END}\n")
    run_zelda_command("@zelda stats")
    
    # Demo 2: Simulate some coding (with sounds)
    print(f"\n{Colors.PURPLE}━━━ Demo 2: Code With Sounds! ━━━{Colors.END}")
    print(f"{Colors.YELLOW}(Listen for Zelda sounds as we code!){Colors.END}")
    simulate_coding()
    time.sleep(1)
    
    # Demo 3: Check combo
    print(f"\n{Colors.PURPLE}━━━ Demo 3: Check Your Combo ━━━{Colors.END}\n")
    run_zelda_command("@zelda combo")
    
    # Demo 4: View achievements
    print(f"\n{Colors.PURPLE}━━━ Demo 4: View Achievements ━━━{Colors.END}\n")
    run_zelda_command("@zelda achievements")
    
    # Demo 5: Configure settings
    print(f"\n{Colors.PURPLE}━━━ Demo 5: Configure Settings ━━━{Colors.END}\n")
    run_zelda_command("@zelda config volume 75")
    
    # Demo 6: Get help
    print(f"\n{Colors.PURPLE}━━━ Demo 6: Get Help ━━━{Colors.END}\n")
    run_zelda_command("@zelda help")
    
    # Ending
    print(f"\n{Colors.BOLD}{Colors.GREEN}🎉 Ready to start your adventure?{Colors.END}")
    print(f"\n{Colors.CYAN}Install now:{Colors.END}")
    print("github.com/linjiw/claude-code-but-zelda")
    print(f"\n{Colors.YELLOW}May the Triforce guide your code! 🗡️✨{Colors.END}\n")

if __name__ == "__main__":
    print("\n🎬 Starting demo in 3 seconds...")
    print("   (Start recording now!)")
    time.sleep(3)
    main()