# CLI Settings Interface

The racing game now includes a powerful CLI (Command Line Interface) settings interface that allows you to adjust game settings in real-time while playing.

## How to Use

1. **Start the Game**: Run `python main.py` or use the VS Code task "Run Racing Game"
2. **Two Windows Open**:
   - **Pygame Window**: The visual game where you control the cars
   - **Console/Terminal**: The CLI settings interface

## CLI Navigation

### Controls
- **↑ (Up Arrow)**: Move selection up to previous setting
- **↓ (Down Arrow)**: Move selection down to next setting  
- **← (Left Arrow)**: Decrease the selected setting value
- **→ (Right Arrow)**: Increase the selected setting value
- **q**: Quit the settings interface (game continues running)

### Visual Indicators
- **→ Arrow**: Shows which setting is currently selected (highlighted in yellow)
- **Value Display**: Current value with 2 decimal precision
- **Range Display**: Shows [minimum - maximum] allowed values for each setting
- **Real-time Updates**: Changes apply immediately to the game

## Available Settings

### Player 1 Settings
- **Acceleration**: How quickly the car speeds up (0.1 - 1.0)
  - Default: 0.30
  - Increment: 0.05
- **Max Speed**: Maximum speed the car can reach (2.0 - 15.0)
  - Default: 8.00
  - Increment: 0.5
- **Turn Speed**: How quickly the car turns (1.0 - 8.0)
  - Default: 4.00
  - Increment: 0.2
- **Friction**: Surface friction/resistance (0.01 - 0.20)
  - Default: 0.05
  - Increment: 0.01
  - **Lower values** = Less friction (ice-like, cars coast longer)
  - **Higher values** = More friction (grippy surface, faster stopping)

### Player 2 Settings  
- **Acceleration**: How quickly the car speeds up (0.1 - 1.0)
  - Default: 0.20
  - Increment: 0.05
- **Max Speed**: Maximum speed the car can reach (2.0 - 15.0)
  - Default: 6.00
  - Increment: 0.5
- **Turn Speed**: How quickly the car turns (1.0 - 8.0)
  - Default: 2.50
  - Increment: 0.2
- **Friction**: Surface friction/resistance (0.01 - 0.20)
  - Default: 0.07
  - Increment: 0.01
  - **Lower values** = Less friction (ice-like, cars coast longer)
  - **Higher values** = More friction (grippy surface, faster stopping)

### Global Settings
- **Wall Stickiness**: How much cars stick to walls when colliding (0.0 - 1.0)
  - Default: 0.40
  - Increment: 0.1
  - 0.0 = No sticking (cars slide along walls)
  - 1.0 = Very sticky (cars get stuck on walls)

## Game Controls (In Pygame Window)

### Player 1
- **W**: Accelerate forward
- **S**: Reverse  
- **A**: Turn left
- **D**: Turn right

### Player 2
- **↑**: Accelerate forward
- **↓**: Reverse
- **←**: Turn left  
- **→**: Turn right

## Tips for Tuning

### Making Cars Faster
- Increase **Max Speed** for higher top speed
- Increase **Acceleration** for quicker acceleration
- **Decrease Friction** for less resistance (cars coast longer on ice-like surfaces)

### Making Cars More Responsive
- Increase **Acceleration** for faster response to input
- Increase **Turn Speed** for sharper turning
- Adjust **Wall Stickiness** lower for smoother wall interactions

### Making Cars More Stable
- **Increase Friction** for better control and faster stopping (grippy surfaces)
- Decrease **Turn Speed** for more gradual, stable turns
- Increase **Wall Stickiness** if cars slide off track too easily

### Realistic Physics Simulation
- **Low Friction** (0.01-0.05): Ice, wet surfaces - cars slide and coast
- **Medium Friction** (0.06-0.12): Normal road conditions
- **High Friction** (0.13-0.20): Racing tires on grip-enhanced surfaces

### Balancing Players
- Adjust settings for each player independently
- Player 1 (Sports Car) starts with lower friction (sportier, more slidey)
- Player 2 (Truck) starts with higher friction (more stable, grippier)
- Fine-tune **Friction** and **Turn Speed** together for different driving experiences

## Technical Details

- Settings update in real-time without restarting the game
- Console interface runs in a separate thread from the game
- All changes are temporary (reset when game restarts)
- Terminal settings are automatically restored when exiting
- **Friction Physics**: Lower values = higher velocity retention (realistic)

## Troubleshooting

### Interface Not Responding
- Make sure the terminal/console window has focus
- Try pressing arrow keys gently (not holding down)
- If stuck, press 'q' to quit settings interface

### Interface Misaligned
- The interface now uses proper carriage returns (\r)
- Should display correctly in all terminals
- If still having issues, try resizing terminal window

### Game Performance
- The CLI interface uses minimal CPU
- Game performance should not be affected
- If issues occur, press 'q' to disable settings interface

## Example Usage Session

1. Start game: `python main.py`
2. Use ↓ arrow to select "P1 Max Speed"
3. Use → arrow multiple times to increase to 12.00
4. Use ↓ arrow to select "P1 Friction"  
5. Use ← arrow to decrease to 0.02 for ice-like sliding
6. Use ↓ arrow to select "Wall Stickiness"
7. Use ← arrow to decrease to 0.10 for smoother wall sliding
8. Switch to game window and test the changes
9. Return to settings to increase **P1 Friction** to 0.08 for better control
10. Press 'q' when done adjusting settings

The settings interface now provides realistic friction physics where lower values create slippery, ice-like conditions and higher values create grippy, racing-tire conditions!
