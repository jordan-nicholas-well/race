# Track Asset Creation Guide

This guide provides detailed instructions for creating custom track images for the 2D Racing Game.

## Image Requirements

- **Dimensions**: Both images must be exactly 1280x720 pixels
- **Format**: PNG format
- **Names**: `track1_visual.png` and `track1_mask.png`
- **Location**: Place both files in the same directory as `main.py`

## Creating track1_visual.png (Visual Track)

This is the image players will see during gameplay. Be creative with your design!

### Recommended Elements:
- **Track surface**: Use asphalt-like colors (dark gray, black)
- **Grass areas**: Green colors for areas around the track
- **Barriers/walls**: Brown, concrete, or metallic colors
- **Start/finish line**: White dashed lines or checkered pattern
- **Track markings**: Lane dividers, corner markers, etc.

### Design Tips:
- Make the track wide enough for two cars (at least 60-80 pixels wide)
- Ensure there's a clear racing line
- Add visual interest with color variations
- Consider adding texture or patterns

## Creating track1_mask.png (Collision Mask)

This image defines the game logic and MUST use exact color values:

### Required Colors (RGB Values):

#### Black (0, 0, 0) - Drivable Track Surface
- Use pure black for all areas where cars can drive
- This includes the main track and any alternate routes

#### White (255, 255, 255) - Walls and Barriers  
- Use pure white for all impassable areas
- Cars will crash and reset when touching white pixels
- Include track boundaries, barriers, and obstacles

#### Blue (0, 0, 255) - Starting Positions
- Place exactly 2 blue pixels on the track
- These mark where Player 1 and Player 2 will start
- Position them side-by-side on a straight section

#### Green (0, 255, 0) - Slow-Down Areas
- Use pure green for grass, sand, or off-track areas
- Cars will have reduced speed when on green pixels
- Optional - you can skip this if you want

### Mask Creation Process:

1. **Start with a white canvas** (1280x720 pixels)
2. **Paint the track black** where cars should be able to drive
3. **Leave walls white** (barriers, boundaries, obstacles)
4. **Add 2 blue dots** for starting positions on the track
5. **Paint green areas** for slow-down zones (optional)
6. **Double-check color values** are exact - use a color picker tool

### Important Notes:

- **Alignment**: The mask must align perfectly with the visual track
- **Precision**: Use the exact RGB values listed above
- **No anti-aliasing**: Turn off anti-aliasing to avoid color mixing
- **Zoom in**: Work at high zoom levels to ensure pixel precision

## Example Workflow (GIMP):

1. Create new image: File → New → 1280x720 pixels
2. Fill with white background
3. Select brush tool with hard edge (no feathering)
4. Set foreground color to pure black (0,0,0)
5. Paint the track areas
6. Set foreground color to pure blue (0,0,255)  
7. Paint 2 small dots for start positions
8. Set foreground color to pure green (0,255,0)
9. Paint any slow-down areas
10. Export as PNG: File → Export As → track1_mask.png

## Example Workflow (Photoshop):

1. File → New → 1280x720 pixels, RGB mode
2. Fill background layer with white
3. Create new layer for track
4. Use brush tool with hardness 100%
5. Set foreground color to #000000 (black)
6. Paint the track surface
7. Create new layer for start positions
8. Set foreground color to #0000FF (blue)
9. Paint 2 small dots
10. Save as PNG: File → Export → Export As → PNG

## Testing Your Track:

1. Place both PNG files in the game directory
2. Run `python main.py`
3. Check that cars appear at the blue dots
4. Test that cars crash when hitting white areas
5. Verify slow-down areas work if you added green zones

## Quick Track Generator:

If you want to start with a basic track, run:
```bash
python create_track.py
```

This creates a simple oval track that you can use as a starting point for your own design.

## Common Issues:

- **Cars spawn in wrong places**: Check blue pixel placement
- **Cars crash unexpectedly**: Verify track areas are pure black
- **Cars don't slow down**: Ensure green areas use exact RGB(0,255,0)
- **Track doesn't align**: Visual and mask images must match perfectly

## Advanced Tips:

- Create multiple track files (track2_visual.png, track2_mask.png) and modify `settings.py`
- Use layers in your image editor for easier editing
- Save an editable version (.psd, .xcf) before exporting to PNG
- Test frequently during creation to catch issues early
