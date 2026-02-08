# -*- coding: utf-8 -*-
#!/usr/bin/env python3
"""
AI Employee Agent - Main controller for all skills
Implements the Ralph Wiggum autonomous completion loop
Bronze Tier requirement: All AI functionality as Agent Skills
"""

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')
import os
import time
from pathlib import Path
from datetime import datetime, timezone
import importlib.util

class AIEmployee:
    """Main AI Employee agent that coordinates all skills"""
    
    def __init__(self, vault_path=None):
        self.vault_path = Path(vault_path) if vault_path else Path(__file__).parent.parent
        self.load_skills()
        
    def load_skills(self):
        """Dynamically load all available skills"""
        skills_dir = self.vault_path / 'agents' / 'skills'
        self.skills = {}
        
        # Import each skill module
        for skill_file in skills_dir.glob('*.py'):
            if skill_file.name != '__init__.py':
                skill_name = skill_file.stem
                spec = importlib.util.spec_from_file_location(skill_name, skill_file)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                self.skills[skill_name] = module
                print(f"LOADED SKILL: {skill_name}")
    
    def get_vault_folders(self):
        """Get all vault folder paths"""
        return {
            'inbox': self.vault_path / 'Vault' / 'Inbox',
            'needs_action': self.vault_path / 'Vault' / 'Needs_Action',
            'pending_approval': self.vault_path / 'Vault' / 'Pending_Approval',
            'approved': self.vault_path / 'Vault' / 'Approved',
            'done': self.vault_path / 'Vault' / 'Done',
            'plans': self.vault_path / 'Vault' / 'Plans',
            'dashboard': self.vault_path / 'Vault' / 'Dashboard.md'
        }
    
    def ralph_wiggum_loop(self, max_iterations=3):
        """Ralph Wiggum autonomous completion loop - Bronze Tier requirement"""
        print(f"\n{'='*60}")
        print("RALPH WIGGUM AUTONOMOUS LOOP STARTED")
        print(f"{'='*60}")
        
        for iteration in range(max_iterations):
            print(f"\nITERATION {iteration + 1}/{max_iterations}")
            
            # Use file processor skill
            if 'file_processor' in self.skills:
                self.skills['file_processor'].process_needs_action(self)
            
            # Use approval manager skill
            if 'approval_manager' in self.skills:
                self.skills['approval_manager'].process_approved_files(self)
            
            # Use dashboard updater skill
            if 'dashboard_updater' in self.skills:
                self.skills['dashboard_updater'].update_dashboard(self)
            
            time.sleep(5)  # Short delay between iterations
        
        print(f"\nRALPH WIGGUM LOOP COMPLETED {max_iterations} ITERATIONS")

def main():
    print("AI EMPLOYEE AGENT STARTED")
    print("LOADING AGENT SKILLS...")
    
    agent = AIEmployee()
    
    print("STARTING RALPH WIGGUM AUTONOMOUS LOOP...")
    try:
        while True:
            agent.ralph_wiggum_loop(max_iterations=2)
            time.sleep(15)  # Wait between loops
    except KeyboardInterrupt:
        print("\nAI EMPLOYEE AGENT STOPPED")

if __name__ == "__main__":
    main()
