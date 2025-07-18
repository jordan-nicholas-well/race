#!/usr/bin/env python3
"""
Quick test script to verify web game components work correctly.
"""

import sys
import os

def test_web_files():
    """Test that all required web files exist and have basic content."""
    required_files = [
        'index.html',
        'web_game.js', 
        'web_main.py'
    ]
    
    print("🧪 Testing Web Game Files...")
    
    for file in required_files:
        if not os.path.exists(file):
            print(f"❌ Missing file: {file}")
            return False
        else:
            print(f"✅ Found: {file}")
    
    # Test HTML file contains required elements
    with open('index.html', 'r') as f:
        html_content = f.read()
        required_elements = [
            'canvas id="gameCanvas"',
            'pyodide.js',
            'web_game.js',
            'WebRacingGame'
        ]
        
        for element in required_elements:
            if element in html_content:
                print(f"✅ HTML contains: {element}")
            else:
                print(f"❌ HTML missing: {element}")
                return False
    
    # Test JavaScript file contains required functions
    with open('web_game.js', 'r') as f:
        js_content = f.read()
        required_functions = [
            'initializePyodide',
            'loadGameFiles', 
            'setupWebEnvironment',
            'WebRacingGame'
        ]
        
        for func in required_functions:
            if func in js_content:
                print(f"✅ JS contains: {func}")
            else:
                print(f"❌ JS missing: {func}")
                return False
    
    # Test Python web file contains required classes
    with open('web_main.py', 'r') as f:
        py_content = f.read()
        required_items = [
            'class WebRacingGame',
            'async def run',
            'pygame.init',
            'asyncio.sleep'
        ]
        
        for item in required_items:
            if item in py_content:
                print(f"✅ Python contains: {item}")
            else:
                print(f"❌ Python missing: {item}")
                return False
    
    return True

def test_game_assets():
    """Test that game assets exist."""
    print("\n🎮 Testing Game Assets...")
    
    required_assets = [
        'car_sports.png',
        'car_truck.png', 
        'track1_visual.png',
        'track1_mask.png'
    ]
    
    for asset in required_assets:
        if os.path.exists(asset):
            print(f"✅ Asset found: {asset}")
        else:
            print(f"⚠️  Asset missing: {asset} (will use fallback)")
    
    return True

def test_python_modules():
    """Test that Python game modules can be imported."""
    print("\n🐍 Testing Python Modules...")
    
    modules = [
        'settings',
        'car',
        'track',
        'controls',
        'game_settings'
    ]
    
    for module in modules:
        try:
            __import__(module)
            print(f"✅ Module imports: {module}")
        except ImportError as e:
            print(f"❌ Module import failed: {module} - {e}")
            return False
    
    return True

def main():
    """Run all tests."""
    print("🚀 Web Racing Game Test Suite")
    print("=" * 40)
    
    all_passed = True
    
    # Test web files
    if not test_web_files():
        all_passed = False
    
    # Test game assets
    if not test_game_assets():
        all_passed = False
    
    # Test Python modules
    if not test_python_modules():
        all_passed = False
    
    print("\n" + "=" * 40)
    if all_passed:
        print("🎉 All tests passed! Web game is ready for deployment.")
        print("\nNext steps:")
        print("1. Test locally: python3 -m http.server 8080")
        print("2. Visit: http://localhost:8080")
        print("3. Deploy to GitHub Pages (see WEB_DEPLOYMENT.md)")
    else:
        print("❌ Some tests failed. Please fix the issues above.")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
