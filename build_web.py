#!/usr/bin/env python3
"""
Build script for deploying the racing game to web using Pygbag.

This script handles the complete build process including:
- Installing web dependencies
- Building the WebAssembly package
- Creating the web distribution
"""

import subprocess
import sys
import os
import shutil
from pathlib import Path

def install_web_dependencies():
    """Install dependencies required for web deployment."""
    print("🔧 Installing web dependencies...")
    try:
        subprocess.run([
            sys.executable, "-m", "pip", "install", "pygbag>=0.8.0"
        ], check=True)
        print("✅ Web dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install web dependencies: {e}")
        return False

def clean_build_artifacts():
    """Clean any existing build artifacts."""
    print("🧹 Cleaning build artifacts...")
    
    artifacts_to_clean = [
        "dist",
        "build", 
        "__pycache__",
        "*.pyc",
        ".pygame_web"
    ]
    
    for artifact in artifacts_to_clean:
        if os.path.exists(artifact):
            if os.path.isdir(artifact):
                shutil.rmtree(artifact)
                print(f"   Removed directory: {artifact}")
            else:
                os.remove(artifact)
                print(f"   Removed file: {artifact}")
    
    print("✅ Build artifacts cleaned")

def build_web_version():
    """Build the web version using Pygbag."""
    print("🏗️  Building web version...")
    
    # Ensure we're in the project directory
    project_dir = Path(__file__).parent
    os.chdir(project_dir)
    
    try:
        # Build command for Pygbag
        build_cmd = [
            sys.executable, "-m", "pygbag",
            "--width", "1024",
            "--height", "768", 
            "--name", "Racing Game",
            "--archive",
            "--optimize",
            "--cdn", "https://cdn.jsdelivr.net/pyodide/",
            "main_web.py"
        ]
        
        print(f"Running: {' '.join(build_cmd)}")
        subprocess.run(build_cmd, check=True)
        
        print("✅ Web version built successfully!")
        print("📁 Output files are in the dist/ directory")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Build failed: {e}")
        return False
    except FileNotFoundError:
        print("❌ Pygbag not found. Please install it first.")
        return False

def create_web_template():
    """Create a custom web template if needed."""
    print("🎨 Creating web template...")
    
    template_dir = Path("web_template")
    template_dir.mkdir(exist_ok=True)
    
    # Create a basic HTML template
    html_content = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Racing Game</title>
    <style>
        body {
            margin: 0;
            padding: 20px;
            background-color: #1a1a1a;
            color: white;
            font-family: Arial, sans-serif;
            text-align: center;
        }
        
        .game-container {
            max-width: 1024px;
            margin: 0 auto;
        }
        
        .controls-info {
            margin-bottom: 20px;
            padding: 15px;
            background-color: #2a2a2a;
            border-radius: 8px;
        }
        
        .controls-info h3 {
            margin-top: 0;
            color: #4CAF50;
        }
        
        .control-row {
            display: flex;
            justify-content: space-around;
            margin: 10px 0;
        }
        
        .player-controls {
            background-color: #3a3a3a;
            padding: 10px;
            border-radius: 5px;
            flex: 1;
            margin: 0 10px;
        }
        
        .loading-text {
            font-size: 18px;
            margin-top: 20px;
        }
        
        canvas {
            border: 2px solid #444;
            border-radius: 8px;
        }
    </style>
</head>
<body>
    <div class="game-container">
        <h1>🏎️ Racing Game</h1>
        
        <div class="controls-info">
            <h3>Game Controls</h3>
            <div class="control-row">
                <div class="player-controls">
                    <h4>Player 1 (Sports Car)</h4>
                    <p>WASD Keys</p>
                    <p>W/S: Accelerate/Brake</p>
                    <p>A/D: Turn Left/Right</p>
                </div>
                <div class="player-controls">
                    <h4>Player 2 (Truck)</h4>
                    <p>Arrow Keys</p>
                    <p>↑/↓: Accelerate/Brake</p>
                    <p>←/→: Turn Left/Right</p>
                </div>
            </div>
            <p><strong>TAB:</strong> Toggle Settings Menu | <strong>ESC:</strong> Quit Game</p>
        </div>
        
        <div id="pygame-container">
            <!-- Pygame canvas will be inserted here -->
        </div>
        
        <div class="loading-text">
            <p>🌐 Loading game... Please wait</p>
            <p><em>The game will start automatically once loaded</em></p>
        </div>
    </div>
</body>
</html>'''
    
    with open(template_dir / "index.html", "w") as f:
        f.write(html_content)
    
    print("✅ Web template created")

def main():
    """Main build process."""
    print("🚀 Starting web build process...")
    print("=" * 50)
    
    # Step 1: Install dependencies
    if not install_web_dependencies():
        sys.exit(1)
    
    # Step 2: Clean build artifacts
    clean_build_artifacts()
    
    # Step 3: Create web template
    create_web_template()
    
    # Step 4: Build web version
    if not build_web_version():
        sys.exit(1)
    
    print("=" * 50)
    print("🎉 Build completed successfully!")
    print("📋 Next steps:")
    print("   1. Test locally: Open dist/index.html in a web browser")
    print("   2. Deploy: Upload the dist/ folder to your web server")
    print("   3. Share: Send the URL to your deployed game!")

if __name__ == "__main__":
    main()
