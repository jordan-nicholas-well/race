#!/usr/bin/env python3
"""
Car sprite generator utility.

This script creates car sprite images for the racing game.
"""

import pygame
from settings import COLORS

def create_car_sprite(color: tuple, size: tuple, filename: str) -> bool:
    """
    Create a car sprite with the given color and size.
    
    Args:
        color: RGB color tuple for the car
        size: (width, height) tuple for the car dimensions
        filename: Output filename for the sprite
        
    Returns:
        bool: True if successful, False otherwise
    """
    pygame.init()
    
    # Create surface with transparency
    sprite = pygame.Surface(size, pygame.SRCALPHA)
    sprite.fill((0, 0, 0, 0))  # Transparent background
    
    width, height = size
    
    # Main car body (rounded rectangle)
    car_rect = pygame.Rect(2, 2, width - 4, height - 4)
    pygame.draw.rect(sprite, color, car_rect, border_radius=3)
    
    # Car outline (darker version of the color)
    outline_color = tuple(max(0, c - 50) for c in color)
    pygame.draw.rect(sprite, outline_color, car_rect, 2, border_radius=3)
    
    # Front of the car (slightly lighter)
    front_color = tuple(min(255, c + 30) for c in color)
    front_rect = pygame.Rect(width - 6, height // 2 - 3, 4, 6)
    pygame.draw.rect(sprite, front_color, front_rect, border_radius=1)
    
    # Windows (dark blue/gray)
    window_color = (40, 40, 60)
    # Front windshield
    front_window = pygame.Rect(width - 10, height // 2 - 2, 4, 4)
    pygame.draw.rect(sprite, window_color, front_window, border_radius=1)
    
    # Side windows
    if width > 20:  # Only add side windows for larger cars
        side_window1 = pygame.Rect(6, 4, width - 16, 2)
        side_window2 = pygame.Rect(6, height - 6, width - 16, 2)
        pygame.draw.rect(sprite, window_color, side_window1, border_radius=1)
        pygame.draw.rect(sprite, window_color, side_window2, border_radius=1)
    
    # Wheels (black circles)
    wheel_color = (20, 20, 20)
    wheel_radius = 2
    
    # Front wheels
    pygame.draw.circle(sprite, wheel_color, (width - 5, 3), wheel_radius)
    pygame.draw.circle(sprite, wheel_color, (width - 5, height - 3), wheel_radius)
    
    # Rear wheels
    pygame.draw.circle(sprite, wheel_color, (5, 3), wheel_radius)
    pygame.draw.circle(sprite, wheel_color, (5, height - 3), wheel_radius)
    
    # Headlights (small white/yellow circles)
    headlight_color = (255, 255, 200)
    pygame.draw.circle(sprite, headlight_color, (width - 2, height // 2 - 2), 1)
    pygame.draw.circle(sprite, headlight_color, (width - 2, height // 2 + 2), 1)
    
    # Save the sprite
    try:
        pygame.image.save(sprite, filename)
        print(f"✓ Created car sprite: {filename}")
        return True
    except Exception as e:
        print(f"❌ Error creating sprite {filename}: {e}")
        return False
    finally:
        pygame.quit()

def create_all_car_sprites():
    """Create all car sprites for the game."""
    print("Creating car sprites...")
    
    # Sports car (red)
    create_car_sprite(COLORS['RED'], (24, 14), "car_sports.png")
    
    # Truck (blue)
    create_car_sprite(COLORS['BLUE'], (28, 18), "car_truck.png")
    
    # Additional car types
    create_car_sprite((255, 165, 0), (26, 16), "car_orange.png")  # Orange car
    create_car_sprite((128, 0, 128), (24, 14), "car_purple.png")  # Purple car
    create_car_sprite((255, 255, 0), (25, 15), "car_yellow.png")  # Yellow car
    
    print("Car sprites created successfully!")

if __name__ == "__main__":
    create_all_car_sprites()
