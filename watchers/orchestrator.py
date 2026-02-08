#!/usr/bin/env python3
import os
import time
import shutil
from pathlib import Path
from datetime import datetime, timezone

class Orchestrator:
    def __init__(self, vault_path=None):
        self.vault_path = Path(vault_path) if vault_path else Path(__file__).parent.parent.parent
        self.needs_action = self.vault_path / 'Needs_Action'
        self.plans = self.vault_path / 'Plans'
        self.pending_approval = self.vault_path / 'Pending_Approval'
        self.approved = self.vault_path / 'Approved'
        self.done = self.vault_path / 'Done'
        self.dashboard = self.vault_path / 'Dashboard.md'
        for folder in [self.needs_action, self.plans, self.pending_approval, self.approved, self.done, self.vault_path / 'Logs']:
            folder.mkdir(exist_ok=True)
    
    def count_pending_actions(self):
        return len(list(self.needs_action.glob('*.md')))
    
    def count_pending_approvals(self):
        return len(list(self.pending_approval.glob('*.md')))
    
    def update_dashboard(self):
        try:
            if self.dashboard.exists():
                with open(self.dashboard, 'r', encoding='utf-8') as f:
                    content = f.read()
            else:
                content = "---\nlast_updated: 2026-01-27T00:00:00Z\nstatus: operational\nbank_balance: $0.00\npending_actions: 0\nawaiting_approval: 0\n---\n# AI Employee Dashboard\n"
            now = datetime.now(timezone.utc).isoformat()
            pending_actions = self.count_pending_actions()
            pending_approvals = self.count_pending_approvals()
            content = content.replace('last_updated: 2026-01-27T00:00:00Z', f'last_updated: {now}')
            content = content.replace('pending_actions: 0', f'pending_actions: {pending_actions}')
            content = content.replace('awaiting_approval: 0', f'awaiting_approval: {pending_approvals}')
            with open(self.dashboard, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Dashboard updated: {pending_actions} actions, {pending_approvals} approvals")
        except Exception as e:
            print(f"Failed to update dashboard: {e}")
    
    def ralph_wiggum_loop(self, prompt, max_iterations=2):
        print(f"\n{'='*60}")
        print(f"Starting Ralph Wiggum Loop")
        print(f"{'='*60}\n")
        for iteration in range(1, max_iterations + 1):
            print(f"Iteration {iteration}/{max_iterations}")
            time.sleep(1)
            if iteration == 1 and self.count_pending_actions() > 0:
                plan_file = self.plans / f"PLAN_{int(time.time())}_simulated.md"
                with open(plan_file, 'w', encoding='utf-8') as f:
                    f.write(f"""---
created: {datetime.now(timezone.utc).isoformat()}
type: plan
status: pending
---

Simulated Execution Plan
Based on items in Needs_Action:
1. Review file content
2. Categorize document type
3. Create approval request if needed
<TASK_COMPLETE>
""")
                print(f"PLAN CREATED: {plan_file.name}")
        print("Ralph Wiggum loop completed")
        return True
    
    def process_approvals(self):
        approved_files = list(self.approved.glob('*.md'))
        for file in approved_files:
            print(f"Processing: {file.name}")
            try:
                shutil.move(str(file), str(self.done / file.name))
                print(f"  Moved to Done/{file.name}")
            except Exception as e:
                print(f"Error: {e}")
    
    def run(self):
        print("\n" + "="*60)
        print("AI EMPLOYEE ORCHESTRATOR STARTED")
        print("="*60)
        print(f"VAULT: {self.vault_path}")
        print(f"MODE: DRY RUN (safe)")
        print("\nREADY FOR WORK")
        print("  - Drop files into Inbox folder")
        print("  - Check Pending_Approval for requests")
        print("\n" + "="*60 + "\n")
        self.update_dashboard()
        try:
            while True:
                self.process_approvals()
                pending = self.count_pending_actions()
                if pending > 0:
                    print(f"\nProcessing {pending} pending actions...")
                    self.ralph_wiggum_loop(f"Process {pending} items", max_iterations=2)
                self.update_dashboard()
                time.sleep(10)
        except KeyboardInterrupt:
            print("\nOrchestrator shutdown complete")

if __name__ == "__main__":
    orchestrator = Orchestrator()
    orchestrator.run()
