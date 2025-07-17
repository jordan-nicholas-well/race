#!/usr/bin/env python3
"""
Development script for testing both local and web versions of the racing game.

This script provides convenient commands for development, testing, and building.
"""

import subprocess
import sys
import os
import argparse
from pathlib import Path

def run_local():
    """Run the game in local mode."""
    print("🖥️  Running local version...")
    try:
        subprocess.run([sys.executable, "main_universal.py"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Local execution failed: {e}")
        return False
    except KeyboardInterrupt:
        print("\n🛑 Local game stopped by user")
    return True

def run_web_dev():
    """Run the game in web development mode (simulated web environment)."""
    print("🌐 Running web version in development mode...")
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
        subprocess.run([sys.executable, "build_web.py"], check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Web build failed: {e}")
        return False

def install_dependencies():
    """Install all required dependencies."""
    print("📦 Installing dependencies...")
    
    # Core dependencies
    deps = ["pygame>=2.5.0"]
    
    # Web dependencies (optional)
    web_deps = ["pygbag>=0.8.0"]
    
    try:
        # Install core dependencies
        print("Installing core dependencies...")
        subprocess.run([
            sys.executable, "-m", "pip", "install"
        ] + deps, check=True)
        
        # Install web dependencies
        print("Installing web dependencies...")
        subprocess.run([
            sys.executable, "-m", "pip", "install"
        ] + web_deps, check=True)
        
        print("✅ All dependencies installed successfully")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Dependency installation failed: {e}")
        return False

def lint_code():
    """Run code linting on the project."""
    print("🔍 Running code linting...")
    
    python_files = [
        "main.py",
        "main_web.py", 
        "main_universal.py",
        "car.py",
        "track.py",
        "settings.py",
        "game_settings.py",
        "settings_interface.py",
        "web_settings_interface.py",
        "build_web.py"
    ]
    
    # Filter to only existing files
    existing_files = [f for f in python_files if os.path.exists(f)]
    
    try:
        # Try to use pylint if available
        subprocess.run([
            sys.executable, "-m", "pylint", "--disable=C0103,R0903,R0902"
        ] + existing_files, check=False)  # Don't fail on warnings
        
        print("✅ Code linting completed")
        return True
        
    except FileNotFoundError:
        print("ℹ️  Pylint not available, skipping linting")
        return True

def test_imports():
    """Test that all imports work correctly."""
    print("🧪 Testing imports...")
    
    tests = [
        ("main.py", "from main import RacingGame"),
        ("main_web.py", "from main_web import RacingGameWeb"),
        ("car.py", "from car import Car"),
        ("track.py", "from track import Track"),
        ("settings_interface.py", "from settings_interface import settings_interface"),
        ("web_settings_interface.py", "from web_settings_interface import WebSettingsInterface"),
    ]
    
    all_passed = True
    
    for file_name, import_stmt in tests:
        if os.path.exists(file_name):
            try:
                exec(import_stmt)
                print(f"✅ {file_name}: Import successful")
            except Exception as e:
                print(f"❌ {file_name}: Import failed - {e}")
                all_passed = False
        else:
            print(f"⚠️  {file_name}: File not found")
    
    if all_passed:
        print("✅ All import tests passed")
    else:
        print("❌ Some import tests failed")
    
    return all_passed

def show_project_info():
    """Show information about the project structure."""
    print("📋 Project Information")
    print("=" * 50)
    
    # Check file existence
    core_files = {
        "main.py": "Local game entry point",
        "main_web.py": "Web game entry point", 
        "main_universal.py": "Universal launcher",
        "car.py": "Car physics and rendering",
        "track.py": "Track loading and collision",
        "settings.py": "Game configuration",
        "game_settings.py": "Runtime game settings",
        "settings_interface.py": "Terminal settings interface",
        "web_settings_interface.py": "GUI settings interface",
        "build_web.py": "Web build script",
        "pyproject.toml": "Project configuration",
        "requirements.txt": "Python dependencies"
    }
    
    print("📁 Core Files:")
    for filename, description in core_files.items():
        status = "✅" if os.path.exists(filename) else "❌"
        print(f"   {status} {filename:<25} - {description}")
    
    print("\n🎮 Available Commands:")
    print("   python dev.py local         - Run local version")
    print("   python dev.py web-dev       - Run web version (dev mode)")
    print("   python dev.py build         - Build web version")
    print("   python dev.py install       - Install dependencies")
    print("   python dev.py test          - Test imports")
    print("   python dev.py lint          - Run code linting")
    print("   python dev.py info          - Show this information")

def main():
    """Main development script entry point."""
    parser = argparse.ArgumentParser(
        description="Development script for the racing game",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python dev.py local      # Run local version
  python dev.py web-dev    # Test web version
  python dev.py build      # Build for web deployment
  python dev.py install    # Install all dependencies
        """
    )
    
    parser.add_argument(
        "command",
        choices=["local", "web-dev", "build", "install", "test", "lint", "info"],
        help="Command to execute"
    )
    
    if len(sys.argv) == 1:
        show_project_info()
        return
    
    args = parser.parse_args()
    
    print(f"🚀 Executing: {args.command}")
    print("-" * 30)
    
    success = True
    
    if args.command == "local":
        success = run_local()
    elif args.command == "web-dev":
        success = run_web_dev()
    elif args.command == "build":
        success = build_web()
    elif args.command == "install":
        success = install_dependencies()
    elif args.command == "test":
        success = test_imports()
    elif args.command == "lint":
        success = lint_code()
    elif args.command == "info":
        show_project_info()
    
    if not success:
        sys.exit(1)

if __name__ == "__main__":
    main()
