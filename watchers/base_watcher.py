#!/usr/bin/env python3
"""
Base watcher template for all watchers
"""

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')
import os
import time
import logging
from pathlib import Path
from datetime import datetime, timezone

class BaseWatcher:
    """Template for all watchers"""
    
    def __init__(self, vault_path=None, check_interval=60):
        self.vault_path = Path(vault_path) if vault_path else Path(__file__).parent.parent.parent
        self.check_interval = check_interval
        self.setup_logging()
        
    def setup_logging(self):
        """Setup logging for the watcher"""
        log_dir = self.vault_path / 'Logs'
        log_dir.mkdir(exist_ok=True)
        
        logger = logging.getLogger(self.__class__.__name__)
        logger.setLevel(logging.INFO)
        
        # File handler
        file_handler = logging.FileHandler(log_dir / f"{self.__class__.__name__}.log")
        file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
        logger.addHandler(file_handler)
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
        logger.addHandler(console_handler)
        
        self.logger = logger
    
    def check_for_updates(self):
        """Return list of new items to process"""
        pass
    
    def create_action_file(self, item):
        """Create .md file in Needs_Action folder"""
        pass
    
    def run(self):
        """Main monitoring loop"""
        self.logger.info(f"Starting {self.__class__.__name__}...")
        while True:
            try:
                items = self.check_for_updates()
                for item in items:
                    self.create_action_file(item)
                time.sleep(self.check_interval)
            except Exception as e:
                self.logger.error(f"Error in {self.__class__.__name__} loop: {e}")
                time.sleep(60)  # Wait before retrying

if __name__ == "__main__":
    watcher = BaseWatcher()
    watcher.run()