# -*- coding: utf-8 -*-
#!/usr/bin/env python3
"""
Debug Filesystem Watcher - Shows detailed info
"""

import time
import shutil
from pathlib import Path

def main():
    vault_root = Path(__file__).parent.parent
    inbox = vault_root / 'Vault' / 'Inbox'
    needs_action = vault_root / 'Vault' / 'Needs_Action'
    
    inbox.mkdir(parents=True, exist_ok=True)
    needs_action.mkdir(parents=True, exist_ok=True)
    
    print(f"DEBUG: Inbox path: {inbox}")
    print(f"DEBUG: Needs_Action path: {needs_action}")
    print(f"DEBUG: Inbox exists: {inbox.exists()}")
    print(f"DEBUG: Needs_Action exists: {needs_action.exists()}")
    
    print("="*60)
    print("DEBUG FILESYSTEM WATCHER STARTED")
    print("="*60)

    while True:
        try:
            # Show current files in inbox
            files = list(inbox.glob("*.md")) + list(inbox.glob("*.txt"))
            print(f"DEBUG: Found {len(files)} files in inbox: {[f.name for f in files]}")
            
            if files:
                for file in files:
                    destination = needs_action / file.name
                    try:
                        shutil.move(str(file), str(destination))
                        print(f"MOVED: {file.name} -> Needs_Action")
                    except Exception as e:
                        print(f"ERROR moving {file.name}: {e}")
            else:
                print(".", end="", flush=True)
                
            time.sleep(5)
        except KeyboardInterrupt:
            print("\nDEBUG WATCHER STOPPED")
            break
        except Exception as e:
            print(f"ERROR: {e}")
            time.sleep(5)

if __name__ == "__main__":
    main()
