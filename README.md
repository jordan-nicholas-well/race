# 🎮 2D Racing Game

A dual-platform 2D racing game that runs both locally (desktop) and in web browsers.

## 🚀 Quick Start

All commands are handled through the `dev.py` development tool:

```bash
# Install dependencies
python dev.py install

# Run locally (desktop version)
python dev.py run

# Run in web browser
python dev.py serve

# Build for web deployment
python dev.py build
```

## 📁 Project Structure

**Core Files:**

- `main_desktop.py` - Desktop version with full features
- `main.py` - Web-compatible version for browsers
- `dev.py` - Development tool (replaces all other scripts)

**Game Components:**

- `car.py` - Car physics and controls
- `track.py` - Track loading and collision detection
- `settings.py` - Game configuration
- `controls.py` - Input handling
- `game_settings.py` - Runtime settings management

**Assets:**

- `car_*.png` - Car sprite images
- `track1_visual.png` - Track background
- `track1_mask.png` - Collision detection mask

## 🎮 Game Controls

- **Player 1**: WASD keys (S for reverse)
- **Player 2**: Arrow keys (↓ for reverse)
- **Settings**: TAB key (desktop version only)
- **Quit**: ESC key

## 🌐 Web Deployment

1. Build the web version: `python dev.py build`
2. Copy `build/web/` contents to your web host
3. Deploy to GitHub Pages, itch.io, or any static hosting

## 🔧 Development

- **Local testing**: `python dev.py run`
- **Web testing**: `python dev.py serve`
- **Clean project**: `python dev.py clean`
- **Help**: `python dev.py help`

The web version uses Pygbag to compile Python/pygame to WebAssembly for browser compatibility.

## 🎨 Creating Custom Content

Generate new tracks and car sprites:

```bash
# Create track images
python create_track.py

# Create car sprites
python create_sprites.py
```

## 📋 Game Features

- **Two-player racing** with different car types
- **Realistic physics** with momentum and friction
- **Track collision detection** using bitmap masks
- **Visual feedback** for speed and reverse status
- **Cross-platform compatibility** (desktop + web)
