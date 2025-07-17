"""
Main entry point for the 2D Racing Game.

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
from controls import PLAYER1_CONTROLS, PLAYER2_CONTROLS, PHYSICS_CONTROLS
from track import Track
from car import Car
from game_settings import game_settings


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
    
    def _handle_events(self) -> None:
        """Handle pygame events including physics adjustments."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            elif event.type == pygame.KEYDOWN:
                # Physics adjustment controls (affect Player 1 car)
                if len(self.cars) > 0:
                    car = self.cars[0]  # Player 1 car
                    
                    if event.key == PHYSICS_CONTROLS['increase_turn_speed']:
                        car.adjust_physics('turn_speed', True)
                    elif event.key == PHYSICS_CONTROLS['decrease_turn_speed']:
                        car.adjust_physics('turn_speed', False)
                    elif event.key == PHYSICS_CONTROLS['increase_acceleration']:
                        car.adjust_physics('acceleration', True)
                    elif event.key == PHYSICS_CONTROLS['decrease_acceleration']:
                        car.adjust_physics('acceleration', False)
                    elif event.key == PHYSICS_CONTROLS['increase_stickiness']:
                        game_settings.adjust_stickiness(True)
                    elif event.key == PHYSICS_CONTROLS['decrease_stickiness']:
                        game_settings.adjust_stickiness(False)
        
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
        font = pygame.font.Font(None, 36)
        
        # Render controls instructions
        instructions = [
            "Player 1: WASD to move (S to reverse)",
            "Player 2: Arrow keys to move (↓ to reverse)",
            "U/J: Adjust turn speed | I/K: Adjust acceleration",
            "O/L: Adjust wall stickiness",
        ]
        
        for i, instruction in enumerate(instructions):
            text_surface = font.render(instruction, True, COLORS['WHITE'])
            self.screen.blit(text_surface, (10, 10 + i * 30))
        
        # Show current car stats for Player 1
        if len(self.cars) > 0:
            car = self.cars[0]
            stats_text = [
                f"P1 Turn Speed: {car.turn_speed:.2f}",
                f"P1 Acceleration: {car.acceleration:.2f}",
                f"P1 Reversing: {'Yes' if car.is_reversing else 'No'}",
                f"Wall Stickiness: {game_settings.wall_stickiness:.2f}",
            ]
            
            for i, stat in enumerate(stats_text):
                if i == 2 and car.is_reversing:
                    color = COLORS['RED']
                elif i == 3:
                    color = COLORS['GREEN']
                else:
                    color = COLORS['YELLOW']
                text_surface = font.render(stat, True, color)
                self.screen.blit(text_surface, (10, 150 + i * 30))
        
        # Show reverse status for Player 2
        if len(self.cars) > 1:
            car2 = self.cars[1]
            if car2.is_reversing:
                text_surface = font.render("P2 Reversing: Yes", True, COLORS['RED'])
                self.screen.blit(text_surface, (10, 270))
    
    def run(self) -> None:
        """Run the main game loop."""
        print("Starting Racing Game...")
        print("Controls:")
        print("  Player 1: WASD (S for reverse)")
        print("  Player 2: Arrow Keys (↓ for reverse)")
        print("  U/J: Adjust Player 1 turn speed")
        print("  I/K: Adjust Player 1 acceleration")
        print("  O/L: Adjust wall stickiness")
        print("Cars start facing up. White lights indicate reverse gear.")
        
        while self.running:
            # Handle events and input
            self._handle_events()
            
            # Render everything
            self._render()
            
            # Control frame rate
            self.clock.tick(FPS)
        
        # Cleanup
        pygame.quit()
        sys.exit()


def main() -> None:
    """Main function to start the racing game."""
    try:
        game = RacingGame()
        game.run()
    except Exception as e:
        print(f"Error running game: {e}")
        pygame.quit()
        sys.exit(1)


if __name__ == "__main__":
    main()
