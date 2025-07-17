#!/usr/bin/env python3
"""
Working racing game for Pygbag - final attempt with proper startup sequence.
"""

import asyncio
import pygame
import sys

# Import racing game components with fallbacks
try:
    from settings import *
    from car import Car
    from track import Track
    from controls import PLAYER1_CONTROLS, PLAYER2_CONTROLS
    GAME_IMPORTS_OK = True
except ImportError as e:
    print(f"Import error: {e}")
    # Fallback constants
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600
    FPS = 60
    COLORS = {
        'BLACK': (0, 0, 0),
        'WHITE': (255, 255, 255),
        'RED': (255, 0, 0),
        'BLUE': (0, 0, 255),
        'YELLOW': (255, 255, 0),
        'GREEN': (0, 255, 0)
    }
    GAME_IMPORTS_OK = False

# Initialize pygame immediately
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Racing Game Web")
clock = pygame.time.Clock()

# Game state
running = True
game_started = False
error_message = ""

# Simple fallback game
player1_x, player1_y = 200, 250
player2_x, player2_y = 200, 350

async def main():
    """Main game loop."""
    global running, game_started, error_message
    global player1_x, player1_y, player2_x, player2_y
    
    print("🎮 Racing game main() called!")
    
    if GAME_IMPORTS_OK:
        print("✅ All game modules imported successfully")
        try:
            # Initialize full racing game
            track = Track()
            if not track.load_track():
                print("⚠️ Using fallback track")
            
            # Get starting positions
            start_positions = track.get_start_positions()
            if len(start_positions) >= 2:
                car1_pos = start_positions[0]
                car2_pos = start_positions[1]
            else:
                car1_pos = (SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2)
                car2_pos = (SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2 + 50)
            
            # Create cars
            car1 = Car(car1_pos, SPORTS_CAR)
            car1.angle = 270.0
            car2 = Car(car2_pos, TRUCK)
            car2.angle = 270.0
            
            game_started = True
            print("✅ Full racing game initialized")
            
        except Exception as e:
            print(f"❌ Failed to initialize full game: {e}")
            error_message = f"Game init error: {e}"
            GAME_IMPORTS_OK = False
    
    frame_count = 0
    
    while running:
        frame_count += 1
        
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
        
        # Get keys
        keys = pygame.key.get_pressed()
        
        # Clear screen
        screen.fill(COLORS['BLACK'])
        
        if GAME_IMPORTS_OK and game_started:
            # Full racing game
            try:
                car1.update(keys, PLAYER1_CONTROLS, track)
                car2.update(keys, PLAYER2_CONTROLS, track)
                
                track.render(screen)
                car1.render(screen)
                car2.render(screen)
                
                # UI
                font = pygame.font.Font(None, 24)
                instructions = [
                    "Player 1: WASD",
                    "Player 2: Arrow Keys",
                    f"Frame: {frame_count}"
                ]
                for i, text in enumerate(instructions):
                    text_surface = font.render(text, True, COLORS['WHITE'])
                    screen.blit(text_surface, (10, 10 + i * 25))
                    
            except Exception as e:
                error_message = f"Runtime error: {e}"
                print(f"❌ Runtime error: {e}")
        else:
            # Fallback simple game
            # Simple controls
            if keys[pygame.K_w] or keys[pygame.K_UP]:
                player1_y -= 3
                player2_y -= 3
            if keys[pygame.K_s] or keys[pygame.K_DOWN]:
                player1_y += 3
                player2_y += 3
            if keys[pygame.K_a] or keys[pygame.K_LEFT]:
                player1_x -= 3
                player2_x -= 3
            if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
                player1_x += 3
                player2_x += 3
            
            # Keep on screen
            player1_x = max(20, min(SCREEN_WIDTH - 20, player1_x))
            player1_y = max(20, min(SCREEN_HEIGHT - 20, player1_y))
            player2_x = max(20, min(SCREEN_WIDTH - 20, player2_x))
            player2_y = max(20, min(SCREEN_HEIGHT - 20, player2_y))
            
            # Draw simple track
            pygame.draw.rect(screen, COLORS['WHITE'], (50, 50, SCREEN_WIDTH - 100, SCREEN_HEIGHT - 100), 3)
            pygame.draw.rect(screen, COLORS['WHITE'], (100, 100, SCREEN_WIDTH - 200, SCREEN_HEIGHT - 200), 3)
            
            # Draw simple cars
            pygame.draw.rect(screen, COLORS['RED'], (player1_x - 10, player1_y - 15, 20, 30))
            pygame.draw.rect(screen, COLORS['BLUE'], (player2_x - 10, player2_y - 15, 20, 30))
            
            # Simple UI
            font = pygame.font.Font(None, 24)
            texts = [
                "🎮 RACING GAME (Fallback Mode)",
                "Player 1 (Red): WASD",
                "Player 2 (Blue): Arrow Keys",
                f"Frame: {frame_count}",
                f"Status: {'Game OK' if GAME_IMPORTS_OK else 'Fallback Mode'}",
            ]
            
            if error_message:
                texts.append(f"Error: {error_message}")
            
            for i, text in enumerate(texts):
                color = COLORS['YELLOW'] if i == 0 else COLORS['WHITE']
                if "Error:" in text:
                    color = COLORS['RED']
                text_surface = font.render(text, True, color)
                screen.blit(text_surface, (10, 10 + i * 25))
        
        # Update display
        pygame.display.flip()
        clock.tick(FPS)
        
        # Critical yield
        await asyncio.sleep(0)
    
    print("🏁 Racing game ended")
    pygame.quit()

# Direct call - no if __name__ check
print("🚀 Starting Pygbag game...")
asyncio.run(main())
