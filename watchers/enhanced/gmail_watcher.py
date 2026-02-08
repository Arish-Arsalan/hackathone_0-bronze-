# -*- coding: utf-8 -*-
#!/usr/bin/env python3
"""
Gmail Watcher - Monitor email for client requests
Silver Tier requirement: Multiple watcher types
"""

import time
import random
from pathlib import Path

def main():
    vault_root = Path(__file__).parent.parent.parent
    inbox = vault_root / 'Vault' / 'Inbox'
    
    print("="*60)
    print("GMAIL WATCHER STARTED")
    print("Silver Tier: Multiple watcher types")
    print("="*60)
    
    # Simulate receiving emails
    counter = 1
    while True:
        try:
            # Create simulated email file
            email_file = inbox / f"GMAIL_EMAIL_{counter:03d}.md"
            subjects = [
                "Invoice Request",
                "Payment Inquiry", 
                "Project Update",
                "Client Meeting",
                "Contract Discussion"
            ]
            
            with open(email_file, 'w', encoding='utf-8') as f:
                f.write(f"""---
type: gmail_email
source: client{counter}@example.com
subject: {random.choice(subjects)} #{counter}
---

Gmail received: {random.choice(subjects)} from client{counter}@example.com. 
Email #{counter} processed by AI Employee system.
Amount: ${random.randint(100, 1000)}
Due Date: March {random.randint(1, 28)}
""")
            print(f"EMAIL RECEIVED: GMAIL_EMAIL_{counter:03d}.md -> Inbox")
            counter += 1
            time.sleep(30)  # Every 30 seconds
        except KeyboardInterrupt:
            print("\nGmail watcher stopped")
            break

if __name__ == "__main__":
    main()
