#!/usr/bin/env python3
"""
Universal main entry point for the racing game.

This file automatically detects the execution environment and runs the
appropriate version:
- Local execution: Uses terminal-based settings interface
- Web execution: Uses GUI-based settings interface via Pygbag

Usage:
    python main_universal.py        # Local mode
    pygbag main_universal.py        # Web mode
"""

import sys
import os
import asyncio
from pathlib import Path

def detect_execution_environment():
    """
    Detect whether we're running locally or in a web browser.
    
    Returns:
        str: 'web' if running in browser via Pygbag, 'local' otherwise
    """
    # Check for Pygbag/Emscripten environment
    if (hasattr(sys, 'platform') and 'emscripten' in sys.platform.lower()) or \
       (hasattr(os, 'name') and os.name == 'emscripten'):
        return 'web'
    
    # Check for Pygbag module presence and web-specific features
    try:
        import platform
        if platform.system() == "Emscripten":
            return 'web'
    except:
        pass
    
    # Check command line arguments for web build
    if '--web' in sys.argv:
        return 'web'
    
    # Default to local
    return 'local'

async def run_local_game():
    """Run the local version with terminal settings interface."""
    print("🖥️  Starting local game mode...")
    print("Features: Terminal-based settings interface")
    
    # Import and run local version
    try:
        from main import RacingGame
        game = RacingGame()
        
        # Local version runs synchronously but we wrap it for consistency
        game.run()
        
    except ImportError as e:
        print(f"❌ Failed to import local game: {e}")
        print("Make sure main.py exists and all dependencies are installed")
        sys.exit(1)

async def run_web_game():
    """Run the web version with GUI settings interface."""
    print("🌐 Starting web game mode...")
    print("Features: GUI-based settings interface, browser compatible")
    
    # Import and run web version
    try:
        from main_web import RacingGameWeb
        game = RacingGameWeb()
        
        # Web version runs asynchronously
        await game.run()
        
    except ImportError as e:
        print(f"❌ Failed to import web game: {e}")
        print("Make sure main_web.py exists and all dependencies are installed")
        sys.exit(1)

def print_environment_info(env_type):
    """Print information about the detected environment."""
    print("🏎️  Racing Game - Universal Launcher")
    print("=" * 50)
    print(f"Environment: {env_type.upper()}")
    
    if env_type == 'local':
        print("🎮 Local Execution Mode")
        print("• Full terminal-based settings interface")
        print("• High performance native execution")
        print("• Complete feature set")
        print("• Controls: WASD (P1), Arrow Keys (P2)")
        print("• Settings: Available in terminal console")
        
    else:  # web
        print("🌐 Web Browser Mode")
        print("• GUI-based settings interface")
        print("• Cross-platform browser compatibility")
        print("• WebAssembly-powered execution")
        print("• Controls: WASD (P1), Arrow Keys (P2)")
        print("• Settings: Press TAB for in-game menu")
    
    print("=" * 50)

async def main():
    """Main entry point that routes to appropriate game version."""
    # Detect environment
    env_type = detect_execution_environment()
    
    # Print environment information
    print_environment_info(env_type)
    
    try:
        if env_type == 'web':
            await run_web_game()
        else:
            await run_local_game()
            
    except KeyboardInterrupt:
        print("\n🛑 Game interrupted by user")
    except Exception as e:
        print(f"❌ Game error: {e}")
        if env_type == 'local':
            import traceback
            traceback.print_exc()
        sys.exit(1)
    
    print("\n👋 Thanks for playing!")

def run_main():
    """Run the main function with proper event loop handling."""
    env_type = detect_execution_environment()
    
    try:
        # Check if we're already in an event loop
        loop = asyncio.get_event_loop()
        if loop.is_running():
            # We're in a running event loop (common in web environments)
            print("🔄 Event loop already running, scheduling coroutine...")
            # Create a task and let it run
            task = asyncio.create_task(main())
            return task
        else:
            # No running loop, safe to use asyncio.run
            asyncio.run(main())
    except RuntimeError as e:
        if "cannot be called from a running event loop" in str(e):
            # We're definitely in a running loop, use ensure_future
            print("🔄 Detected running event loop, using ensure_future...")
            asyncio.ensure_future(main())
        else:
            # Some other runtime error, try the fallback
            try:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                loop.run_until_complete(main())
            except Exception as fallback_error:
                print(f"❌ Failed to run game: {fallback_error}")
                sys.exit(1)

if __name__ == "__main__":
    run_main()
