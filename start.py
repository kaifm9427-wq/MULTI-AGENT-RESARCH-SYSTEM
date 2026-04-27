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
    
    # Detect if running on Hugging Face Spaces
    is_hf_space = os.getenv("SPACE_ID") is not None
    
    if is_hf_space:
        port = 7860
        port_msg = "🚀 Running on Hugging Face Spaces (port 7860)"
    else:
        port = int(os.getenv("PORT", 8000))
        port_msg = f"🚀 Running locally (port {port})"
    
    print(f"""
╔════════════════════════════════════════════════════════════╗
║                  ResearchMind Starting...                  ║
╚════════════════════════════════════════════════════════════╝

{port_msg}
   • Backend: FastAPI with Uvicorn
   • Frontend: Premium dark theme
   • Status: Starting on all interfaces...

💡 Commands:
   • Open browser: http://localhost:{port}
   • Stop server: Press Ctrl+C

════════════════════════════════════════════════════════════════
""")
    
    try:
        # Listen on all interfaces so Safari and other browsers can connect
        uvicorn.run(
            app,
            host="0.0.0.0",  # Listen on all interfaces
            port=port,
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
