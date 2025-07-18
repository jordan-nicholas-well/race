# 🎮 Racing Game - Desktop and Web Versions

This project now supports both desktop and web deployment!

## 🖥️ Desktop Version

To run the desktop version locally:

```bash
# Run with the desktop-specific entry point
python main_desktop.py

# Or use the VS Code task
# In VS Code: Ctrl+Shift+P -> "Tasks: Run Task" -> "Run Racing Game"
```

### Desktop Features
- Full pygame functionality
- Settings interface with TAB key
- Real-time performance monitoring
- Two-player racing (WASD + Arrow Keys)

## 🌐 Web Version

To run the web version:

```bash
# Option 1: Use the build script (recommended)
python build_web.py serve

# Option 2: Use Pygbag directly
.venv/bin/python -m pygbag --port 8001 --cdn https://pygame-web.github.io/archives/0.9/ main_web.py
```

### Web Features
- Runs in any modern web browser
- WebAssembly-powered pygame-ce
- Touch and keyboard controls
- Automatic async event loop management

## 📂 File Structure

```
main_desktop.py  - Desktop version (full features)
main_web.py      - Web version (browser compatible)
main.py          - Web-compatible async version (Pygbag entry point)
build_web.py     - Web build and serve utility
```

## 🚀 GitHub Pages Deployment

To deploy to GitHub Pages:

1. **Build for production:**
   ```bash
   python build_web.py archive
   ```

2. **Copy build artifacts:**
   The web files will be in `build/web/` - copy these to your GitHub Pages repository

3. **Enable GitHub Pages:**
   - Go to your repository settings
   - Enable GitHub Pages from the `main` branch
   - Your game will be available at `https://[username].github.io/[repository]/`

## 🛠️ Development Notes

### Entry Points
- **Desktop**: `main_desktop.py` - Traditional pygame with synchronous game loop
- **Web**: `main_web.py` - Async-compatible version for Pygbag/WebAssembly
- **Pygbag**: `main.py` - Auto-generated async wrapper for web deployment

### Dependencies
- **Desktop**: Pure pygame
- **Web**: pygame-ce (Community Edition) for better web compatibility
- **Build Tool**: Pygbag 0.9.2 for WebAssembly compilation

### Controls
- **Player 1**: WASD keys
- **Player 2**: Arrow keys
- **Settings**: TAB key (desktop only)
- **Quit**: ESC key

## 🔧 Troubleshooting

### Web Version Issues
1. **Port conflicts**: Try different ports with `--port 8002`
2. **CORS errors**: Always use Pygbag's built-in server
3. **Asset loading**: Ensure all PNG files are in the project root

### Performance Tips
- Web version runs at 30 FPS for stability
- Desktop version runs at 60 FPS for smoothness
- Use Chrome/Firefox for best web performance

## 📋 Quick Commands

```bash
# Desktop
python main_desktop.py

# Web development
python build_web.py serve

# Web production build
python build_web.py archive

# Clean build artifacts
python build_web.py clean
```

Your racing game is now ready for both local play and web deployment! 🏁
