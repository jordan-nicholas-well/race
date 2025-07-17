#!/usr/bin/env python3
"""
Development utility script for the racing game.
Provides commands for running, building, and managing the project.
"""

import subprocess
import sys
import platform
from pathlib import Path

def run_local():
    """Run the local Python version."""
    print("🏎️  Starting local game...")
    try:
        subprocess.run([sys.executable, "main.py"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Local game execution failed: {e}")
        return False
    except KeyboardInterrupt:
        print("\n🛑 Game stopped by user")
    return True

def run_web_dev():
    """Run the web development version."""
    print("🌐 Starting web development mode...")
    print("💡 This will use pygame locally for development")
    try:
        subprocess.run([sys.executable, "main_universal.py", "--web"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Web development execution failed: {e}")
        return False
    except KeyboardInterrupt:
        print("\n🛑 Web game stopped by user")
    return True

def build_web():
    """Build the web version using Pygbag."""
    print("🏗️  Building web version...")
    try:
        result = subprocess.run([sys.executable, "build_web.py", "archive"], check=True)
        
        print("\n🎮 Build Summary:")
        print("✅ Web version successfully built!")
        print("📁 Output locations:")
        print("   • build/web/ - Web deployment files")
        print("   • build/web.zip - Complete deployment archive")
        print("   • dist/ - Copied files for convenience")
        print("")
        print("🌐 To test the working solution:")
        print("   python build_web.py serve")
        print("   # This uses Pygbag's server and resolves CORS issues!")
        
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Web build failed: {e}")
        return False

def serve_web():
    """Serve the web version using Pygbag's built-in server."""
    print("🌐 Starting Pygbag web server...")
    print("💡 This resolves CORS issues and provides proper CDN access")
    try:
        subprocess.run([sys.executable, "build_web.py", "serve"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Web server failed: {e}")
        return False
    except KeyboardInterrupt:
        print("\n🛑 Web server stopped by user")
    return True

def install_dependencies():
    """Install all required dependencies."""
    print("📦 Installing dependencies...")
    
    try:
        # Install core dependencies
        print("Installing core dependencies...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pygame>=2.5.0"], check=True)
        
        # Install web dependencies
        print("Installing web dependencies...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pygbag>=0.8.0"], check=True)
        
        print("✅ Dependencies installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False

def show_help():
    """Show help information."""
    print("🎮 Racing Game Development Tool")
    print("=" * 40)
    print("Available commands:")
    print("")
    print("🏎️  Game Execution:")
    print("  run        - Run local Python version")
    print("  web-dev    - Run web development mode (local pygame)")
    print("  serve      - Build and serve web version (RECOMMENDED)")
    print("")
    print("🔧 Build & Deploy:")
    print("  build      - Build web version for deployment")
    print("  install    - Install all dependencies")
    print("")
    print("💡 Quick Start:")
    print("  python dev.py install   # Install dependencies")
    print("  python dev.py run       # Test locally")
    print("  python dev.py serve     # Test web version (WORKING!)")
    print("")
    print("🌐 Web Testing (SOLUTION):")
    print("  The 'serve' command uses Pygbag's built-in server")
    print("  which resolves CORS issues and handles CDN dependencies properly!")

def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        show_help()
        return
    
    command = sys.argv[1]
    
    print(f"🔧 Executing: {command}")
    print("-" * 30)
    
    if command == "run":
        run_local()
    elif command == "web-dev":
        run_web_dev()
    elif command == "serve":
        serve_web()
    elif command == "build":
        build_web()
    elif command == "install":
        install_dependencies()
    elif command == "help":
        show_help()
    else:
        print(f"❌ Unknown command: {command}")
        print("💡 Use 'python dev.py help' for available commands")
        sys.exit(1)

if __name__ == "__main__":
    main()
