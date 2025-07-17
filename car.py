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
    PHYSICS_ADJUSTMENT, SCREEN_WIDTH, SCREEN_HEIGHT,
    WALL_STICKINESS, WALL_BOUNCE_FACTOR, REVERSE_SPEED_MULTIPLIER
)
from game_settings import game_settings


class Car:
    """
    Represents a racing car with physics simulation and rendering.
    
    Handles acceleration, velocity, friction, turning, collision detection,
    and visual representation of the car with proper sprite rotation.
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
        self.angle: float = 270.0  # Start facing up (270 degrees in pygame coordinates)
        self.start_angle: float = self.angle  # Remember starting orientation
        
        # Physics parameters (can be modified at runtime)
        self.acceleration: float = stats['acceleration']
        self.max_speed: float = stats['max_speed']
        self.current_max_speed: float = self.max_speed  # Can be reduced by slow-down areas
        self.friction: float = stats['friction']
        self.turn_speed: float = stats['turn_speed']
        
        # Visual properties
        self.color: Tuple[int, int, int] = stats['color']
        self.size: Tuple[int, int] = stats['size']
        self.image_path: str = stats.get('image_path', '') or ''
        
        # Car surface for rendering
        self.base_surface: pygame.Surface = self._create_car_surface()
        self.rotated_surface: pygame.Surface = self.base_surface.copy()
        self.rect: pygame.Rect = self.base_surface.get_rect()
        
        # Collision detection
        self.collision_points: list = self._calculate_collision_points()
        
        # State tracking
        self.on_slow_surface: bool = False
        self.collision_bounce_factor: float = WALL_BOUNCE_FACTOR
        self.is_reversing: bool = False
    
    def _create_car_surface(self) -> pygame.Surface:
        """
        Create the visual representation of the car.
        
        Returns:
            pygame.Surface: The car's visual surface
        """
        if self.image_path:
            try:
                surface = pygame.image.load(self.image_path).convert_alpha()
                return pygame.transform.scale(surface, self.size)
            except pygame.error:
                print(f"Could not load car image: {self.image_path}, using fallback")
        
        # Create a more detailed fallback sprite
        surface = pygame.Surface(self.size, pygame.SRCALPHA)
        surface.fill((0, 0, 0, 0))  # Transparent background
        
        width, height = self.size
        
        # Main car body
        car_rect = pygame.Rect(1, 1, width - 2, height - 2)
        pygame.draw.rect(surface, self.color, car_rect, border_radius=2)
        
        # Car outline
        outline_color = tuple(max(0, c - 50) for c in self.color)
        pygame.draw.rect(surface, outline_color, car_rect, 1, border_radius=2)
        
        # Front of the car (directional indicator)
        front_color = tuple(min(255, c + 50) for c in self.color)
        front_rect = pygame.Rect(width - 4, height // 2 - 2, 3, 4)
        pygame.draw.rect(surface, front_color, front_rect)
        
        # Windows
        window_color = (40, 40, 60)
        if width > 15:
            window_rect = pygame.Rect(4, 3, width - 10, height - 6)
            pygame.draw.rect(surface, window_color, window_rect, border_radius=1)
        
        return surface
    
    def _calculate_collision_points(self) -> list:
        """
        Calculate collision detection points around the car.
        
        Returns:
            list: List of offset points for collision detection
        """
        # Create collision points around the car's perimeter
        width, height = self.size
        points = []
        
        # Front corners
        points.extend([
            (width // 2, 0),      # Front center
            (width - 2, 2),       # Front right
            (width - 2, height - 2), # Rear right
            (2, height - 2),      # Rear left
            (2, 2),               # Front left
        ])
        
        return points
    
    def _get_collision_points_world(self) -> list:
        """
        Get collision points in world coordinates (rotated and translated).
        
        Returns:
            list: List of (x, y) world coordinates for collision detection
        """
        world_points = []
        angle_rad = math.radians(self.angle)
        cos_a = math.cos(angle_rad)
        sin_a = math.sin(angle_rad)
        
        center_x = self.x
        center_y = self.y
        
        for local_x, local_y in self.collision_points:
            # Rotate point around center
            rotated_x = local_x * cos_a - local_y * sin_a
            rotated_y = local_x * sin_a + local_y * cos_a
            
            # Translate to world position
            world_x = center_x + rotated_x
            world_y = center_y + rotated_y
            
            world_points.append((int(world_x), int(world_y)))
        
        return world_points
    
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
        
        # Calculate current speed for various calculations
        speed = math.sqrt(self.velocity_x**2 + self.velocity_y**2)
        
        # Determine if we're moving forward or backward
        angle_rad = math.radians(self.angle)
        forward_x = math.cos(angle_rad)
        forward_y = math.sin(angle_rad)
        
        # Dot product to determine forward/backward motion
        dot_product = self.velocity_x * forward_x + self.velocity_y * forward_y
        self.is_reversing = dot_product < 0 and speed > 0.1
        
        # Handle turning (only when moving, with better reverse handling)
        if speed > 0.1:
            turn_factor = min(speed / self.max_speed, 1.0)
            turn_amount = self.turn_speed * turn_factor
            
            # Reverse turning direction when reversing
            if self.is_reversing:
                turn_amount *= -1
            
            if turning_left:
                self.angle -= turn_amount
            if turning_right:
                self.angle += turn_amount
        
        # Handle acceleration and braking/reverse
        if accelerating:
            # Forward acceleration
            angle_rad = math.radians(self.angle)
            accel_x = math.cos(angle_rad) * self.acceleration
            accel_y = math.sin(angle_rad) * self.acceleration
            
            self.velocity_x += accel_x
            self.velocity_y += accel_y
        
        if braking:
            # Check if we're already moving backward or stopped
            if speed < 0.5:
                # Start reversing
                angle_rad = math.radians(self.angle)
                reverse_accel = self.acceleration * REVERSE_SPEED_MULTIPLIER
                accel_x = -math.cos(angle_rad) * reverse_accel
                accel_y = -math.sin(angle_rad) * reverse_accel
                
                self.velocity_x += accel_x
                self.velocity_y += accel_y
            else:
                # Apply braking force
                brake_force = 0.3
                brake_x = -(self.velocity_x / speed) * brake_force
                brake_y = -(self.velocity_y / speed) * brake_force
                self.velocity_x += brake_x
                self.velocity_y += brake_y
        
        # Apply friction
        self.velocity_x *= self.friction
        self.velocity_y *= self.friction
        
        # Limit speed (different limits for forward and reverse)
        current_speed = math.sqrt(self.velocity_x**2 + self.velocity_y**2)
        max_speed_to_use = self.current_max_speed
        
        if self.is_reversing:
            max_speed_to_use *= REVERSE_SPEED_MULTIPLIER
        
        if current_speed > max_speed_to_use:
            scale = max_speed_to_use / current_speed
            self.velocity_x *= scale
            self.velocity_y *= scale
        
        # Calculate new position
        new_x = self.x + self.velocity_x
        new_y = self.y + self.velocity_y
        
        # Check for collisions before moving
        collision_result = self._check_collision(new_x, new_y, track)
        
        if collision_result['collision']:
            # Handle collision
            self._handle_collision(collision_result, track)
        else:
            # Safe to move
            self.x = new_x
            self.y = new_y
            
            # Check surface type at new position
            surface_color = track.check_collision(int(self.x), int(self.y))
            if surface_color == TRACK_COLORS['SLOW_DOWN']:
                self.current_max_speed = self.max_speed * SLOW_DOWN_MULTIPLIER
                self.on_slow_surface = True
            else:
                self.current_max_speed = self.max_speed
                self.on_slow_surface = False
        
        # Keep car within screen bounds as a failsafe
        self.x = max(self.size[0] // 2, min(SCREEN_WIDTH - self.size[0] // 2, self.x))
        self.y = max(self.size[1] // 2, min(SCREEN_HEIGHT - self.size[1] // 2, self.y))
        
        # Update rotated surface for rendering
        self.rotated_surface = pygame.transform.rotate(self.base_surface, -self.angle)
    
    def _check_collision(self, new_x: float, new_y: float, track) -> Dict[str, Any]:
        """
        Check if the car would collide at the new position.
        
        Args:
            new_x: Proposed new X position
            new_y: Proposed new Y position
            track: Track object for collision detection
            
        Returns:
            Dict containing collision information
        """
        # Temporarily move car to check collision points
        old_x, old_y = self.x, self.y
        self.x, self.y = new_x, new_y
        
        collision_points = self._get_collision_points_world()
        wall_collisions = []
        
        # Check each collision point
        for point_x, point_y in collision_points:
            surface_color = track.check_collision(point_x, point_y)
            if surface_color == TRACK_COLORS['WALL']:
                wall_collisions.append((point_x, point_y))
        
        # Restore position
        self.x, self.y = old_x, old_y
        
        return {
            'collision': len(wall_collisions) > 0,
            'wall_points': wall_collisions,
            'collision_count': len(wall_collisions)
        }
    
    def _handle_collision(self, collision_result: Dict[str, Any], track) -> None:
        """
        Handle collision with walls by adjusting velocity and position.
        
        Args:
            collision_result: Collision information from _check_collision
            track: Track object for collision detection
        """
        # Calculate collision severity and apply velocity reduction
        collision_count = collision_result['collision_count']
        
        # Less sticky behavior - use global stickiness setting
        base_velocity_reduction = 0.2 + (collision_count * 0.1)
        velocity_reduction = base_velocity_reduction * game_settings.wall_stickiness
        
        # Apply velocity reduction with bounce factor
        bounce_factor = game_settings.wall_bounce_factor
        self.velocity_x *= bounce_factor * (1.0 - velocity_reduction)
        self.velocity_y *= bounce_factor * (1.0 - velocity_reduction)
        
        # Calculate current speed and direction
        speed = math.sqrt(self.velocity_x**2 + self.velocity_y**2)
        
        if speed > 0.1:
            # Try to slide along the wall instead of stopping
            # Calculate wall normal by checking surrounding pixels
            wall_normal_x, wall_normal_y = self._calculate_wall_normal(collision_result['wall_points'], track)
            
            # Reflect velocity off the wall normal (with energy loss)
            dot_product = self.velocity_x * wall_normal_x + self.velocity_y * wall_normal_y
            
            # Only reflect if moving into the wall
            if dot_product < 0:
                reflection_factor = 0.3  # Partial reflection for more realistic feel
                self.velocity_x -= 2 * dot_product * wall_normal_x * reflection_factor
                self.velocity_y -= 2 * dot_product * wall_normal_y * reflection_factor
            
            # Move away from wall slightly
            safe_distance = 3.0
            back_x = wall_normal_x * safe_distance
            back_y = wall_normal_y * safe_distance
            
            # Try the backed-off position
            test_x = self.x + back_x
            test_y = self.y + back_y
            
            test_collision = self._check_collision(test_x, test_y, track)
            if not test_collision['collision']:
                self.x = test_x
                self.y = test_y
                return
        
        # If still colliding or moving very slowly, find nearest safe position
        current_collision = self._check_collision(self.x, self.y, track)
        if current_collision['collision'] or speed < 0.3:
            self._find_safe_position(track)
    
    def _calculate_wall_normal(self, wall_points: list, track) -> Tuple[float, float]:
        """
        Calculate the normal vector of the wall from collision points.
        
        Args:
            wall_points: List of collision points
            track: Track object for collision detection
            
        Returns:
            Tuple of normalized wall normal vector (nx, ny)
        """
        if not wall_points:
            return (0.0, -1.0)  # Default to upward normal
        
        # Sample points around the collision area to find wall direction
        normal_x = 0.0
        normal_y = 0.0
        
        for wall_x, wall_y in wall_points[:3]:  # Use first few collision points
            # Check 8 directions around the collision point
            for dx, dy in [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]:
                check_x = wall_x + dx * 2
                check_y = wall_y + dy * 2
                
                surface_color = track.check_collision(check_x, check_y)
                if surface_color != TRACK_COLORS['WALL']:
                    # This direction points away from the wall
                    normal_x += dx
                    normal_y += dy
        
        # Normalize the normal vector
        length = math.sqrt(normal_x**2 + normal_y**2)
        if length > 0:
            normal_x /= length
            normal_y /= length
        else:
            # Fallback: use direction from car center to first wall point
            if wall_points:
                wall_x, wall_y = wall_points[0]
                dx = self.x - wall_x
                dy = self.y - wall_y
                length = math.sqrt(dx**2 + dy**2)
                if length > 0:
                    normal_x = dx / length
                    normal_y = dy / length
                else:
                    normal_x, normal_y = 0.0, -1.0
            else:
                normal_x, normal_y = 0.0, -1.0
        
        return (normal_x, normal_y)
    
    def _find_safe_position(self, track) -> None:
        """
        Find the nearest safe position when stuck in a collision.
        
        Args:
            track: Track object for collision detection
        """
        # Search in expanding circles for a safe position
        for radius in range(5, 25, 2):
            for angle in range(0, 360, 15):
                angle_rad = math.radians(angle)
                test_x = self.x + math.cos(angle_rad) * radius
                test_y = self.y + math.sin(angle_rad) * radius
                
                # Check if this position is safe
                test_collision = self._check_collision(test_x, test_y, track)
                if not test_collision['collision']:
                    self.x = test_x
                    self.y = test_y
                    # Reduce velocity significantly when repositioned
                    self.velocity_x *= 0.3
                    self.velocity_y *= 0.3
                    return
        
        # If no safe position found nearby, reset to start
        print(f"Car stuck in collision, resetting to start position")
        self._reset_to_start()
    
    def _reset_to_start(self) -> None:
        """Reset the car to its starting position and stop movement."""
        self.x = self.start_x
        self.y = self.start_y
        self.velocity_x = 0.0
        self.velocity_y = 0.0
        self.angle = self.start_angle  # Restore starting orientation
        self.is_reversing = False
        print(f"Car reset to start position: ({self.start_x}, {self.start_y}) facing {self.start_angle}°")
    
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
        # Get the rect for the rotated surface and center it on the car's position
        rotated_rect = self.rotated_surface.get_rect()
        rotated_rect.center = (int(self.x), int(self.y))
        
        # Blit the rotated car to the screen
        screen.blit(self.rotated_surface, rotated_rect)
        
        # Show reverse indicator when reversing
        if self.is_reversing:
            # Draw small white circles as reverse lights
            angle_rad = math.radians(self.angle)
            # Calculate back of car position
            back_distance = self.size[0] // 2 - 2
            back_x = self.x - math.cos(angle_rad) * back_distance
            back_y = self.y - math.sin(angle_rad) * back_distance
            
            # Draw two small reverse lights
            side_offset = self.size[1] // 4
            side_x = -math.sin(angle_rad) * side_offset
            side_y = math.cos(angle_rad) * side_offset
            
            pygame.draw.circle(screen, COLORS['WHITE'], 
                             (int(back_x + side_x), int(back_y + side_y)), 2)
            pygame.draw.circle(screen, COLORS['WHITE'], 
                             (int(back_x - side_x), int(back_y - side_y)), 2)
        
        # Optional: Draw collision points for debugging
        # for point in self._get_collision_points_world():
        #     pygame.draw.circle(screen, COLORS['YELLOW'], point, 2)
