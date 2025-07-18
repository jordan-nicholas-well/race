"""
Desktop main entry point for the 2D Racing Game.

This module initializes Pygame, creates the game window, instantiates the track
and cars, and contains the main game loop with event handling and rendering.
"""

import sys
from typing import Dict, List
import pygame
from settings import (
    SCREEN_WIDTH, SCREEN_HEIGHT, FPS, WINDOW_TITLE, COLORS,
    SPORTS_CAR, TRUCK
)
from controls import PLAYER1_CONTROLS, PLAYER2_CONTROLS
from track import Track
from car import Car
from game_settings import game_settings
from settings_interface import settings_interface


class RacingGame:
    """
    Main game class that manages the racing game state and game loop.
    """
    
    def __init__(self) -> None:
        """Initialize the racing game."""
        # Initialize Pygame
        pygame.init()
        
        # Create the game window
        self.screen: pygame.Surface = pygame.display.set_mode(
            (SCREEN_WIDTH, SCREEN_HEIGHT)
        )
        pygame.display.set_caption(WINDOW_TITLE)
        
        # Initialize clock for FPS control
        self.clock: pygame.time.Clock = pygame.time.Clock()
        
        # Initialize game objects
        self.track: Track = Track()
        self.cars: List[Car] = []
        self.running: bool = True
        
        # Load track and create cars
        self._initialize_game()
    
    def _initialize_game(self) -> None:
        """Initialize the track and cars."""
        # Load the track
        if not self.track.load_track():
            print("Using fallback track")
        
        # Get starting positions
        start_positions = self.track.get_start_positions()
        
        if len(start_positions) < 2:
            print("Warning: Not enough start positions found. Using default positions.")
            start_positions = [
                (SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2),
                (SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2 + 50)
            ]
        
        # Create Player 1 car (Sports Car)
        self.cars.append(Car(start_positions[0], SPORTS_CAR))
        print(f"Player 1 (Sports Car) created at {start_positions[0]}")
        
        # Create Player 2 car (Truck)
        if len(start_positions) > 1:
            self.cars.append(Car(start_positions[1], TRUCK))
            print(f"Player 2 (Truck) created at {start_positions[1]}")
        else:
            # Use a slightly offset position if only one start position available
            offset_pos = (start_positions[0][0], start_positions[0][1] + 30)
            self.cars.append(Car(offset_pos, TRUCK))
            print(f"Player 2 (Truck) created at {offset_pos}")
        
        # Set cars for the settings interface
        settings_interface.set_cars(self.cars)
    
    def _handle_events(self) -> None:
        """Handle pygame events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
        
        # Get currently pressed keys for continuous movement
        keys_pressed = pygame.key.get_pressed()
        
        # Update cars with continuous key presses
        if len(self.cars) > 0:
            self.cars[0].update(keys_pressed, PLAYER1_CONTROLS, self.track)
        if len(self.cars) > 1:
            self.cars[1].update(keys_pressed, PLAYER2_CONTROLS, self.track)
    
    def _render(self) -> None:
        """Render all game objects to the screen."""
        # Clear screen
        self.screen.fill(COLORS['BLACK'])
        
        # Render track
        self.track.render(self.screen)
        
        # Render cars
        for car in self.cars:
            car.render(self.screen)
        
        # Render UI information
        self._render_ui()
        
        # Update display
        pygame.display.flip()
    
    def _render_ui(self) -> None:
        """Render user interface elements."""
        font = pygame.font.Font(None, 24)
        
        # Game info
        info_lines = [
            "🎮 2D Racing Game",
            "Player 1: WASD | Player 2: Arrow Keys",
            "TAB: Settings Menu | ESC: Quit",
        ]
        
        for i, line in enumerate(info_lines):
            text_surface = font.render(line, True, COLORS['WHITE'])
            self.screen.blit(text_surface, (10, 10 + i * 25))
        
        # Show current car stats
        if len(self.cars) > 0:
            car = self.cars[0]
            import math
            current_speed = math.sqrt(car.velocity_x**2 + car.velocity_y**2)
            stats_text = [
                f"P1 Speed: {current_speed:.1f}/{car.max_speed:.1f}",
                f"P1 Turn: {car.turn_speed:.1f}",
                f"P1 Reversing: {'Yes' if car.is_reversing else 'No'}",
            ]
            
            for i, stat in enumerate(stats_text):
                if i == 2 and car.is_reversing:
                    color = COLORS['RED']
                else:
                    color = COLORS['YELLOW']
                text_surface = font.render(stat, True, color)
                self.screen.blit(text_surface, (10, 100 + i * 25))
        
        # Show Player 2 stats
        if len(self.cars) > 1:
            car2 = self.cars[1]
            import math
            current_speed2 = math.sqrt(car2.velocity_x**2 + car2.velocity_y**2)
            stats_text = [
                f"P2 Speed: {current_speed2:.1f}/{car2.max_speed:.1f}",
                f"P2 Turn: {car2.turn_speed:.1f}",
                f"P2 Reversing: {'Yes' if car2.is_reversing else 'No'}",
            ]
            
            for i, stat in enumerate(stats_text):
                if i == 2 and car2.is_reversing:
                    color = COLORS['RED']
                else:
                    color = COLORS['BLUE']
                text_surface = font.render(stat, True, color)
                self.screen.blit(text_surface, (10, 200 + i * 25))
    
    def run(self) -> None:
        """Run the main game loop."""
        print("Starting 2D Racing Game...")
        print("🎮 Controls: Player 1 (WASD) | Player 2 (Arrow Keys)")
        print("TAB: Settings Menu | ESC: Quit")
        
        # Start the settings interface thread
        settings_interface.start()
        
        try:
            while self.running:
                self._handle_events()
                self._render()
                self.clock.tick(FPS)
        except KeyboardInterrupt:
            print("\n🛑 Game interrupted by user")
        finally:
            # Stop the settings interface
            settings_interface.stop()
            pygame.quit()
            print("Game ended.")


def main() -> None:
    """Main function to start the game."""
    game = RacingGame()
    game.run()


if __name__ == "__main__":
    main()
