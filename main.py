#!/usr/bin/env python3
"""
Racing game - Web compatible version for Pygbag
"""

import asyncio
import math
import sys

import pygame

from car import Car
from controls import PLAYER1_CONTROLS, PLAYER2_CONTROLS
from game_settings import game_settings

# Import core game modules
from settings import *
from track import Track

try:
    from web_settings_interface import WebSettingsInterface

    HAS_WEB_SETTINGS = True
except ImportError:
    HAS_WEB_SETTINGS = False


class RacingGameWeb:
    """Web-compatible racing game class for Pygbag."""

    def __init__(self):
        print("🌐 INITTING")
        """Initialize the web racing game."""
        # Initialize pygame and display IMMEDIATELY
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(WINDOW_TITLE)
        self.clock = pygame.time.Clock()

        # Initialize game objects
        self.track = Track()
        self.track.load_track()

        # Get starting positions
        start_positions = self.track.get_start_positions()
        if len(start_positions) >= 2:
            car1_pos, car2_pos = start_positions[0], start_positions[1]
        else:
            car1_pos = (SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2)
            car2_pos = (SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2 + 50)

        # Create cars
        self.car1 = Car(car1_pos, SPORTS_CAR)
        self.car1.angle = 270.0
        self.car2 = Car(car2_pos, TRUCK)
        self.car2.angle = 270.0

        # Web settings
        if HAS_WEB_SETTINGS:
            self.web_settings = WebSettingsInterface(self.screen)
        else:
            self.web_settings = None

        # Game state
        self.running = True

    async def render_ui(self):
        """Render UI elements."""
        font = pygame.font.Font(None, 24)

        instructions = [
            "Player 1: WASD (S for reverse)",
            "Player 2: Arrow Keys (↓ for reverse)",
        ]

        if self.web_settings:
            instructions.append("TAB: Settings Menu")

        for i, instruction in enumerate(instructions):
            text_surface = font.render(instruction, True, COLORS["WHITE"])
            self.screen.blit(text_surface, (10, 10 + i * 25))

        # Car stats
        stats_y = 10 + len(instructions) * 25 + 10

        car1_speed = math.sqrt(self.car1.velocity_x**2 + self.car1.velocity_y**2)
        car1_stats = [
            f"P1 Speed: {car1_speed:.1f}",
            f"P1 Reverse: {'Yes' if self.car1.is_reversing else 'No'}",
        ]

        for i, stat in enumerate(car1_stats):
            color = COLORS["RED"] if "Reverse: Yes" in stat else COLORS["YELLOW"]
            text_surface = font.render(stat, True, color)
            self.screen.blit(text_surface, (10, stats_y + i * 25))

        p2_stats_y = stats_y + len(car1_stats) * 25 + 10
        car2_speed = math.sqrt(self.car2.velocity_x**2 + self.car2.velocity_y**2)
        car2_stats = [
            f"P2 Speed: {car2_speed:.1f}",
            f"P2 Reverse: {'Yes' if self.car2.is_reversing else 'No'}",
        ]

        for i, stat in enumerate(car2_stats):
            color = COLORS["RED"] if "Reverse: Yes" in stat else COLORS["BLUE"]
            text_surface = font.render(stat, True, color)
            self.screen.blit(text_surface, (10, p2_stats_y + i * 25))

    async def run(self):
        """Main game loop - MUST be async for Pygbag."""
        print("🌐 Starting web racing game...")

        while self.running:
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                    elif event.key == pygame.K_TAB and self.web_settings:
                        self.web_settings.toggle_visibility()

                    if self.web_settings:
                        self.web_settings.handle_event(event)

            # Get key states
            keys = pygame.key.get_pressed()

            # Update cars
            self.car1.update(keys, PLAYER1_CONTROLS, self.track)
            self.car2.update(keys, PLAYER2_CONTROLS, self.track)

            # Render
            self.screen.fill(COLORS["BLACK"])
            self.track.render(self.screen)
            self.car1.render(self.screen)
            self.car2.render(self.screen)
            self.render_ui()

            if self.web_settings:
                self.web_settings.render()

            pygame.display.flip()
            self.clock.tick(FPS)

            # CRITICAL: This yield is required for Pygbag
            await asyncio.sleep(0)

        pygame.quit()
        print("👋 Web game finished!")


# Legacy support - only run if this file is executed directly
if __name__ == "__main__":
    # This will only run if main_web.py is called directly (not through universal launcher)
    game = RacingGameWeb()
    asyncio.run(game.run())
