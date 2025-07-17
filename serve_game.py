#!/usr/bin/env python3
"""
Local test server for the racing game web build.
This serves the game with proper MIME types and CORS headers.
"""

import http.server
import socketserver
import webbrowser
import sys
from pathlib import Path

class GameHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        # Add comprehensive CORS headers for Pygbag web games
        self.send_header('Cross-Origin-Embedder-Policy', 'credentialless')
        self.send_header('Cross-Origin-Opener-Policy', 'same-origin')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', '*')
        self.send_header('Cross-Origin-Resource-Policy', 'cross-origin')
        super().end_headers()

    def do_OPTIONS(self):
        """Handle preflight OPTIONS requests."""
        self.send_response(200)
        self.end_headers()

    def guess_type(self, path):
        # Convert path to string if needed
        path_str = str(path)
        
        # Fix WASM MIME type
        if path_str.endswith('.wasm'):
            return 'application/wasm'
        if path_str.endswith('.apk'):
            return 'application/octet-stream'
            
        return super().guess_type(path)

def main():
    port = 8000
    
    # Change to the directory containing this script
    script_dir = Path(__file__).parent
    web_dir = script_dir / "dist"
    
    if not web_dir.exists():
        print("❌ dist/ directory not found. Run 'python dev.py build' first.")
        sys.exit(1)
    
    print(f"🌐 Starting local game server on port {port}...")
    print(f"📁 Serving files from: {web_dir}")
    
    # Change to the web directory
    import os
    os.chdir(web_dir)
    
    print("🔧 CORS headers enabled for CDN resource loading")
    print("🌐 Allowing cross-origin requests for Pygbag dependencies")
    
    with socketserver.TCPServer(("", port), GameHTTPRequestHandler) as httpd:
        url = f"http://localhost:{port}"
        print(f"🎮 Game available at: {url}")
        print("📋 Press Ctrl+C to stop the server")
        
        # Try to open the browser automatically
        try:
            webbrowser.open(url)
            print("🌐 Opened browser automatically")
        except:
            print("💡 Please open the URL manually in your browser")
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n🛑 Server stopped")

if __name__ == "__main__":
    main()
