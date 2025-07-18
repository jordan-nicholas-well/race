"""
Settings and configuration constants for the racing game.

This module contains all the game configuration including screen dimensions,
physics parameters, colors, and car statistics presets.
"""

from typing import Dict, Any, Tuple

# Screen and display settings
SCREEN_WIDTH: int = 1280
SCREEN_HEIGHT: int = 720
FPS: int = 60
WINDOW_TITLE: str = "2D Racing Game"

# Colors (RGB tuples)
COLORS: Dict[str, Tuple[int, int, int]] = {
    'BLACK': (0, 0, 0),
    'WHITE': (255, 255, 255),
    'RED': (255, 0, 0),
    'GREEN': (0, 255, 0),
    'BLUE': (0, 0, 255),
    'YELLOW': (255, 255, 0),
    'GRAY': (128, 128, 128),
}

# Track mask colors for collision detection
TRACK_COLORS: Dict[str, Tuple[int, int, int]] = {
    'TRACK_SURFACE': (0, 0, 0),      # Black - drivable area
    'WALL': (255, 255, 255),         # White - impassable barriers
    'START_POSITION': (0, 0, 255),   # Blue - starting points
    'SLOW_DOWN': (0, 255, 0),        # Green - grass/sand areas
}

# Car physics presets
SPORTS_CAR: Dict[str, Any] = {
    'acceleration': 0.3,
    'max_speed': 8.0,
    'friction': 0.95,
    'turn_speed': 6.0,
    'image_path': 'car_sports.png',
    'color': COLORS['RED'],
    'size': (24, 14),
}

TRUCK: Dict[str, Any] = {
    'acceleration': 0.2,
    'max_speed': 6.0,
    'friction': 0.93,
    'turn_speed': 5.0,
    'image_path': 'car_truck.png',
    'color': COLORS['BLUE'],
    'size': (28, 18),
}

# Default car stats (can be modified at runtime)
DEFAULT_CAR_STATS: Dict[str, Any] = SPORTS_CAR.copy()

# Physics adjustment increments
PHYSICS_ADJUSTMENT: Dict[str, float] = {
    'turn_speed_increment': 0.2,
    'acceleration_increment': 0.05,
    'stickiness_increment': 0.1,
    'max_adjustment': 2.0,  # Maximum multiplier for adjustments
    'min_adjustment': 0.2,  # Minimum multiplier for adjustments
}

# Slow-down effect settings
SLOW_DOWN_MULTIPLIER: float = 0.5  # Speed reduction when on slow-down areas

# Wall collision settings
WALL_STICKINESS: float = 0.4  # How much cars stick to walls (0.0 = no stick, 1.0 = very sticky)
WALL_BOUNCE_FACTOR: float = 0.6  # How much velocity is retained after wall collision
REVERSE_SPEED_MULTIPLIER: float = 0.5  # Speed multiplier when reversing

# Track settings
TRACK_FILES: Dict[str, str] = {
    'visual': 'track2_visual.png',
    'mask': 'track2_mask.png',
}
