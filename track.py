"""
Track class for handling track loading, rendering, and collision detection.

This module provides the Track class which manages track visuals, collision masks,
and starting positions for the racing game.
"""

from typing import List, Tuple, Optional
import pygame
from settings import TRACK_FILES, TRACK_COLORS, SCREEN_WIDTH, SCREEN_HEIGHT


class Track:
    """
    Handles track loading, rendering, and collision detection.
    
    The track uses two images:
    - Visual image: The detailed track that players see
    - Mask image: A simplified image for collision detection
    """
    
    def __init__(self) -> None:
        """Initialize the track with visual and mask images."""
        self.visual_surface: Optional[pygame.Surface] = None
        self.mask_surface: Optional[pygame.Surface] = None
        self.start_positions: List[Tuple[int, int]] = []
        self.track_loaded: bool = False
        
    def load_track(self) -> bool:
        """
        Load the track visual and mask images.
        
        Returns:
            bool: True if track loaded successfully, False otherwise
        """
        try:
            # Load visual track image
            self.visual_surface = pygame.image.load(TRACK_FILES['visual'])
            self.visual_surface = pygame.transform.scale(
                self.visual_surface, (SCREEN_WIDTH, SCREEN_HEIGHT)
            )
            
            # Load mask image for collision detection
            self.mask_surface = pygame.image.load(TRACK_FILES['mask'])
            self.mask_surface = pygame.transform.scale(
                self.mask_surface, (SCREEN_WIDTH, SCREEN_HEIGHT)
            )
            
            # Find start positions from blue pixels
            self._find_start_positions()
            self.track_loaded = True
            return True
            
        except pygame.error as e:
            print(f"Error loading track images: {e}")
            print("Creating fallback track...")
            self._create_fallback_track()
            return False
    
    def _create_fallback_track(self) -> None:
        """Create a simple fallback track if image files are not found."""
        # Create visual surface with a simple oval track
        self.visual_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.visual_surface.fill((50, 150, 50))  # Green background
        
        # Draw track surface (gray oval)
        track_rect = pygame.Rect(100, 100, SCREEN_WIDTH - 200, SCREEN_HEIGHT - 200)
        pygame.draw.ellipse(self.visual_surface, (80, 80, 80), track_rect)
        
        # Draw inner grass area
        inner_rect = pygame.Rect(200, 200, SCREEN_WIDTH - 400, SCREEN_HEIGHT - 400)
        pygame.draw.ellipse(self.visual_surface, (50, 150, 50), inner_rect)
        
        # Create mask surface for collision detection
        self.mask_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.mask_surface.fill(TRACK_COLORS['WALL'])  # White background (walls)
        
        # Draw track surface (black - drivable)
        pygame.draw.ellipse(self.mask_surface, TRACK_COLORS['TRACK_SURFACE'], track_rect)
        
        # Draw inner walls (white)
        pygame.draw.ellipse(self.mask_surface, TRACK_COLORS['WALL'], inner_rect)
        
        # Add start positions manually
        self.start_positions = [
            (150, SCREEN_HEIGHT // 2 - 20),  # Player 1 start
            (150, SCREEN_HEIGHT // 2 + 20),  # Player 2 start
        ]
        
        # Draw start positions on mask
        for pos in self.start_positions:
            pygame.draw.circle(self.mask_surface, TRACK_COLORS['START_POSITION'], pos, 5)
        
        self.track_loaded = True
        print("Fallback track created successfully!")
    
    def _find_start_positions(self) -> None:
        """Find all blue pixels (start positions) on the mask image."""
        self.start_positions = []
        
        if self.mask_surface is None:
            return
        
        # Scan the mask surface for blue pixels
        for x in range(self.mask_surface.get_width()):
            for y in range(self.mask_surface.get_height()):
                pixel_color = self.mask_surface.get_at((x, y))[:3]  # Get RGB, ignore alpha
                if pixel_color == TRACK_COLORS['START_POSITION']:
                    self.start_positions.append((x, y))
        
        print(f"Found {len(self.start_positions)} start positions: {self.start_positions}")
    
    def get_start_positions(self) -> List[Tuple[int, int]]:
        """
        Get the list of starting positions for cars.
        
        Returns:
            List of (x, y) coordinates for car starting positions
        """
        return self.start_positions.copy()
    
    def check_collision(self, x: int, y: int) -> Tuple[int, int, int]:
        """
        Check what type of surface is at the given coordinates.
        
        Args:
            x: X coordinate to check
            y: Y coordinate to check
            
        Returns:
            RGB color tuple representing the surface type
        """
        if (self.mask_surface is None or 
            x < 0 or x >= self.mask_surface.get_width() or
            y < 0 or y >= self.mask_surface.get_height()):
            return TRACK_COLORS['WALL']  # Out of bounds is treated as wall
        
        pixel_color = self.mask_surface.get_at((int(x), int(y)))[:3]  # Get RGB
        return pixel_color
    
    def render(self, screen: pygame.Surface) -> None:
        """
        Render the track visual to the screen.
        
        Args:
            screen: The pygame surface to render to
        """
        if self.visual_surface is not None:
            screen.blit(self.visual_surface, (0, 0))
