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
- **Friction**: How much the car slows down naturally (0.80 - 0.99)
  - Default: 0.950
  - Increment: 0.01
  - Higher = more resistance, slower deceleration

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
- **Friction**: How much the car slows down naturally (0.80 - 0.99)
  - Default: 0.930
  - Increment: 0.01
  - Higher = more resistance, slower deceleration

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
- Decrease **Friction** for less resistance (coasts longer)

### Making Cars More Responsive
- Increase **Acceleration** for faster response to input
- Increase **Turn Speed** for sharper turning
- Adjust **Wall Stickiness** lower for smoother wall interactions

### Making Cars More Stable
- Increase **Friction** for better control and stopping
- Decrease **Turn Speed** for more gradual, stable turns
- Increase **Wall Stickiness** if cars slide off track too easily

### Balancing Players
- Adjust settings for each player independently
- Player 1 (Sports Car) starts with higher speed and better handling
- Player 2 (Truck) starts with more stability but lower performance
- Fine-tune **Friction** and **Turn Speed** for different driving experiences

## Technical Details

- Settings update in real-time without restarting the game
- Console interface runs in a separate thread from the game
- All changes are temporary (reset when game restarts)
- Terminal settings are automatically restored when exiting

## Troubleshooting

### Interface Not Responding
- Make sure the terminal/console window has focus
- Try pressing arrow keys gently (not holding down)
- If stuck, press 'q' to quit settings interface

### Game Performance
- The CLI interface uses minimal CPU
- Game performance should not be affected
- If issues occur, press 'q' to disable settings interface

## Example Usage Session

1. Start game: `python main.py`
2. Use ↓ arrow to select "P1 Max Speed"
3. Use → arrow multiple times to increase to 12.00
4. Use ↓ arrow to select "P1 Turn Speed"  
5. Use ← arrow to decrease to 3.00 for more stable handling
6. Use ↓ arrow to select "Wall Stickiness"
7. Use ← arrow to decrease to 0.20 for smoother wall sliding
8. Switch to game window and test the changes
9. Return to settings to fine-tune **Friction** for perfect feel
10. Press 'q' when done adjusting settings

The settings interface provides immediate feedback and allows for precise tuning of the game experience!
