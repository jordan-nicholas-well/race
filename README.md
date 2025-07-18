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

### Automatic GitHub Pages Deployment

This repository includes a GitHub Actions workflow that automatically builds and deploys to GitHub Pages:

1. **Enable GitHub Pages**:

   - Go to your repository Settings → Pages
   - Set Source to "GitHub Actions"
   - The game will auto-deploy on every push to main/master

2. **Manual deployment**: `python dev.py build` then copy `build/web/` contents to your web host

3. **Other platforms**: Deploy to itch.io, Netlify, or any static hosting

### 🔗 Access Your Game

After deployment, your game will be available at:
`https://[username].github.io/[repository-name]/`

## 🔧 Development

- **Local testing**: `python dev.py run`
- **Web testing**: `python dev.py serve`
- **Clean project**: `python dev.py clean`
- **Help**: `python dev.py help`

### 🚀 Continuous Deployment

- **GitHub Actions**: Automatically builds and deploys on push to main/master
- **Workflow file**: `.github/workflows/deploy.yml`
- **Requirements**: Enable GitHub Pages with "GitHub Actions" source

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
