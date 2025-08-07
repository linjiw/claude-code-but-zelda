#!/usr/bin/env python3
"""
Zelda Sound Store Search Tool
Parse and search through the zelda-sound-store.txt to find specific sounds
"""

import re
import json
from pathlib import Path
from typing import List, Dict, Optional
from dataclasses import dataclass
import argparse

# Simple color codes for terminal output  
class Fore:
    @staticmethod
    def _wrap(color, text):
        return f"{color}{text}\033[0m"
    
    @staticmethod
    def RED(text):
        return Fore._wrap('\033[91m', text)
    
    @staticmethod
    def GREEN(text):
        return Fore._wrap('\033[92m', text)
    
    @staticmethod
    def YELLOW(text):
        return Fore._wrap('\033[93m', text)
    
    @staticmethod
    def BLUE(text):
        return Fore._wrap('\033[94m', text)
    
    @staticmethod
    def CYAN(text):
        return Fore._wrap('\033[96m', text)
    
    @staticmethod
    def WHITE(text):
        return Fore._wrap('\033[97m', text)

@dataclass
class Sound:
    id: int
    name: str
    duration: str
    size: str
    
    def __str__(self):
        return f"#{self.id:04d} | {self.name:<40} | {self.duration:>6} | {self.size:>8}"

class ZeldaSoundDatabase:
    def __init__(self, file_path: str = "docs/zelda-sound-store.txt"):
        self.file_path = Path(file_path)
        self.sounds: List[Sound] = []
        self.load_sounds()
    
    def load_sounds(self):
        """Parse the sound store text file"""
        if not self.file_path.exists():
            print(Fore.RED(f"Error: {self.file_path} not found!"))
            return
        
        with open(self.file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Pattern to match sound entries
        # Format: number.\nname\nduration\nsize
        pattern = r'(\d+)\.\s*\n([^\n]+)\n(\d+:\d+)\n([\d.]+ [MK]B)'
        
        matches = re.finditer(pattern, content)
        
        for match in matches:
            sound_id = int(match.group(1))
            name = match.group(2).strip()
            duration = match.group(3)
            size = match.group(4)
            
            self.sounds.append(Sound(sound_id, name, duration, size))
        
        print(Fore.GREEN(f"Loaded {len(self.sounds)} sounds from database"))
    
    def search(self, query: str, case_sensitive: bool = False) -> List[Sound]:
        """Search for sounds by name"""
        results = []
        
        if not case_sensitive:
            query = query.lower()
        
        for sound in self.sounds:
            search_name = sound.name if case_sensitive else sound.name.lower()
            if query in search_name:
                results.append(sound)
        
        return results
    
    def search_multiple(self, queries: List[str], case_sensitive: bool = False) -> Dict[str, List[Sound]]:
        """Search for multiple queries at once"""
        results = {}
        for query in queries:
            results[query] = self.search(query, case_sensitive)
        return results
    
    def get_by_id(self, sound_id: int) -> Optional[Sound]:
        """Get a sound by its ID number"""
        for sound in self.sounds:
            if sound.id == sound_id:
                return sound
        return None
    
    def get_by_ids(self, sound_ids: List[int]) -> List[Sound]:
        """Get multiple sounds by their IDs"""
        results = []
        for sid in sound_ids:
            sound = self.get_by_id(sid)
            if sound:
                results.append(sound)
        return results
    
    def export_results(self, results: List[Sound], output_file: str = "sound_shopping_list.txt"):
        """Export search results to a file"""
        with open(output_file, 'w') as f:
            f.write("ZELDA SOUND SHOPPING LIST\n")
            f.write("=" * 60 + "\n\n")
            
            total_duration = 0
            total_size = 0.0
            
            for sound in results:
                f.write(f"{sound}\n")
                
                # Calculate totals
                mins, secs = map(int, sound.duration.split(':'))
                total_duration += mins * 60 + secs
                
                size_val = float(sound.size.split()[0])
                size_unit = sound.size.split()[1]
                if size_unit == "MB":
                    total_size += size_val
                elif size_unit == "KB":
                    total_size += size_val / 1024
            
            f.write("\n" + "=" * 60 + "\n")
            f.write(f"Total sounds: {len(results)}\n")
            f.write(f"Total duration: {total_duration // 60}:{total_duration % 60:02d}\n")
            f.write(f"Total size: {total_size:.2f} MB\n")
        
        print(Fore.GREEN(f"Shopping list saved to {output_file}"))
    
    def show_stats(self):
        """Display database statistics"""
        print("\n" + Fore.CYAN('='*60))
        print(Fore.CYAN("ZELDA SOUND DATABASE STATISTICS"))
        print(Fore.CYAN('='*60))
        print(f"Total sounds: {len(self.sounds)}")
        
        if self.sounds:
            print(f"ID range: #{self.sounds[0].id:04d} - #{self.sounds[-1].id:04d}")
            
            # Find some interesting sounds
            keywords = ['battle', 'shrine', 'item', 'get', 'complete', 'fail', 
                       'success', 'damage', 'game over', 'rupee', 'heart']
            
            print("\n" + Fore.YELLOW("Interesting categories found:"))
            for keyword in keywords:
                count = len(self.search(keyword))
                if count > 0:
                    print(f"  • {keyword.capitalize()}: {count} sounds")

def get_needed_sounds_for_claude_code():
    """Return list of sound types needed for Claude Code integration"""
    return {
        # Core sounds
        "success": ["success", "complete", "correct", "yes", "achievement"],
        "error": ["error", "fail", "wrong", "no", "damage", "miss"],
        "warning": ["warning", "alert", "attention", "caution", "assassin appear"],
        "notification": ["notify", "hey listen", "navi", "alert", "message"],
        
        # Combat/Execution
        "sword_draw": ["sword draw", "sword out", "weapon ready", "battle start"],
        "enemy_defeated": ["enemy defeat", "victory", "win", "monster die"],
        "damage": ["damage", "hurt", "hit", "ouch"],
        "game_over": ["game over", "death", "fail", "lose"],
        
        # Discovery/Search
        "secret_discovered": ["secret", "discover", "found", "reveal", "hidden"],
        "item_get": ["item get", "obtain", "acquire", "receive", "pickup"],
        "rupee_collect": ["rupee", "money", "coin", "treasure"],
        "shrine_complete": ["shrine complete", "shrine clear", "puzzle solve"],
        
        # Quest/Todo
        "quest_start": ["quest start", "mission begin", "adventure"],
        "quest_complete": ["quest complete", "mission complete", "task done"],
        "heart_container": ["heart", "health", "life up"],
        "master_sword": ["master sword", "legendary", "ultimate"],
        
        # Session
        "wake_up": ["wake up", "morning", "start", "begin", "hello"],
        "save_game": ["save", "record", "checkpoint"],
        "menu_navigate": ["menu", "select", "navigate", "browse"],
        
        # Special
        "companion_summon": ["summon", "call", "companion", "helper"],
        "memory_unlock": ["memory", "remember", "flashback", "recall"],
        "sheikah_activate": ["sheikah", "technology", "ancient", "scan"],
        
        # Ambience
        "morning_theme": ["morning", "dawn", "sunrise"],
        "night_theme": ["night", "evening", "dark"],
        "battle_music": ["battle music", "combat theme", "fight"],
    }

def main():
    parser = argparse.ArgumentParser(description="Search Zelda Sound Database")
    parser.add_argument("action", choices=["search", "id", "needed", "stats"], 
                       help="Action to perform")
    parser.add_argument("query", nargs="*", 
                       help="Search query or sound ID(s)")
    parser.add_argument("-e", "--export", action="store_true",
                       help="Export results to file")
    parser.add_argument("-c", "--case-sensitive", action="store_true",
                       help="Case-sensitive search")
    
    args = parser.parse_args()
    
    # Initialize database
    db = ZeldaSoundDatabase()
    
    if args.action == "stats":
        db.show_stats()
    
    elif args.action == "search":
        if not args.query:
            print(Fore.RED("Please provide a search term"))
            return
        
        query = " ".join(args.query)
        results = db.search(query, args.case_sensitive)
        
        if results:
            print(Fore.GREEN(f"\nFound {len(results)} matches for '{query}':\n"))
            print(Fore.YELLOW(f"{'ID':<6} | {'Name':<40} | {'Duration':>8} | {'Size':>10}"))
            print("-" * 70)
            
            for sound in results[:20]:  # Show first 20 results
                print(Fore.WHITE(str(sound)))
            
            if len(results) > 20:
                print(Fore.YELLOW(f"\n... and {len(results) - 20} more results"))
            
            if args.export:
                db.export_results(results, f"search_{query.replace(' ', '_')}.txt")
        else:
            print(Fore.RED(f"No results found for '{query}'"))
    
    elif args.action == "id":
        if not args.query:
            print(Fore.RED("Please provide sound ID(s)"))
            return
        
        ids = [int(q) for q in args.query if q.isdigit()]
        results = db.get_by_ids(ids)
        
        if results:
            print(Fore.GREEN(f"\nFound {len(results)} sounds:\n"))
            for sound in results:
                print(Fore.WHITE(str(sound)))
            
            if args.export:
                db.export_results(results, "selected_sounds.txt")
        else:
            print(Fore.RED("No sounds found with those IDs"))
    
    elif args.action == "needed":
        print(Fore.CYAN("\nSEARCHING FOR CLAUDE CODE NEEDED SOUNDS..."))
        print("=" * 70)
        
        needed = get_needed_sounds_for_claude_code()
        all_results = []
        shopping_list = []
        
        for category, keywords in needed.items():
            print(Fore.YELLOW(f"\nCategory: {category.upper()}"))
            found_any = False
            
            for keyword in keywords:
                results = db.search(keyword)
                if results:
                    # Show best match
                    best_match = results[0]
                    print(Fore.GREEN(f"  ✓ '{keyword}' → {best_match.name} (#{best_match.id:04d})"))
                    if not found_any:
                        shopping_list.append(best_match)
                        found_any = True
                    break
            
            if not found_any:
                print(Fore.RED(f"  ✗ No matches found for: {', '.join(keywords)}"))
        
        if args.export or True:  # Always export for needed sounds
            db.export_results(shopping_list, "claude_code_shopping_list.txt")
            
            # Also create a JSON mapping file
            mapping = {}
            for sound in shopping_list:
                # Create a simple key from the sound name
                key = sound.name.lower().replace(" ", "_")
                mapping[key] = {
                    "id": sound.id,
                    "name": sound.name,
                    "duration": sound.duration,
                    "size": sound.size
                }
            
            with open("sound_id_mapping.json", "w") as f:
                json.dump(mapping, f, indent=2)
            
            print(Fore.GREEN(f"\nCreated sound_id_mapping.json with {len(mapping)} sounds"))

if __name__ == "__main__":
    main()