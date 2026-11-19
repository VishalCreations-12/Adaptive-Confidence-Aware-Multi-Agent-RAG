import os
import sys
from pathlib import Path

# Add project root to sys.path
BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from scripts.run_reviewer_revision import run_reviewer_revision_experiments

def run_master_experiments():
    """Execute the master automated research experiment suite with true modular ablations."""
    run_reviewer_revision_experiments()

if __name__ == "__main__":
    run_master_experiments()
