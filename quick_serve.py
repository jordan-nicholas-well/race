#!/usr/bin/env python3
"""
Quick web game launcher - bypasses port conflicts by using Pygbag directly.
"""

import subprocess
import sys
import socket
from pathlib import Path

def find_free_port(start_port=8080, max_attempts=10):
    """Find a free port starting from start_port."""
    for port in range(start_port, start_port + max_attempts):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(('localhost', port))
                return port
        except OSError:
            continue
    return None

def main():
    """Quick launcher for the web game."""
    print("🚀 Quick Web Game Launcher")
    print("=" * 30)
    
    # Find a free port
    port = find_free_port()
    if not port:
        print("❌ No free ports available (8080-8090)")
        sys.exit(1)
    
    print(f"🌐 Using port {port}")
    print("🎮 Starting game...")
    print("📋 Press Ctrl+C to stop")
    print()
    
    try:
        # Launch Pygbag directly
        cmd = [
            sys.executable, "-m", "pygbag",
            "--port", str(port),
            "--cdn", "https://pygame-web.github.io/archives/0.9/",
            "main_web.py"
        ]
        
        subprocess.run(cmd)
        
    except KeyboardInterrupt:
        print("\n🛑 Game stopped")
    except FileNotFoundError:
        print("❌ Pygbag not installed. Run: pip install pygbag")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
