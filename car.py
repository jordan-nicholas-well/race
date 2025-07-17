"""
Car class for handling car physics, movement, and rendering.

This module provides the Car class which manages individual car behavior,
including physics simulation, collision detection, and visual rendering.
"""

from typing import Dict, Any, Tuple
import math
import pygame
from settings import (
    TRACK_COLORS, SLOW_DOWN_MULTIPLIER, COLORS, 
    PHYSICS_ADJUSTMENT, SCREEN_WIDTH, SCREEN_HEIGHT
)


class Car:
    """
    Represents a racing car with physics simulation and rendering.
    
    Handles acceleration, velocity, friction, turning, collision detection,
    and visual representation of the car.
    """
    
    def __init__(self, start_position: Tuple[int, int], stats: Dict[str, Any]) -> None:
        """
        Initialize a car with given starting position and statistics.
        
        Args:
            start_position: (x, y) tuple for the car's starting position
            stats: Dictionary containing car physics and visual properties
        """
        # Position and movement
        self.x: float = float(start_position[0])
        self.y: float = float(start_position[1])
        self.start_x: float = self.x
        self.start_y: float = self.y
        self.velocity_x: float = 0.0
        self.velocity_y: float = 0.0
        self.angle: float = 0.0  # Car's rotation angle in degrees
        
        # Physics parameters (can be modified at runtime)
        self.acceleration: float = stats['acceleration']
        self.max_speed: float = stats['max_speed']
        self.current_max_speed: float = self.max_speed  # Can be reduced by slow-down areas
        self.friction: float = stats['friction']
        self.turn_speed: float = stats['turn_speed']
        
        # Visual properties
        self.color: Tuple[int, int, int] = stats['color']
        self.size: Tuple[int, int] = stats['size']
        self.image_path: str = stats.get('image_path', None)
        
        # Car surface for rendering
        self.surface: pygame.Surface = self._create_car_surface()
        self.rect: pygame.Rect = self.surface.get_rect()
        
        # State tracking
        self.on_slow_surface: bool = False
    
    def _create_car_surface(self) -> pygame.Surface:
        """
        Create the visual representation of the car.
        
        Returns:
            pygame.Surface: The car's visual surface
        """
        if self.image_path:
            try:
                surface = pygame.image.load(self.image_path)
                return pygame.transform.scale(surface, self.size)
            except pygame.error:
                print(f"Could not load car image: {self.image_path}")
        
        # Create a simple colored rectangle as fallback
        surface = pygame.Surface(self.size)
        surface.fill(self.color)
        
        # Add a small indicator for the front of the car
        front_rect = pygame.Rect(self.size[0] - 4, self.size[1] // 2 - 2, 4, 4)
        pygame.draw.rect(surface, COLORS['WHITE'], front_rect)
        
        return surface
    
    def update(self, keys_pressed, controls: Dict[str, int], 
               track) -> None:
        """
        Update the car's position and physics based on input and track conditions.
        
        Args:
            keys_pressed: Pygame key state from pygame.key.get_pressed()
            controls: Control scheme for this car
            track: Track object for collision detection
        """
        # Handle input
        accelerating = keys_pressed[controls['accelerate']]
        braking = keys_pressed[controls['brake']]
        turning_left = keys_pressed[controls['turn_left']]
        turning_right = keys_pressed[controls['turn_right']]
        
        # Handle turning (only when moving)
        speed = math.sqrt(self.velocity_x**2 + self.velocity_y**2)
        if speed > 0.1:  # Only turn when moving
            if turning_left:
                self.angle -= self.turn_speed * (speed / self.max_speed)
            if turning_right:
                self.angle += self.turn_speed * (speed / self.max_speed)
        
        # Handle acceleration and braking
        if accelerating:
            # Calculate acceleration in the direction the car is facing
            angle_rad = math.radians(self.angle)
            accel_x = math.cos(angle_rad) * self.acceleration
            accel_y = math.sin(angle_rad) * self.acceleration
            
            self.velocity_x += accel_x
            self.velocity_y += accel_y
        
        if braking:
            # Apply braking force
            brake_force = 0.2
            if speed > 0:
                brake_x = -(self.velocity_x / speed) * brake_force
                brake_y = -(self.velocity_y / speed) * brake_force
                self.velocity_x += brake_x
                self.velocity_y += brake_y
        
        # Apply friction
        self.velocity_x *= self.friction
        self.velocity_y *= self.friction
        
        # Limit speed
        current_speed = math.sqrt(self.velocity_x**2 + self.velocity_y**2)
        if current_speed > self.current_max_speed:
            scale = self.current_max_speed / current_speed
            self.velocity_x *= scale
            self.velocity_y *= scale
        
        # Update position
        new_x = self.x + self.velocity_x
        new_y = self.y + self.velocity_y
        
        # Check track collision before moving
        surface_color = track.check_collision(int(new_x), int(new_y))
        
        if surface_color == TRACK_COLORS['WALL']:
            # Hit a wall, reset to start position and stop
            self._reset_to_start()
        elif surface_color == TRACK_COLORS['SLOW_DOWN']:
            # On slow-down surface (grass/sand)
            self.current_max_speed = self.max_speed * SLOW_DOWN_MULTIPLIER
            self.on_slow_surface = True
            self.x = new_x
            self.y = new_y
        else:
            # On normal track surface
            self.current_max_speed = self.max_speed
            self.on_slow_surface = False
            self.x = new_x
            self.y = new_y
        
        # Keep car within screen bounds as a failsafe
        self.x = max(0, min(SCREEN_WIDTH - self.size[0], self.x))
        self.y = max(0, min(SCREEN_HEIGHT - self.size[1], self.y))
    
    def _reset_to_start(self) -> None:
        """Reset the car to its starting position and stop movement."""
        self.x = self.start_x
        self.y = self.start_y
        self.velocity_x = 0.0
        self.velocity_y = 0.0
        self.angle = 0.0
        print(f"Car crashed and reset to start position: ({self.start_x}, {self.start_y})")
    
    def adjust_physics(self, parameter: str, increase: bool) -> None:
        """
        Adjust car physics parameters at runtime.
        
        Args:
            parameter: The parameter to adjust ('turn_speed' or 'acceleration')
            increase: True to increase, False to decrease
        """
        if parameter == 'turn_speed':
            increment = PHYSICS_ADJUSTMENT['turn_speed_increment']
            if increase:
                self.turn_speed = min(
                    self.turn_speed + increment,
                    self.turn_speed * PHYSICS_ADJUSTMENT['max_adjustment']
                )
            else:
                self.turn_speed = max(
                    self.turn_speed - increment,
                    self.turn_speed * PHYSICS_ADJUSTMENT['min_adjustment']
                )
            print(f"Turn speed adjusted to: {self.turn_speed:.2f}")
        
        elif parameter == 'acceleration':
            increment = PHYSICS_ADJUSTMENT['acceleration_increment']
            if increase:
                self.acceleration = min(
                    self.acceleration + increment,
                    self.acceleration * PHYSICS_ADJUSTMENT['max_adjustment']
                )
            else:
                self.acceleration = max(
                    self.acceleration - increment,
                    self.acceleration * PHYSICS_ADJUSTMENT['min_adjustment']
                )
            print(f"Acceleration adjusted to: {self.acceleration:.2f}")
    
    def render(self, screen: pygame.Surface) -> None:
        """
        Render the car to the screen with proper rotation.
        
        Args:
            screen: The pygame surface to render to
        """
        # Rotate the car surface based on current angle
        rotated_surface = pygame.transform.rotate(self.surface, -self.angle)
        
        # Get the rect for the rotated surface and center it on the car's position
        rotated_rect = rotated_surface.get_rect()
        rotated_rect.center = (int(self.x), int(self.y))
        
        # Blit the rotated car to the screen
        screen.blit(rotated_surface, rotated_rect)
        
        # Optional: Draw a small circle at the car's center for debugging
        # pygame.draw.circle(screen, COLORS['YELLOW'], (int(self.x), int(self.y)), 2)
