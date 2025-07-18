#!/usr/bin/env python3
"""
Development utility script for the racing game.
Provides commands for running, building, and managing the project.
"""

import subprocess
import sys
from pathlib import Path


def run_local():
    """Run the local Python version."""
    print("🏎️  Starting local game...")
    try:
        subprocess.run([sys.executable, "main_desktop.py"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Local game execution failed: {e}")
        return False
    except KeyboardInterrupt:
        print("\n🛑 Game stopped by user")
    return True


def serve_web():
    """Serve the web version using Pygbag's built-in server."""
    print("🌐 Starting Pygbag web server...")
    print("💡 This resolves CORS issues and provides proper CDN access")
    try:
        subprocess.run(
            [
                sys.executable,
                "-m",
                "pygbag",
                "--port",
                "8000",
                "--cdn",
                "https://pygame-web.github.io/archives/0.9/",
                "main.py",
            ],
            check=True,
        )
    except subprocess.CalledProcessError as e:
        print(f"❌ Web server failed: {e}")
        return False
    except KeyboardInterrupt:
        print("\n🛑 Web server stopped by user")
    return True


def build_web():
    """Build the web version using Pygbag."""
    print("🏗️  Building web version...")
    try:
        subprocess.run(
            [
                sys.executable,
                "-m",
                "pygbag",
                "--archive",
                "--cdn",
                "https://pygame-web.github.io/archives/0.9/",
                "main.py",
            ],
            check=True,
        )

        print("\n🎮 Build Summary:")
        print("✅ Web version successfully built!")
        print("📁 Output: build/web/ directory")
        print("🌐 To test: python dev.py serve")

        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Web build failed: {e}")
        return False


def install_dependencies():
    """Install all required dependencies."""
    print("📦 Installing dependencies...")

    try:
        print("Installing pygame...")
        subprocess.run(
            [sys.executable, "-m", "pip", "install", "pygame>=2.5.0"], check=True
        )

        print("Installing pygbag...")
        subprocess.run(
            [sys.executable, "-m", "pip", "install", "pygbag>=0.8.0"], check=True
        )

        print("✅ Dependencies installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False


def clean_project():
    """Clean up unused files and build artifacts."""
    print("🧹 Cleaning up project...")

    removed_files = []

    # Clean build directories
    import shutil

    for build_dir in ["build", "dist"]:
        build_path = Path(build_dir)
        if build_path.exists():
            shutil.rmtree(build_path)
            removed_files.append(f"{build_dir}/")

    if removed_files:
        print(f"✅ Removed {len(removed_files)} unused files:")
        for file in removed_files:
            print(f"   • {file}")
    else:
        print("✅ Project already clean!")

    return True


def show_help():
    """Show help information."""
    print("🎮 Racing Game Development Tool")
    print("=" * 40)
    print("Available commands:")
    print("")
    print("🏎️  Game Execution:")
    print("  run        - Run local Python version")
    print("  serve      - Build and serve web version")
    print("")
    print("🔧 Build & Deploy:")
    print("  build      - Build web version for deployment")
    print("  install    - Install all dependencies")
    print("  clean      - Clean up unused files")
    print("")
    print("💡 Quick Start:")
    print("  python dev.py install   # Install dependencies")
    print("  python dev.py run       # Test locally")
    print("  python dev.py serve     # Test web version")
    print("")
    print("📁 Project Structure:")
    print("  main_desktop.py - Desktop version (full features)")
    print("  main.py         - Web version (browser compatible)")
    print("  dev.py          - This development tool")


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
    elif command == "serve":
        serve_web()
    elif command == "build":
        build_web()
    elif command == "install":
        install_dependencies()
    elif command == "clean":
        clean_project()
    elif command == "help":
        show_help()
    else:
        print(f"❌ Unknown command: {command}")
        print("💡 Use 'python dev.py help' for available commands")
        sys.exit(1)


if __name__ == "__main__":
    main()
