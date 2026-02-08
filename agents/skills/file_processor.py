# -*- coding: utf-8 -*-
"""
Skill: File Processor
Handles processing files in Needs_Action folder
Bronze Tier requirement: All AI functionality as Agent Skills
"""

from pathlib import Path
import time
from datetime import datetime, timezone

def count_pending_actions(agent):
    """Count files needing processing"""
    folders = agent.get_vault_folders()
    needs_action = folders['needs_action']
    
    md_files = list(needs_action.glob('*.md'))
    txt_files = list(needs_action.glob('*.txt'))
    
    return len(md_files) + len(txt_files)

def process_needs_action(agent):
    """Process files in Needs_Action folder using file processing skill"""
    folders = agent.get_vault_folders()
    needs_action = folders['needs_action']
    
    files_to_process = list(needs_action.glob('*.md')) + list(needs_action.glob('*.txt'))
    
    if not files_to_process:
        print("NO FILES TO PROCESS IN NEEDS_ACTION")
        return
    
    print(f"PROCESSING {len(files_to_process)} FILES IN NEEDS_ACTION...")
    
    for file_path in files_to_process:
        print(f"PROCESSING: {file_path.name}")
        
        # Read file content
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Analyze content and determine next action
        if 'invoice' in content.lower() or 'payment' in content.lower():
            # Use plan generator skill
            if hasattr(agent.skills.get('plan_generator'), 'create_plan'):
                agent.skills['plan_generator'].create_plan(agent, file_path, content)
            else:
                create_plan_fallback(agent, file_path, content)
        
        elif 'client' in content.lower() or 'request' in content.lower():
            # Use communication skill
            if hasattr(agent.skills.get('communication'), 'handle_client_request'):
                agent.skills['communication'].handle_client_request(agent, file_path, content)
            else:
                handle_client_request_fallback(agent, file_path, content)
        
        print(f"PROCESSED: {file_path.name}")

def create_plan_fallback(agent, file_path, content):
    """Fallback plan creation if plan_generator skill not loaded"""
    folders = agent.get_vault_folders()
    plans_folder = folders['plans']
    
    timestamp = int(time.time())
    plan_file = plans_folder / f"PLAN_{timestamp}_auto.md"
    
    with open(plan_file, 'w', encoding='utf-8') as f:
        f.write(f"""---
created: {datetime.now(timezone.utc).isoformat()}
type: plan
source_file: {file_path.name}
status: pending
---

## Auto-Generated Plan

Based on: {file_path.name}

Content Analysis:
{content}

## Recommended Actions:
1. Review invoice details
2. Create approval request if amount > $50
3. Move to Pending_Approval for human review

<TASK_COMPLETE>
""")
    
    print(f"CREATED PLAN: {plan_file.name}")

def handle_client_request_fallback(agent, file_path, content):
    """Fallback client request handling"""
    folders = agent.get_vault_folders()
    pending_approval = folders['pending_approval']
    
    timestamp = int(time.time())
    approval_file = pending_approval / f"CLIENT_REQUEST_{timestamp}.md"
    
    with open(approval_file, 'w', encoding='utf-8') as f:
        f.write(f"""---
created: {datetime.now(timezone.utc).isoformat()}
type: client_request
source_file: {file_path.name}
status: pending_approval
---

## Client Request Analysis

Source: {file_path.name}

Content:
{content}

## Action Required:
Please review and approve this client request.

Approve by moving to Approved folder.
""")
    
    print(f"CREATED APPROVAL REQUEST: {approval_file.name}")
