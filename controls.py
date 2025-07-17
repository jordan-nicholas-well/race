"""
Control schemes for the racing game.

This module defines the keyboard controls for both players.
"""

from typing import Dict, Any
import pygame

# Player 1 controls (WASD)
PLAYER1_CONTROLS: Dict[str, int] = {
    'accelerate': pygame.K_w,
    'brake': pygame.K_s,
    'turn_left': pygame.K_a,
    'turn_right': pygame.K_d,
}

# Player 2 controls (Arrow keys)
PLAYER2_CONTROLS: Dict[str, int] = {
    'accelerate': pygame.K_UP,
    'brake': pygame.K_DOWN,
    'turn_left': pygame.K_LEFT,
    'turn_right': pygame.K_RIGHT,
}

# Physics adjustment controls
PHYSICS_CONTROLS: Dict[str, int] = {
    'increase_turn_speed': pygame.K_u,
    'decrease_turn_speed': pygame.K_j,
    'increase_acceleration': pygame.K_i,
    'decrease_acceleration': pygame.K_k,
    'increase_stickiness': pygame.K_o,
    'decrease_stickiness': pygame.K_l,
}
