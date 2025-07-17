"""
Web-compatible GUI settings interface using Pygame UI elements.

This module provides a GUI-based settings interface that works in web browsers,
replacing the terminal-based interface which is not compatible with Pygbag.
"""

import pygame
import asyncio
from typing import Dict, Any, Tuple, Optional
from game_settings import game_settings

# GUI Constants
GUI_WIDTH = 400
GUI_HEIGHT = 500
PANEL_COLOR = (40, 40, 40, 220)  # Semi-transparent dark panel
BORDER_COLOR = (100, 100, 100)
TEXT_COLOR = (255, 255, 255)
HIGHLIGHT_COLOR = (255, 255, 0)
VALUE_COLOR = (0, 255, 255)
BUTTON_COLOR = (60, 60, 60)
BUTTON_HOVER_COLOR = (80, 80, 80)
BUTTON_ACTIVE_COLOR = (100, 100, 100)

class WebSettingsInterface:
    """
    GUI-based settings interface for web deployment.
    
    Provides real-time adjustment of game settings using Pygame UI elements
    that are compatible with web browsers via Pygbag.
    """
    
    def __init__(self, screen: pygame.Surface) -> None:
        """
        Initialize the web settings interface.
        
        Args:
            screen: The main pygame screen surface
        """
        self.screen = screen
        self.font = pygame.font.Font(None, 24)
        self.title_font = pygame.font.Font(None, 32)
        self.small_font = pygame.font.Font(None, 20)
        
        # Interface state
        self.visible = False
        self.selected_setting = 0
        self.settings_list = [
            'car1_acceleration',
            'car1_max_speed', 
            'car1_friction',
            'car1_turn_speed',
            'car2_acceleration',
            'car2_max_speed',
            'car2_friction', 
            'car2_turn_speed'
        ]
        
        # Button tracking
        self.buttons: Dict[str, pygame.Rect] = {}
        self.mouse_over_button: Optional[str] = None
        self.button_pressed: Optional[str] = None
        
        # Create the GUI panel surface
        self.panel_surface = pygame.Surface((GUI_WIDTH, GUI_HEIGHT), pygame.SRCALPHA)
        
        # Position the panel (centered on screen)
        screen_width, screen_height = screen.get_size()
        self.panel_x = (screen_width - GUI_WIDTH) // 2
        self.panel_y = (screen_height - GUI_HEIGHT) // 2
        
    def toggle_visibility(self) -> None:
        """Toggle the visibility of the settings interface."""
        self.visible = not self.visible
        
    def is_visible(self) -> bool:
        """Check if the settings interface is currently visible."""
        return self.visible
        
    def handle_event(self, event: pygame.event.Event) -> bool:
        """
        Handle pygame events for the settings interface.
        
        Args:
            event: Pygame event to handle
            
        Returns:
            True if event was handled, False otherwise
        """
        if not self.visible:
            return False
            
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.visible = False
                return True
            elif event.key == pygame.K_UP:
                self.selected_setting = (self.selected_setting - 1) % len(self.settings_list)
                return True
            elif event.key == pygame.K_DOWN:
                self.selected_setting = (self.selected_setting + 1) % len(self.settings_list)
                return True
            elif event.key == pygame.K_LEFT:
                self._adjust_setting(-1)
                return True
            elif event.key == pygame.K_RIGHT:
                self._adjust_setting(1)
                return True
                
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left click
                mouse_x, mouse_y = event.pos
                # Convert to panel-relative coordinates
                rel_x = mouse_x - self.panel_x
                rel_y = mouse_y - self.panel_y
                
                # Check if click is within panel
                if 0 <= rel_x <= GUI_WIDTH and 0 <= rel_y <= GUI_HEIGHT:
                    # Check button clicks
                    for button_name, button_rect in self.buttons.items():
                        if button_rect.collidepoint(rel_x, rel_y):
                            self.button_pressed = button_name
                            self._handle_button_click(button_name)
                            return True
                    return True
                else:
                    # Click outside panel - close interface
                    self.visible = False
                    return True
                    
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                self.button_pressed = None
                
        elif event.type == pygame.MOUSEMOTION:
            if self.visible:
                mouse_x, mouse_y = event.pos
                rel_x = mouse_x - self.panel_x
                rel_y = mouse_y - self.panel_y
                
                # Update hover state
                self.mouse_over_button = None
                for button_name, button_rect in self.buttons.items():
                    if button_rect.collidepoint(rel_x, rel_y):
                        self.mouse_over_button = button_name
                        break
                        
        return False
        
    def _handle_button_click(self, button_name: str) -> None:
        """Handle clicking on a settings adjustment button."""
        if button_name.endswith('_inc'):
            setting_name = button_name[:-4]
            setting_index = self.settings_list.index(setting_name)
            self.selected_setting = setting_index
            self._adjust_setting(1)
        elif button_name.endswith('_dec'):
            setting_name = button_name[:-4]
            setting_index = self.settings_list.index(setting_name)
            self.selected_setting = setting_index
            self._adjust_setting(-1)
        elif button_name == 'close':
            self.visible = False
            
    def _adjust_setting(self, direction: int) -> None:
        """
        Adjust the currently selected setting.
        
        Args:
            direction: 1 for increase, -1 for decrease
        """
        setting_name = self.settings_list[self.selected_setting]
        current_value = getattr(game_settings, setting_name)
        
        # Determine adjustment amount based on setting type
        if 'friction' in setting_name:
            # Friction: 0.1 to 2.0 in steps of 0.1
            adjustment = 0.1 * direction
            new_value = max(0.1, min(2.0, current_value + adjustment))
        elif 'acceleration' in setting_name:
            # Acceleration: 0.1 to 3.0 in steps of 0.1
            adjustment = 0.1 * direction
            new_value = max(0.1, min(3.0, current_value + adjustment))
        elif 'max_speed' in setting_name:
            # Max speed: 1.0 to 20.0 in steps of 0.5
            adjustment = 0.5 * direction
            new_value = max(1.0, min(20.0, current_value + adjustment))
        elif 'turn_speed' in setting_name:
            # Turn speed: 0.5 to 10.0 in steps of 0.5
            adjustment = 0.5 * direction
            new_value = max(0.5, min(10.0, current_value + adjustment))
        else:
            return
            
        # Apply the new value
        setattr(game_settings, setting_name, new_value)
        
    def _get_setting_display_name(self, setting_name: str) -> str:
        """Get a user-friendly display name for a setting."""
        names = {
            'car1_acceleration': 'P1 Acceleration',
            'car1_max_speed': 'P1 Max Speed',
            'car1_friction': 'P1 Friction',
            'car1_turn_speed': 'P1 Turn Speed',
            'car2_acceleration': 'P2 Acceleration',
            'car2_max_speed': 'P2 Max Speed',
            'car2_friction': 'P2 Friction',
            'car2_turn_speed': 'P2 Turn Speed',
        }
        return names.get(setting_name, setting_name)
        
    def _draw_button(self, surface: pygame.Surface, rect: pygame.Rect, 
                    text: str, button_name: str) -> None:
        """Draw a button with hover and press states."""
        # Determine button color based on state
        color = BUTTON_COLOR
        if self.button_pressed == button_name:
            color = BUTTON_ACTIVE_COLOR
        elif self.mouse_over_button == button_name:
            color = BUTTON_HOVER_COLOR
            
        # Draw button
        pygame.draw.rect(surface, color, rect)
        pygame.draw.rect(surface, BORDER_COLOR, rect, 2)
        
        # Draw button text
        text_surface = self.small_font.render(text, True, TEXT_COLOR)
        text_rect = text_surface.get_rect(center=rect.center)
        surface.blit(text_surface, text_rect)
        
    def render(self) -> None:
        """Render the settings interface if visible."""
        if not self.visible:
            return
            
        # Clear the panel surface
        self.panel_surface.fill(PANEL_COLOR)
        
        # Draw border
        pygame.draw.rect(self.panel_surface, BORDER_COLOR, 
                        (0, 0, GUI_WIDTH, GUI_HEIGHT), 3)
        
        # Clear buttons dict for this frame
        self.buttons.clear()
        
        # Draw title
        title_text = "Game Settings"
        title_surface = self.title_font.render(title_text, True, HIGHLIGHT_COLOR)
        title_rect = title_surface.get_rect(centerx=GUI_WIDTH // 2, y=20)
        self.panel_surface.blit(title_surface, title_rect)
        
        # Draw instructions
        instructions = [
            "Use arrow keys or mouse to adjust",
            "ESC to close, click outside to close"
        ]
        y_offset = 60
        for instruction in instructions:
            inst_surface = self.small_font.render(instruction, True, TEXT_COLOR)
            inst_rect = inst_surface.get_rect(centerx=GUI_WIDTH // 2, y=y_offset)
            self.panel_surface.blit(inst_surface, inst_rect)
            y_offset += 25
            
        # Draw settings
        start_y = 120
        for i, setting_name in enumerate(self.settings_list):
            y_pos = start_y + i * 40
            
            # Highlight selected setting
            if i == self.selected_setting:
                highlight_rect = pygame.Rect(10, y_pos - 5, GUI_WIDTH - 20, 35)
                pygame.draw.rect(self.panel_surface, (60, 60, 60), highlight_rect)
                pygame.draw.rect(self.panel_surface, HIGHLIGHT_COLOR, highlight_rect, 2)
            
            # Setting name
            display_name = self._get_setting_display_name(setting_name)
            name_surface = self.font.render(display_name, True, TEXT_COLOR)
            self.panel_surface.blit(name_surface, (20, y_pos))
            
            # Current value
            current_value = getattr(game_settings, setting_name)
            value_text = f"{current_value:.1f}"
            value_surface = self.font.render(value_text, True, VALUE_COLOR)
            self.panel_surface.blit(value_surface, (200, y_pos))
            
            # Decrease button
            dec_rect = pygame.Rect(270, y_pos, 30, 25)
            self.buttons[f"{setting_name}_dec"] = dec_rect
            self._draw_button(self.panel_surface, dec_rect, "-", f"{setting_name}_dec")
            
            # Increase button
            inc_rect = pygame.Rect(310, y_pos, 30, 25)
            self.buttons[f"{setting_name}_inc"] = inc_rect
            self._draw_button(self.panel_surface, inc_rect, "+", f"{setting_name}_inc")
            
        # Close button
        close_rect = pygame.Rect(GUI_WIDTH - 80, 10, 60, 30)
        self.buttons["close"] = close_rect
        self._draw_button(self.panel_surface, close_rect, "Close", "close")
        
        # Blit the panel to the main screen
        self.screen.blit(self.panel_surface, (self.panel_x, self.panel_y))
