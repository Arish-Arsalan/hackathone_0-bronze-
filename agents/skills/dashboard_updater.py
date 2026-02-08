# -*- coding: utf-8 -*-
"""
Skill: Dashboard Updater
Updates Dashboard.md with current system status
Bronze Tier requirement: All AI functionality as Agent Skills
"""

from pathlib import Path
from datetime import datetime, timezone

def update_dashboard(agent):
    """Update Dashboard.md with current system status"""
    folders = agent.get_vault_folders()
    dashboard_path = folders['dashboard']
    
    # Count files in each folder
    counts = {}
    for folder_name, folder_path in folders.items():
        if folder_name != 'dashboard':
            if folder_path.exists():
                counts[folder_name] = len(list(folder_path.glob('*.md'))) + len(list(folder_path.glob('*.txt')))
            else:
                counts[folder_name] = 0
    
    # Create dashboard content
    content = f"""---
last_updated: {datetime.now(timezone.utc).isoformat()}
status: operational
bank_balance: $0.00
pending_actions: {counts.get('needs_action', 0)}
awaiting_approval: {counts.get('pending_approval', 0)}
---

# AI Employee Dashboard

## System Metrics
- **Pending actions:** {counts.get('needs_action', 0)}
- **Pending approvals:** {counts.get('pending_approval', 0)}
- **Completed tasks:** {counts.get('done', 0)}
- **System status:** operational

## Recent Activity
*{datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')} - System check: {counts.get('needs_action', 0)} pending, {counts.get('pending_approval', 0)} awaiting approval*

## Folder Status
- **Inbox:** {counts.get('inbox', 0)} items
- **Needs Action:** {counts.get('needs_action', 0)} items
- **Pending Approval:** {counts.get('pending_approval', 0)} items
- **Approved:** {counts.get('approved', 0)} items
- **Done:** {counts.get('done', 0)} items
- **Plans:** {counts.get('plans', 0)} items
"""
    
    # Write dashboard
    with open(dashboard_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"DASHBOARD UPDATED: {counts.get('needs_action', 0)} ACTIONS, {counts.get('pending_approval', 0)} APPROVALS")
