# -*- coding: utf-8 -*-
"""
Skill: Approval Manager
Handles processing approved files
Bronze Tier requirement: All AI functionality as Agent Skills
"""

import shutil
from pathlib import Path

def process_approved_files(agent):
    """Process files that have been approved"""
    folders = agent.get_vault_folders()
    approved_folder = folders['approved']
    done_folder = folders['done']
    
    approved_files = list(approved_folder.glob('*.md'))
    
    if not approved_files:
        print("NO APPROVED FILES TO PROCESS")
        return
    
    print(f"PROCESSING {len(approved_files)} APPROVED FILES...")
    
    for file_path in approved_files:
        print(f"EXECUTING APPROVED ACTION: {file_path.name}")
        
        # Move to Done folder
        destination = done_folder / file_path.name
        shutil.move(str(file_path), str(destination))
        
        print(f"COMPLETED: {file_path.name} -> DONE")
