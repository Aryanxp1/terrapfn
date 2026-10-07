"""TerraPFN - Root Entrypoint for Cloud Deployment (Streamlit Cloud & Hugging Face Spaces).

Delegates to src/terrapfn/app/dashboard.py while ensuring sys.path and environment
are properly configured across Linux, macOS, and Windows containers.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

# Add src to sys.path
root_dir = Path(__file__).resolve().parent
src_dir = root_dir / "src"
if str(src_dir) not in sys.path:
    sys.path.insert(0, str(src_dir))

# Execute main dashboard
from terrapfn.app.dashboard import main

main()

