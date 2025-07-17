#!/usr/bin/env python3
"""
Web-compatible main entry point for the racing game.
Compatible with both local execution and Pygbag web compilation.
"""

import asyncio
import pygame
import sys
import math
from typing import Optional
from pathlib import Path

# Import game modules
from settings import *
from car import Car
from track import Track
from game_settings import game_settings
from controls import PLAYER1_CONTROLS, PLAYER2_CONTROLS
from car import Car
from track import Track
from controls import PLAYER1_CONTROLS, PLAYER2_CONTROLS
from game_settings import game_settings

# Import game modules
from settings import *
from car import Car
from track import Track
from game_settings import game_settings
from controls import PLAYER1_CONTROLS, PLAYER2_CONTROLS
from web_settings_interface import WebSettingsInterface


class RacingGameWeb:
    """Web-compatible racing game class."""
    
    def __init__(self):
        """Initialize the web-compatible racing game."""
        pygame.init()
        
        # Create display
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(WINDOW_TITLE)
        self.clock = pygame.time.Clock()
        
        # Initialize game objects
        self.track = Track()
        self.running = True
        
        # Load track
        if not self.track.load_track():
            print("Using fallback track")
        
        # Get starting positions
        start_positions = self.track.get_start_positions()
        if len(start_positions) >= 2:
            player1_pos = start_positions[0]
            player2_pos = start_positions[1]
        else:
            # Fallback positions
            player1_pos = (SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2)
            player2_pos = (SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2 + 50)
        
        # Create cars with proper starting angle (facing up = 270°)
        self.car1 = Car(player1_pos, SPORTS_CAR)
        self.car1.angle = 270.0  # Face up
        
        self.car2 = Car(player2_pos, TRUCK)
        self.car2.angle = 270.0  # Face up
        
        self.cars = [self.car1, self.car2]
        
        # Initialize web settings interface
        self.web_settings = WebSettingsInterface(self.screen)
        
        # Web-specific settings
        self.is_web = self._detect_web_environment()
        
        print(f"Player 1 (Sports Car) created at {player1_pos}")
        print(f"Player 2 (Truck) created at {player2_pos}")
        print("Cars start facing up. White lights indicate reverse gear.")
        
        if self.is_web:
            print("🌐 Running in web mode")
            print("Settings: Press TAB to toggle in-game settings menu")
        
    def _detect_web_environment(self) -> bool:
        """Detect if running in web browser via Pygbag."""
        try:
            # Pygbag sets this when running in browser
            import platform
            return platform.system() == "Emscripten" or "emscripten" in sys.platform.lower()
        except:
            return False
    
    async def run(self):
        """Main game loop - async for web compatibility."""
        while self.running:
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                    elif event.key == pygame.K_TAB:
                        self.web_settings.toggle_visibility()
                    
                    # Pass event to settings interface
                    self.web_settings.handle_event(event)
            
            # Get key states
            keys = pygame.key.get_pressed()
            
            # Update cars
            self.car1.update(keys, PLAYER1_CONTROLS, self.track)
            self.car2.update(keys, PLAYER2_CONTROLS, self.track)
            
            # Render everything
            self._render()
            
            # Update display
            pygame.display.flip()
            self.clock.tick(FPS)
            
            # Yield control for web compatibility
            if self.is_web:
                await asyncio.sleep(0)
    
    def _render(self):
        """Render the game."""
        # Clear screen
        self.screen.fill(COLORS['BLACK'])
        
        # Render track
        self.track.render(self.screen)
        
        # Render cars
        self.car1.render(self.screen)
        self.car2.render(self.screen)
        
        # Render UI
        self._render_ui()
        
        # Render web settings interface
        self.web_settings.render()
    
    def _render_ui(self):
        """Render user interface elements."""
        font = pygame.font.Font(None, 24)
        
        # Instructions
        instructions = [
            "Player 1: WASD (S for reverse)",
            "Player 2: Arrow Keys (↓ for reverse)",
        ]
        
        if self.is_web:
            instructions.append("TAB: Settings Menu")
        
        for i, instruction in enumerate(instructions):
            text_surface = font.render(instruction, True, COLORS['WHITE'])
            self.screen.blit(text_surface, (10, 10 + i * 25))
        
        # Show current car stats
        stats_y = 10 + len(instructions) * 25 + 10
        
        # Player 1 stats
        car1_speed = math.sqrt(self.car1.velocity_x**2 + self.car1.velocity_y**2)
        car1_stats = [
            f"P1 Speed: {car1_speed:.1f}",
            f"P1 Reverse: {'Yes' if self.car1.is_reversing else 'No'}",
        ]
        
        for i, stat in enumerate(car1_stats):
            color = COLORS['RED'] if 'Reverse: Yes' in stat else COLORS['YELLOW']
            text_surface = font.render(stat, True, color)
            self.screen.blit(text_surface, (10, stats_y + i * 25))
        
        # Player 2 stats
        p2_stats_y = stats_y + len(car1_stats) * 25 + 10
        car2_speed = math.sqrt(self.car2.velocity_x**2 + self.car2.velocity_y**2)
        car2_stats = [
            f"P2 Speed: {car2_speed:.1f}",
            f"P2 Reverse: {'Yes' if self.car2.is_reversing else 'No'}",
        ]
        
        for i, stat in enumerate(car2_stats):
            color = COLORS['RED'] if 'Reverse: Yes' in stat else COLORS['BLUE']
            text_surface = font.render(stat, True, color)
            self.screen.blit(text_surface, (10, p2_stats_y + i * 25))


async def main():
    """Main entry point for web compatibility."""
    game = RacingGameWeb()
    await game.run()
    pygame.quit()

if __name__ == "__main__":
    # Run with asyncio for web compatibility
    asyncio.run(main())
