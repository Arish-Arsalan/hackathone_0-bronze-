# -*- coding: utf-8 -*-
#!/usr/bin/env python3
"""
MCP Server - Handles external actions like sending emails
Silver Tier requirement: MCP server for external actions
"""

import json
import time
from pathlib import Path

class MCPServer:
    def __init__(self):
        self.vault_path = Path(__file__).parent.parent
        self.actions_queue = self.vault_path / 'Vault' / 'actions_queue'
        self.actions_queue.mkdir(exist_ok=True)
        
    def send_email(self, to_email, subject, body):
        """Simulate sending email"""
        print(f"MCP SERVER: Sending email to {to_email}")
        print(f"   Subject: {subject}")
        print(f"   Body: {body[:50]}...")
        return {"status": "sent", "message_id": f"msg_{int(time.time())}"}
    
    def process_action_queue(self):
        """Process queued actions"""
        queue_files = list(self.actions_queue.glob("*.json"))
        for file_path in queue_files:
            try:
                # Read file with proper encoding handling
                content = file_path.read_text(encoding='utf-8', errors='replace')
                action = json.loads(content)
                
                if action['type'] == 'send_email':
                    result = self.send_email(
                        action['to'], 
                        action['subject'], 
                        action['body']
                    )
                    print(f"   Result: {result}")
                
                # Move processed file to archive
                archive_path = self.actions_queue / 'archive'
                archive_path.mkdir(exist_ok=True)
                file_path.rename(archive_path / file_path.name)
                
            except json.JSONDecodeError:
                print(f"MCP ERROR: Invalid JSON in {file_path.name}")
            except UnicodeDecodeError:
                print(f"MCP ERROR: Encoding issue with {file_path.name}")
            except Exception as e:
                print(f"MCP ERROR: {e}")

def main():
    print("MCP SERVER STARTED")
    print("Silver Tier: External action server")
    
    mcp = MCPServer()
    
    while True:
        mcp.process_action_queue()
        time.sleep(10)

if __name__ == "__main__":
    main()
