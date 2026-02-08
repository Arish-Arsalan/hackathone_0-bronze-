# -*- coding: utf-8 -*-
#!/usr/bin/env python3
"""
Automated Scheduler - Basic scheduling system
Silver Tier requirement: Basic scheduling via cron or Task Scheduler
"""

import time
import threading
from datetime import datetime, timedelta
from pathlib import Path

class TaskScheduler:
    def __init__(self):
        self.vault_path = Path(__file__).parent.parent
        self.tasks = []
        
    def add_task(self, interval_seconds, task_function, *args, **kwargs):
        """Add a recurring task"""
        task = {
            'interval': interval_seconds,
            'function': task_function,
            'args': args,
            'kwargs': kwargs,
            'last_run': 0
        }
        self.tasks.append(task)
        
    def run_tasks(self):
        """Run scheduled tasks"""
        current_time = time.time()
        
        for task in self.tasks:
            if current_time - task['last_run'] >= task['interval']:
                try:
                    task['function'](*task['args'], **task['kwargs'])
                    task['last_run'] = current_time
                except Exception as e:
                    print(f"❌ SCHEDULER ERROR: {e}")
    
    def start(self):
        """Start the scheduler"""
        print("⏰ AUTOMATED SCHEDULER STARTED")
        print("Silver Tier: Basic scheduling system")
        
        while True:
            self.run_tasks()
            time.sleep(1)

def main():
    scheduler = TaskScheduler()
    
    # Add LinkedIn post scheduling (every 2 hours)
    try:
        from agents.ai_employee import AIEmployee
        from agents.skills.linkedin_publisher import generate_linkedin_post
        
        agent = AIEmployee()
        scheduler.add_task(7200, generate_linkedin_post, agent, "AI_Employee")
    except ImportError:
        pass
    
    scheduler.start()

if __name__ == "__main__":
    main()
