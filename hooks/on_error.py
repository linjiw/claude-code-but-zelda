#!/usr/bin/env python3
import subprocess
import sys
from pathlib import Path
sound_path = Path("/Users/linji/Downloads/zelda_claude") / "sounds" / "error.wav"
subprocess.Popen(["afplay", str(sound_path)],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL)
sys.exit(0)
