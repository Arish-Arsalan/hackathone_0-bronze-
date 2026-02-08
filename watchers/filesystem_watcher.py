# -*- coding: utf-8 -*-
#!/usr/bin/env python3
"""
Filesystem Watcher - Monitors Inbox and moves files to Needs_Action
Part of Agent Skills architecture
"""

import time
import shutil
from pathlib import Path

def main():
    # Define folder paths - corrected for Vault subdirectory
    vault_root = Path(__file__).parent.parent
    inbox = vault_root / 'Vault' / 'Inbox'
    needs_action = vault_root / 'Vault' / 'Needs_Action'
    
    # Create folders if they don't exist
    inbox.mkdir(parents=True, exist_ok=True)
    needs_action.mkdir(parents=True, exist_ok=True)
    
    print("="*60)
    print("FILESYSTEM WATCHER STARTED")
    print("AGENT SKILLS ARCHITECTURE: File Monitoring")
    print("="*60)
    print(f"Watching: {inbox}")
    print(f"Moving to: {needs_action}")
    print("Auto-moving .md/.txt files every 5 seconds...")
    print("="*60 + "\n")

    while True:
        try:
            # Look for .md and .txt files
            files = list(inbox.glob("*.md")) + list(inbox.glob("*.txt"))
            
            if files:
                for file in files:
                    destination = needs_action / file.name
                    shutil.move(str(file), str(destination))
                    print(f"MOVED: {file.name} -> Needs_Action")
            else:
                # Optional: print dots to show it's still running
                print(".", end="", flush=True)
                
            time.sleep(5)
        except Exception as e:
            print(f"ERROR: {e}")
            time.sleep(5)

if __name__ == "__main__":
    main()
