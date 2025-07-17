#!/usr/bin/env python3
"""
Minimal racing game for Pygbag web deployment.
"""

import asyncio
import pygame
import sys

# Initialize pygame first
pygame.init()

# Basic constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

# Create display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Racing Game - Web Version")
clock = pygame.time.Clock()

# Game state
running = True
frame_count = 0

# Simple car positions
car1_x, car1_y = 200, 300
car2_x, car2_y = 200, 350

async def main():
    """Main game loop - Pygbag compatible."""
    global running, frame_count, car1_x, car1_y, car2_x, car2_y
    
    print("🎮 Starting racing game...")
    
    while running:
        frame_count += 1
        
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                    
        # Get pressed keys
        keys = pygame.key.get_pressed()
        
        # Player 1 controls (WASD)
        if keys[pygame.K_w]:
            car1_y -= 2
        if keys[pygame.K_s]:
            car1_y += 2
        if keys[pygame.K_a]:
            car1_x -= 2
        if keys[pygame.K_d]:
            car1_x += 2
            
        # Player 2 controls (Arrow keys)
        if keys[pygame.K_UP]:
            car2_y -= 2
        if keys[pygame.K_DOWN]:
            car2_y += 2
        if keys[pygame.K_LEFT]:
            car2_x -= 2
        if keys[pygame.K_RIGHT]:
            car2_x += 2
            
        # Keep cars on screen
        car1_x = max(20, min(SCREEN_WIDTH - 20, car1_x))
        car1_y = max(20, min(SCREEN_HEIGHT - 20, car1_y))
        car2_x = max(20, min(SCREEN_WIDTH - 20, car2_x))
        car2_y = max(20, min(SCREEN_HEIGHT - 20, car2_y))
        
        # Clear screen
        screen.fill(BLACK)
        
        # Draw simple track
        pygame.draw.rect(screen, WHITE, (50, 50, SCREEN_WIDTH - 100, SCREEN_HEIGHT - 100), 3)
        pygame.draw.rect(screen, WHITE, (100, 100, SCREEN_WIDTH - 200, SCREEN_HEIGHT - 200), 3)
        
        # Draw cars as simple rectangles
        pygame.draw.rect(screen, RED, (car1_x - 10, car1_y - 15, 20, 30))
        pygame.draw.rect(screen, BLUE, (car2_x - 10, car2_y - 15, 20, 30))
        
        # Draw instructions
        font = pygame.font.Font(None, 24)
        instructions = [
            "Player 1 (Red): WASD",
            "Player 2 (Blue): Arrow Keys",
            "ESC to exit"
        ]
        
        for i, text in enumerate(instructions):
            text_surface = font.render(text, True, WHITE)
            screen.blit(text_surface, (10, 10 + i * 25))
        
        # Show frame count
        frame_text = f"Frame: {frame_count}"
        frame_surface = font.render(frame_text, True, GREEN)
        screen.blit(frame_surface, (SCREEN_WIDTH - 120, 10))
        
        # Update display
        pygame.display.flip()
        clock.tick(60)
        
        # CRITICAL: Yield control to browser
        await asyncio.sleep(0)
    
    # Cleanup
    pygame.quit()
    print("🏁 Game ended")

# Run the game
if __name__ == "__main__":
    asyncio.run(main())
