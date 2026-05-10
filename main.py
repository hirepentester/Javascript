"""
Main entry point for ML JavaScript Analyzer
This file is kept for compatibility with deployment configs.
Use ml_analyzer.py directly for the ML analyzer.
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

if __name__ == "__main__":
    from ml_analyzer import main
    main()
