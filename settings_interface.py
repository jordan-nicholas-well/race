"""
CLI Settings Interface for real-time game adjustment.

This module provides a console-based interface for adjusting game settings
while the game is running using arrow keys.
"""

import threading
import time
import sys
import select
import termios
import tty
from typing import Dict, Any, List, Callable
from game_settings import game_settings


class SettingsInterface:
    """
    Console-based settings interface with arrow key navigation.
    """
    
    def __init__(self) -> None:
        """Initialize the settings interface."""
        self.running: bool = False
        self.current_selection: int = 0
        self.cars: List[Any] = []  # Will be set by the main game
        
        # Settings configuration with realistic friction values
        self.settings: List[Dict[str, Any]] = [
            {
                'name': 'P1 Acceleration',
                'current_value': lambda: self.cars[0].acceleration if self.cars else 0.3,
                'adjust': lambda delta: self._adjust_car_setting(0, 'acceleration', delta),
                'min_value': 0.1,
                'max_value': 1.0,
                'increment': 0.05,
            },
            {
                'name': 'P1 Max Speed',
                'current_value': lambda: self.cars[0].max_speed if self.cars else 8.0,
                'adjust': lambda delta: self._adjust_car_setting(0, 'max_speed', delta),
                'min_value': 2.0,
                'max_value': 15.0,
                'increment': 0.5,
            },
            {
                'name': 'P1 Turn Speed',
                'current_value': lambda: self.cars[0].turn_speed if self.cars else 4.0,
                'adjust': lambda delta: self._adjust_car_setting(0, 'turn_speed', delta),
                'min_value': 1.0,
                'max_value': 8.0,
                'increment': 0.2,
            },
            {
                'name': 'P1 Friction',
                'current_value': lambda: self._get_friction_display(0),
                'adjust': lambda delta: self._adjust_car_friction(0, delta),
                'min_value': 0.01,
                'max_value': 0.20,
                'increment': 0.01,
            },
            {
                'name': 'P2 Acceleration',
                'current_value': lambda: self.cars[1].acceleration if len(self.cars) > 1 else 0.2,
                'adjust': lambda delta: self._adjust_car_setting(1, 'acceleration', delta),
                'min_value': 0.1,
                'max_value': 1.0,
                'increment': 0.05,
            },
            {
                'name': 'P2 Max Speed',
                'current_value': lambda: self.cars[1].max_speed if len(self.cars) > 1 else 6.0,
                'adjust': lambda delta: self._adjust_car_setting(1, 'max_speed', delta),
                'min_value': 2.0,
                'max_value': 15.0,
                'increment': 0.5,
            },
            {
                'name': 'P2 Turn Speed',
                'current_value': lambda: self.cars[1].turn_speed if len(self.cars) > 1 else 2.5,
                'adjust': lambda delta: self._adjust_car_setting(1, 'turn_speed', delta),
                'min_value': 1.0,
                'max_value': 8.0,
                'increment': 0.2,
            },
            {
                'name': 'P2 Friction',
                'current_value': lambda: self._get_friction_display(1),
                'adjust': lambda delta: self._adjust_car_friction(1, delta),
                'min_value': 0.01,
                'max_value': 0.20,
                'increment': 0.01,
            },
            {
                'name': 'Wall Stickiness',
                'current_value': lambda: game_settings.wall_stickiness,
                'adjust': lambda delta: self._adjust_global_setting('wall_stickiness', delta),
                'min_value': 0.0,
                'max_value': 1.0,
                'increment': 0.1,
            },
        ]
        
        # Store friction display values (realistic physics)
        self.friction_display = [0.05, 0.07]  # P1: 0.05 (sporty), P2: 0.07 (stable)
        
        # Terminal settings for raw input
        self.old_settings = None
        
    def set_cars(self, cars: List[Any]) -> None:
        """
        Set the car objects for adjustment.
        
        Args:
            cars: List of car objects from the main game
        """
        self.cars = cars
    
    def start(self) -> None:
        """Start the settings interface in a separate thread."""
        self.running = True
        self.interface_thread = threading.Thread(target=self._run_interface, daemon=True)
        self.interface_thread.start()
    
    def stop(self) -> None:
        """Stop the settings interface."""
        self.running = False
        if self.old_settings:
            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, self.old_settings)
    
    def _setup_terminal(self) -> None:
        """Setup terminal for raw input."""
        self.old_settings = termios.tcgetattr(sys.stdin)
        tty.setraw(sys.stdin.fileno())
    
    def _restore_terminal(self) -> None:
        """Restore terminal settings."""
        if self.old_settings:
            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, self.old_settings)
    
    def _get_key(self) -> str:
        """Get a single keypress from stdin."""
        try:
            if select.select([sys.stdin], [], [], 0.1) == ([sys.stdin], [], []):
                key = sys.stdin.read(1)
                if key == '\x1b':  # ESC sequence
                    key += sys.stdin.read(2)
                return key
        except:
            pass
        return ''
    
    def _get_friction_display(self, car_index: int) -> float:
        """
        Get the friction display value (realistic physics).
        
        Args:
            car_index: Index of the car (0 or 1)
            
        Returns:
            Friction display value (0.01-0.20 range)
        """
        if car_index < len(self.friction_display):
            return self.friction_display[car_index]
        return 0.05 if car_index == 0 else 0.07
    
    def _adjust_car_friction(self, car_index: int, delta: float) -> None:
        """
        Adjust a car's friction setting with realistic physics.
        
        Args:
            car_index: Index of the car (0 or 1)
            delta: Amount to adjust by
        """
        # Ensure friction_display has enough elements
        while len(self.friction_display) <= car_index:
            self.friction_display.append(0.05)
        
        # Get friction setting configuration
        friction_config = None
        for config in self.settings:
            if ((car_index == 0 and config['name'] == 'P1 Friction') or
                (car_index == 1 and config['name'] == 'P2 Friction')):
                friction_config = config
                break
        
        if friction_config:
            # Update display value
            current_value = self.friction_display[car_index]
            new_value = current_value + delta
            new_value = max(friction_config['min_value'], 
                          min(friction_config['max_value'], new_value))
            self.friction_display[car_index] = new_value
            
            # Convert to car friction (lower friction value = higher velocity retention)
            car_friction = 1.0 - new_value
            
            # Apply to car
            if car_index < len(self.cars):
                car = self.cars[car_index]
                setattr(car, 'friction', car_friction)
    
    def _adjust_car_setting(self, car_index: int, setting: str, delta: float) -> None:
        """
        Adjust a car setting.
        
        Args:
            car_index: Index of the car (0 or 1)
            setting: Name of the setting to adjust
            delta: Amount to adjust by
        """
        if car_index < len(self.cars):
            car = self.cars[car_index]
            current_value = getattr(car, setting)
            new_value = current_value + delta
            
            # Apply bounds based on setting configuration
            setting_config = None
            for config in self.settings:
                if ((car_index == 0 and config['name'].startswith('P1') and setting in config['name'].lower()) or
                    (car_index == 1 and config['name'].startswith('P2') and setting in config['name'].lower())):
                    if setting.replace('_', ' ').lower() in config['name'].lower():
                        setting_config = config
                        break
            
            if setting_config:
                new_value = max(setting_config['min_value'], 
                              min(setting_config['max_value'], new_value))
            
            setattr(car, setting, new_value)
            
            # Also update current_max_speed if max_speed changed
            if setting == 'max_speed':
                car.current_max_speed = new_value
    
    def _adjust_global_setting(self, setting: str, delta: float) -> None:
        """
        Adjust a global setting.
        
        Args:
            setting: Name of the setting to adjust
            delta: Amount to adjust by
        """
        if setting == 'wall_stickiness':
            current_value = game_settings.wall_stickiness
            new_value = max(0.0, min(1.0, current_value + delta))
            game_settings.wall_stickiness = new_value
    
    def _clear_screen(self) -> None:
        """Clear the console screen."""
        print('\033[2J\033[H', end='', flush=True)
    
    def _display_interface(self) -> None:
        """Display the settings interface with proper formatting."""
        self._clear_screen()
        
        # Header with proper carriage returns
        print("\r🎮 RACING GAME - SETTINGS INTERFACE")
        print("\r" + "=" * 60)
        print("\rNavigation: ↑/↓ select, ←/→ adjust, 'q' quit")
        print("\r")
        
        for i, setting in enumerate(self.settings):
            # Selection indicator
            indicator = "→ " if i == self.current_selection else "  "
            
            # Get current value
            try:
                current_val = setting['current_value']()
                if setting['name'] in ['P1 Friction', 'P2 Friction']:
                    value_str = f"{current_val:.3f}"
                else:
                    value_str = f"{current_val:.2f}"
            except:
                value_str = "N/A"
            
            # Display range
            if setting['name'] in ['P1 Friction', 'P2 Friction']:
                range_str = f"[{setting['min_value']:.2f}-{setting['max_value']:.2f}]"
            else:
                range_str = f"[{setting['min_value']:.1f}-{setting['max_value']:.1f}]"
            
            # Format line with proper alignment and carriage return
            name_field = f"{setting['name']:<16}"
            value_field = f"{value_str:>6}"
            
            # Color coding for selected item
            if i == self.current_selection:
                line = f"\r{indicator}\033[93m{name_field}\033[0m: \033[92m{value_field}\033[0m {range_str}"
            else:
                line = f"\r{indicator}{name_field}: {value_field} {range_str}"
            
            print(line)
        
        print("\r")
        print("\r" + "=" * 60)
        print("\rGame: WASD (P1), Arrows (P2) | Changes apply instantly!")
    
    def _run_interface(self) -> None:
        """Main interface loop."""
        try:
            self._setup_terminal()
            
            while self.running:
                self._display_interface()
                
                key = self._get_key()
                
                if key == 'q' or key == '\x03':  # 'q' or Ctrl+C
                    break
                elif key == '\x1b[A':  # Up arrow
                    self.current_selection = (self.current_selection - 1) % len(self.settings)
                elif key == '\x1b[B':  # Down arrow
                    self.current_selection = (self.current_selection + 1) % len(self.settings)
                elif key == '\x1b[D':  # Left arrow (decrease)
                    setting = self.settings[self.current_selection]
                    setting['adjust'](-setting['increment'])
                elif key == '\x1b[C':  # Right arrow (increase)
                    setting = self.settings[self.current_selection]
                    setting['adjust'](setting['increment'])
                
                time.sleep(0.05)  # Small delay to prevent excessive CPU usage
                
        except KeyboardInterrupt:
            pass
        finally:
            self._restore_terminal()
            self.running = False
    
    def is_running(self) -> bool:
        """Check if the interface is running."""
        return self.running


# Global instance
settings_interface = SettingsInterface()
