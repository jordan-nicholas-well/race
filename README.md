# 2D Racing Game

A modular, multiplayer top-down racing game built with Python and Pygame.

## Features

- **Two-player local multiplayer** with different control schemes
- **Modular code structure** with clear separation of concerns
- **High-resolution track system** using visual and mask images
- **Realistic car physics** with customizable parameters
- **Runtime physics adjustments** for fine-tuning gameplay
- **Multiple car types** with different handling characteristics
- **Collision detection** with walls and slow-down areas

## Installation

1. Clone or download this repository
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Creating Track Assets

Before running the game, you need to create two track image files. The game will use fallback graphics if these files are not found, but custom tracks provide a much better experience.

### Required Files

Create these two PNG files in the game directory:

1. **`track1_visual.png`** - The visual track image (1280x720 pixels)
2. **`track1_mask.png`** - The collision mask image (1280x720 pixels)

### Track Creation Instructions

#### Using GIMP, Photoshop, or any image editor:

**For `track1_visual.png`:**
1. Create a new image: 1280x720 pixels
2. Design your race track with any colors and details you want
3. Make it visually appealing - this is what players will see
4. Include track surfaces, grass, walls, barriers, etc.
5. Save as `track1_visual.png`

**For `track1_mask.png`:**
1. Create a new image: 1280x720 pixels with WHITE background
2. Use EXACT colors for different areas:
   - **Black (0, 0, 0)**: Drivable track surface
   - **White (255, 255, 255)**: Walls and barriers (cars will crash)
   - **Blue (0, 0, 255)**: Starting positions (place 2 blue dots)
   - **Green (0, 255, 0)**: Slow-down areas (grass/sand)
3. The mask must align perfectly with your visual track
4. Save as `track1_mask.png`

#### Important Notes:
- Both images must be exactly 1280x720 pixels
- Use precise RGB color values for the mask image
- Place exactly 2 blue pixels for the starting positions
- Ensure the mask aligns perfectly with the visual track

#### Example Track Layout:
```
- Outer boundary: White (walls)
- Track surface: Black (drivable)
- Inner area: White (walls) or Green (slow-down)
- Two blue dots on the track for starting positions
```

## Controls

### Player 1 (Red Sports Car)
- **W**: Accelerate
- **S**: Brake/Reverse
- **A**: Turn Left
- **D**: Turn Right

### Player 2 (Blue Truck)
- **↑**: Accelerate
- **↓**: Brake/Reverse
- **←**: Turn Left
- **→**: Turn Right

### Physics Adjustments (Player 1 only)
- **U**: Increase turn speed
- **J**: Decrease turn speed
- **I**: Increase acceleration
- **K**: Decrease acceleration

## Running the Game

### From VS Code (Recommended)

This project is fully configured for VS Code development:

1. **Open the project in VS Code**
2. **Install recommended extensions** (VS Code will prompt you)
3. **Run the game using any of these methods:**

#### Method 1: VS Code Tasks (Easiest)
- Press `Ctrl+Shift+P` (or `Cmd+Shift+P` on Mac)
- Type "Tasks: Run Task"
- Select "🎮 Run Racing Game"

#### Method 2: VS Code Run/Debug
- Press `F5` to run with debugging
- Or select "🎮 Debug Racing Game" from the Run and Debug panel

#### Method 3: Command Palette
- Press `Ctrl+Shift+P`
- Type "Python: Run Python File in Terminal"

#### Available VS Code Tasks:
- **🎮 Run Racing Game** - Start the main game
- **🧪 Test Game Components** - Run component tests
- **🛣️ Create Sample Track** - Generate track images
- **📦 Install Dependencies** - Install Python packages
- **🐍 Setup Python Environment** - Create virtual environment

### From Command Line

```bash
# Quick launch (sets up everything automatically)
./play.sh

# Or manually:
python main.py
```

### From Terminal

## Game Mechanics

### Car Physics
- **Acceleration**: How quickly cars gain speed
- **Max Speed**: Top speed limit for each car
- **Friction**: How quickly cars slow down when not accelerating
- **Turn Speed**: How sharply cars can turn

### Track Surfaces
- **Black areas**: Normal drivable track
- **White areas**: Walls (cars crash and reset to start)
- **Green areas**: Slow-down zones (reduced max speed)
- **Blue dots**: Starting positions

### Car Types
- **Sports Car (Player 1)**: Fast acceleration, high top speed, good turning
- **Truck (Player 2)**: Slower acceleration, lower top speed, slower turning

## Code Structure

- **`main.py`**: Game initialization and main loop
- **`settings.py`**: All configuration constants and car presets
- **`car.py`**: Car class with physics and rendering
- **`track.py`**: Track loading and collision detection
- **`controls.py`**: Input control schemes
- **`requirements.txt`**: Python dependencies

## Customization

### Adding New Car Types
Edit `settings.py` and add new car dictionaries with these parameters:
- `acceleration`: How fast the car speeds up
- `max_speed`: Maximum speed
- `friction`: How quickly it slows down (0.9-0.99)
- `turn_speed`: How sharp it turns
- `color`: RGB color tuple
- `size`: (width, height) in pixels

### Modifying Physics
All physics parameters can be adjusted in `settings.py` or at runtime using the keyboard controls.

## Troubleshooting

### No Track Images
If you don't create the PNG files, the game will automatically generate a simple oval track with proper collision detection.

### Performance Issues
- Reduce `FPS` in `settings.py`
- Use smaller track images
- Reduce the number of collision checks

### Car Handling
Use the runtime physics adjustment keys (U, J, I, K) to fine-tune how Player 1's car handles.

## License

This project is open source and available under the MIT License.
