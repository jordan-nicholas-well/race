#!/usr/bin/env python3
"""
Web-compatible main entry point for the racing game.
Debug version with extensive logging.
"""

import asyncio
import pygame
import sys
import math

print("🚀 Starting debug web version...")

try:
    # Import game modules
    from settings import *
    print("✅ Settings imported")
    
    from car import Car
    print("✅ Car imported")
    
    from track import Track
    print("✅ Track imported")
    
    from game_settings import game_settings
    print("✅ Game settings imported")
    
    from controls import PLAYER1_CONTROLS, PLAYER2_CONTROLS
    print("✅ Controls imported")
    
    try:
        from web_settings_interface import WebSettingsInterface
        print("✅ Web settings interface imported")
        WEB_SETTINGS_AVAILABLE = True
    except ImportError:
        print("⚠️ Web settings interface not available")
        WEB_SETTINGS_AVAILABLE = False

    print("📦 All imports successful!")

except Exception as e:
    print(f"❌ Import error: {e}")
    sys.exit(1)


class RacingGameWeb:
    """Web-compatible racing game class with debug output."""
    
    def __init__(self):
        """Initialize the web-compatible racing game."""
        print("🎮 Initializing racing game...")
        
        try:
            pygame.init()
            print("✅ Pygame initialized")
            
            # Create display
            self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
            pygame.display.set_caption(WINDOW_TITLE)
            self.clock = pygame.time.Clock()
            print(f"✅ Display created: {SCREEN_WIDTH}x{SCREEN_HEIGHT}")
            
            # Initialize game objects
            self.track = Track()
            print("✅ Track created")
            
            self.running = True
            
            # Load track
            if not self.track.load_track():
                print("⚠️ Using fallback track")
            else:
                print("✅ Track loaded successfully")
            
            # Get starting positions
            start_positions = self.track.get_start_positions()
            if len(start_positions) >= 2:
                player1_pos = start_positions[0]
                player2_pos = start_positions[1]
                print(f"✅ Start positions from track: P1={player1_pos}, P2={player2_pos}")
            else:
                # Fallback positions
                player1_pos = (SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2)
                player2_pos = (SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2 + 50)
                print(f"⚠️ Using fallback positions: P1={player1_pos}, P2={player2_pos}")
            
            # Create cars with proper starting angle (facing up = 270°)
            self.car1 = Car(player1_pos, SPORTS_CAR)
            self.car1.angle = 270.0  # Face up
            print("✅ Player 1 car created (Sports Car)")
            
            self.car2 = Car(player2_pos, TRUCK)
            self.car2.angle = 270.0  # Face up
            print("✅ Player 2 car created (Truck)")
            
            self.cars = [self.car1, self.car2]
            
            # Initialize web settings interface
            if WEB_SETTINGS_AVAILABLE:
                self.web_settings = WebSettingsInterface(self.screen)
                print("✅ Web settings interface initialized")
            else:
                self.web_settings = None
                print("⚠️ Web settings interface disabled")
            
            # Web-specific settings
            self.is_web = self._detect_web_environment()
            print(f"🌐 Web environment detected: {self.is_web}")
            
            print("🎯 Game initialization complete!")
            
        except Exception as e:
            print(f"❌ Initialization error: {e}")
            raise
        
    def _detect_web_environment(self) -> bool:
        """Detect if running in web browser via Pygbag."""
        try:
            # Pygbag sets this when running in browser
            import platform
            is_web = platform.system() == "Emscripten" or "emscripten" in sys.platform.lower()
            print(f"🔍 Platform: {platform.system()}, sys.platform: {sys.platform}")
            return is_web
        except Exception as e:
            print(f"⚠️ Web detection error: {e}")
            return False
    
    async def run(self):
        """Main game loop - async for web compatibility."""
        print("🎮 Starting main game loop...")
        
        frame_count = 0
        
        try:
            while self.running:
                frame_count += 1
                
                # Debug output every 60 frames (about once per second)
                if frame_count % 60 == 0:
                    print(f"🔄 Frame {frame_count} - Game running normally")
                
                # Handle events
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        print("🚪 Quit event received")
                        self.running = False
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            print("🚪 Escape key pressed")
                            self.running = False
                        elif event.key == pygame.K_TAB and self.web_settings:
                            print("⚙️ Tab pressed - toggling settings")
                            self.web_settings.toggle_visibility()
                        
                        # Pass event to settings interface
                        if self.web_settings:
                            self.web_settings.handle_event(event)
                
                # Get key states
                keys = pygame.key.get_pressed()
                
                # Update cars
                try:
                    self.car1.update(keys, PLAYER1_CONTROLS, self.track)
                    self.car2.update(keys, PLAYER2_CONTROLS, self.track)
                except Exception as e:
                    print(f"❌ Car update error: {e}")
                
                # Render everything
                try:
                    self._render()
                except Exception as e:
                    print(f"❌ Render error: {e}")
                
                # Update display
                try:
                    pygame.display.flip()
                    self.clock.tick(FPS)
                except Exception as e:
                    print(f"❌ Display update error: {e}")
                
                # Yield control for web compatibility
                if self.is_web:
                    await asyncio.sleep(0)
                    
        except Exception as e:
            print(f"❌ Main loop error: {e}")
            raise
        
        print("🏁 Game loop ended")
    
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
        if self.web_settings:
            self.web_settings.render()
    
    def _render_ui(self):
        """Render user interface elements."""
        font = pygame.font.Font(None, 24)
        
        # Instructions
        instructions = [
            "🎮 RACING GAME DEBUG VERSION",
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
    print("🌟 Starting main function...")
    
    try:
        game = RacingGameWeb()
        print("✅ Game instance created")
        
        await game.run()
        print("✅ Game run completed")
        
    except Exception as e:
        print(f"❌ Main function error: {e}")
        raise
    finally:
        pygame.quit()
        print("🔚 Pygame quit called")

if __name__ == "__main__":
    print("🎯 Script started directly")
    # Run with asyncio for web compatibility
    asyncio.run(main())
