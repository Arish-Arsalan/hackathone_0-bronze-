#!/bin/bash
# ralph-loop.sh - Execute a single Ralph Wiggum loop iteration

VAULT_PATH="${1:-$HOME/AI_Employee_Vault}"

echo "🔄 Starting Ralph Wiggum loop for: $VAULT_PATH"

python "$VAULT_PATH/watchers/orchestrator.py" << 'EOF'
You are my AI Employee. Process all items in /Needs_Action. Create Plans.md for complex tasks. Require approval for sensitive actions.

## CRITICAL RULES
1. ALWAYS require human approval for payments >$50
2. NEVER delete original files - move to /Done after processing
3. When in doubt, create approval request in /Pending_Approval

## COMPLETION CRITERIA
Output <TASK_COMPLETE> when finished.
EOF