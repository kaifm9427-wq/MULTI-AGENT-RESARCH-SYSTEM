#!/usr/bin/env python3
"""
Start ResearchMind server from project root
Handles path setup and runs the backend server
"""

import sys
import os
from pathlib import Path

def main():
    # Get project root
    project_root = Path(__file__).resolve().parent
    backend_path = project_root / "backend"
    
    # Add backend to Python path so imports work
    sys.path.insert(0, str(backend_path))
    
    # Change to backend directory for relative imports
    os.chdir(backend_path)
    
    # Import after path setup
    import uvicorn
    from server import app
    
    print(f"""
╔════════════════════════════════════════════════════════════╗
║                  ResearchMind Starting...                  ║
╚════════════════════════════════════════════════════════════╝

🚀 Server Details:
   • URL (Local):   http://localhost:8000
   • URL (Network): http://127.0.0.1:8000
   • URL (All):     http://0.0.0.0:8000
   • Backend: FastAPI with Uvicorn
   • Frontend: Premium dark theme
   • Status: Starting on all interfaces...

💡 Commands:
   • Open browser: http://localhost:8000
   • Test suite: python backend/tests/test_premium_ui.py
   • Stop server: Press Ctrl+C

════════════════════════════════════════════════════════════════
""")
    
    try:
        # Listen on all interfaces so Safari and other browsers can connect
        uvicorn.run(
            app,
            host="0.0.0.0",  # Listen on all interfaces
            port=8000,
            log_level="info"
        )
    except KeyboardInterrupt:
        print("\n\n✅ Server stopped gracefully")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
