#!/usr/bin/env python3
"""
Track generator utility to create basic track images for testing.

This script creates simple track images that can be used as a starting point
for custom track design.
"""

import pygame
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, TRACK_COLORS

def create_simple_track():
    """Create simple track images for testing purposes."""
    
    pygame.init()
    
    # Create visual track
    visual_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    visual_surface.fill((50, 150, 50))  # Green background (grass)
    
    # Create mask surface
    mask_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    mask_surface.fill(TRACK_COLORS['WALL'])  # White background (walls)
    
    # Track dimensions
    outer_rect = pygame.Rect(100, 100, SCREEN_WIDTH - 200, SCREEN_HEIGHT - 200)
    inner_rect = pygame.Rect(250, 250, SCREEN_WIDTH - 500, SCREEN_HEIGHT - 500)
    
    # Draw visual track
    pygame.draw.ellipse(visual_surface, (80, 80, 80), outer_rect)  # Gray track
    pygame.draw.ellipse(visual_surface, (50, 150, 50), inner_rect)  # Green center
    
    # Add some visual details
    pygame.draw.ellipse(visual_surface, (100, 100, 100), outer_rect, 10)  # Track borders
    pygame.draw.ellipse(visual_surface, (40, 120, 40), inner_rect, 5)  # Inner border
    
    # Draw mask track
    pygame.draw.ellipse(mask_surface, TRACK_COLORS['TRACK_SURFACE'], outer_rect)  # Black track
    pygame.draw.ellipse(mask_surface, TRACK_COLORS['WALL'], inner_rect)  # White inner wall
    
    # Add start positions (blue dots)
    start_pos1 = (150, SCREEN_HEIGHT // 2 - 20)
    start_pos2 = (150, SCREEN_HEIGHT // 2 + 20)
    
    pygame.draw.circle(mask_surface, TRACK_COLORS['START_POSITION'], start_pos1, 3)
    pygame.draw.circle(mask_surface, TRACK_COLORS['START_POSITION'], start_pos2, 3)
    
    # Add some slow-down areas (green patches)
    slow_areas = [
        (SCREEN_WIDTH - 200, 200, 50, 50),
        (SCREEN_WIDTH - 200, SCREEN_HEIGHT - 250, 50, 50),
        (200, 150, 40, 40),
        (200, SCREEN_HEIGHT - 190, 40, 40),
    ]
    
    for area in slow_areas:
        # Visual green patches
        pygame.draw.rect(visual_surface, (30, 100, 30), area)
        # Mask green areas
        pygame.draw.rect(mask_surface, TRACK_COLORS['SLOW_DOWN'], area)
    
    # Save the images
    try:
        pygame.image.save(visual_surface, "track1_visual.png")
        pygame.image.save(mask_surface, "track1_mask.png")
        print("✓ Track images created successfully!")
        print("  - track1_visual.png: Visual track image")
        print("  - track1_mask.png: Collision mask image")
        print("  - Ready to use with the racing game!")
        return True
    except Exception as e:
        print(f"❌ Error creating track images: {e}")
        return False
    finally:
        pygame.quit()

if __name__ == "__main__":
    print("Creating simple track images...")
    create_simple_track()
