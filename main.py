"""
Main entry point for SnapTeX application.
"""

import streamlit.web.cli as stcli
import sys
from pathlib import Path

# Add ui directory to path
sys.path.insert(0, str(Path(__file__).parent))

if __name__ == "__main__":
    # Run Streamlit app
    sys.argv = ["streamlit", "run", "ui/streamlit_app.py"]
    sys.exit(stcli.main())


