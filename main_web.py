#!/usr/bin/env python3
"""
Racing game - Web compatible version for Pygbag
"""

import asyncio
import pygame
import sys
import math

# Import core game modules
from settings import *
from car import Car
from track import Track
from game_settings import game_settings
from controls import PLAYER1_CONTROLS, PLAYER2_CONTROLS

try:
    from web_settings_interface import WebSettingsInterface
    HAS_WEB_SETTINGS = True
except ImportError:
    HAS_WEB_SETTINGS = False

# Initialize pygame and display IMMEDIATELY at module level
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption(WINDOW_TITLE)
clock = pygame.time.Clock()

# Initialize game objects at module level
track = Track()
track.load_track()

# Get starting positions
start_positions = track.get_start_positions()
if len(start_positions) >= 2:
    car1_pos, car2_pos = start_positions[0], start_positions[1]
else:
    car1_pos = (SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2)
    car2_pos = (SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2 + 50)

# Create cars
car1 = Car(car1_pos, SPORTS_CAR)
car1.angle = 270.0
car2 = Car(car2_pos, TRUCK)
car2.angle = 270.0

# Web settings
if HAS_WEB_SETTINGS:
    web_settings = WebSettingsInterface(screen)
else:
    web_settings = None

# Game state
running = True

def render_ui():
    """Render UI elements."""
    font = pygame.font.Font(None, 24)
    
    instructions = [
        "Player 1: WASD (S for reverse)",
        "Player 2: Arrow Keys (↓ for reverse)",
    ]
    
    if web_settings:
        instructions.append("TAB: Settings Menu")
    
    for i, instruction in enumerate(instructions):
        text_surface = font.render(instruction, True, COLORS['WHITE'])
        screen.blit(text_surface, (10, 10 + i * 25))
    
    # Car stats
    stats_y = 10 + len(instructions) * 25 + 10
    
    car1_speed = math.sqrt(car1.velocity_x**2 + car1.velocity_y**2)
    car1_stats = [
        f"P1 Speed: {car1_speed:.1f}",
        f"P1 Reverse: {'Yes' if car1.is_reversing else 'No'}",
    ]
    
    for i, stat in enumerate(car1_stats):
        color = COLORS['RED'] if 'Reverse: Yes' in stat else COLORS['YELLOW']
        text_surface = font.render(stat, True, color)
        screen.blit(text_surface, (10, stats_y + i * 25))
    
    p2_stats_y = stats_y + len(car1_stats) * 25 + 10
    car2_speed = math.sqrt(car2.velocity_x**2 + car2.velocity_y**2)
    car2_stats = [
        f"P2 Speed: {car2_speed:.1f}",
        f"P2 Reverse: {'Yes' if car2.is_reversing else 'No'}",
    ]
    
    for i, stat in enumerate(car2_stats):
        color = COLORS['RED'] if 'Reverse: Yes' in stat else COLORS['BLUE']
        text_surface = font.render(stat, True, color)
        screen.blit(text_surface, (10, p2_stats_y + i * 25))

async def main():
    """Main game loop - MUST be async for Pygbag."""
    global running
    
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_TAB and web_settings:
                    web_settings.toggle_visibility()
                
                if web_settings:
                    web_settings.handle_event(event)
        
        # Get key states
        keys = pygame.key.get_pressed()
        
        # Update cars
        car1.update(keys, PLAYER1_CONTROLS, track)
        car2.update(keys, PLAYER2_CONTROLS, track)
        
        # Render
        screen.fill(COLORS['BLACK'])
        track.render(screen)
        car1.render(screen)
        car2.render(screen)
        render_ui()
        
        if web_settings:
            web_settings.render()
        
        pygame.display.flip()
        clock.tick(FPS)
        
        # CRITICAL: This yield is required for Pygbag
        await asyncio.sleep(0)
    
    pygame.quit()

# Run the game - This pattern is REQUIRED for Pygbag
asyncio.run(main())
