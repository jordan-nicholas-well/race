"""
Global game settings that can be adjusted at runtime.

This module provides a GameSettings class to manage global settings
that affect all cars and gameplay elements.
"""

from typing import Dict, Any
from settings import WALL_STICKINESS, WALL_BOUNCE_FACTOR, PHYSICS_ADJUSTMENT


class GameSettings:
    """
    Manages global game settings that can be adjusted during gameplay.
    """
    
    def __init__(self) -> None:
        """Initialize game settings with default values."""
        self.wall_stickiness: float = WALL_STICKINESS
        self.wall_bounce_factor: float = WALL_BOUNCE_FACTOR
    
    def adjust_stickiness(self, increase: bool) -> None:
        """
        Adjust the wall stickiness setting.
        
        Args:
            increase: True to increase stickiness, False to decrease
        """
        increment = PHYSICS_ADJUSTMENT['stickiness_increment']
        
        if increase:
            self.wall_stickiness = min(1.0, self.wall_stickiness + increment)
        else:
            self.wall_stickiness = max(0.0, self.wall_stickiness - increment)
        
        print(f"Wall stickiness adjusted to: {self.wall_stickiness:.2f}")
    
    def get_settings_dict(self) -> Dict[str, Any]:
        """
        Get current settings as a dictionary.
        
        Returns:
            Dict containing current settings
        """
        return {
            'wall_stickiness': self.wall_stickiness,
            'wall_bounce_factor': self.wall_bounce_factor,
        }


# Global instance
game_settings = GameSettings()
