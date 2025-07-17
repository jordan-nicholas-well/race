# 2D Racing Game

A modular, multiplayer top-down racing game built with Python and Pygame.

## Features

- **Two-player local multiplayer** with different control schemes
- **Modular code structure** with clear separation of concerns
- **High-resolution track system** using visual and mask images
- **Realistic car physics** with customizable parameters
- **Car sprites** with proper rotation and visual details
- **Reverse functionality** - cars can reverse with proper steering
- **Advanced collision detection** with intelligent wall sliding
- **Adjustable wall stickiness** - control how much cars stick to walls
- **Runtime physics adjustments** for fine-tuning gameplay
- **Multiple car types** with different handling characteristics
- **Smart collision system** - cars slow down and slide along walls instead of stopping
- **Visual indicators** - reverse lights when backing up
- **Proper starting orientation** - cars face the correct direction at start

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
- **W**: Accelerate forward
- **S**: Brake/Reverse
- **A**: Turn Left
- **D**: Turn Right

### Player 2 (Blue Truck)
- **↑**: Accelerate forward
- **↓**: Brake/Reverse
- **←**: Turn Left
- **→**: Turn Right

### Physics Adjustments (Global)
- **U**: Increase turn speed (Player 1)
- **J**: Decrease turn speed (Player 1)
- **I**: Increase acceleration (Player 1)
- **K**: Decrease acceleration (Player 1)
- **O**: Increase wall stickiness (affects both players)
- **L**: Decrease wall stickiness (affects both players)

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
- **� Create Car Sprites** - Generate car sprite images
- **�📦 Install Dependencies** - Install Python packages
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
- **Forward/Reverse**: Cars can move forward and backward with realistic acceleration
- **Speed Limiting**: Reverse speed is limited to 50% of forward speed
- **Turn Speed**: Cars turn better at higher speeds, with reversed steering when reversing
- **Friction**: Cars naturally slow down when not accelerating
- **Sprite Rotation**: Cars visually rotate to face their movement direction

### Advanced Collision System
- **Wall Detection**: Multiple collision points around each car
- **Smart Collision Response**: Cars slow down and slide along walls
- **Angle-Based Impact**: Collision severity depends on impact angle
- **Automatic Recovery**: Cars find safe positions when stuck
- **Adjustable Stickiness**: Control how much cars stick to walls (0.0 = no stick, 1.0 = very sticky)

### Track Surfaces
- **Black areas**: Normal drivable track
- **White areas**: Walls (cars slow down and slide when hit, depending on stickiness setting)
- **Green areas**: Slow-down zones (reduced max speed)
- **Blue dots**: Starting positions (cars face upward initially)

### Visual Indicators
- **Car Sprites**: Detailed car graphics with proper rotation
- **Reverse Lights**: White dots appear at the back of cars when reversing
- **Real-time Stats**: On-screen display of car status and settings

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
