#!/usr/bin/env python3
"""
Minimal test version to check if Pygbag is working.
"""

import asyncio
import pygame

async def main():
    """Simple test game to verify Pygbag is working."""
    print("🎮 Starting minimal test game...")
    
    # Initialize Pygame
    pygame.init()
    
    # Create display
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Test Game - Working!")
    
    # Colors
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    WHITE = (255, 255, 255)
    
    clock = pygame.time.Clock()
    running = True
    
    x, y = 400, 300
    dx, dy = 2, 3
    
    print("🌐 Game loop starting...")
    
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        # Update
        x += dx
        y += dy
        
        # Bounce off edges
        if x <= 0 or x >= 800:
            dx = -dx
        if y <= 0 or y >= 600:
            dy = -dy
        
        # Draw
        screen.fill(WHITE)
        pygame.draw.circle(screen, RED, (int(x), int(y)), 20)
        pygame.draw.rect(screen, GREEN, (10, 10, 100, 50))
        
        # Draw text
        font = pygame.font.Font(None, 36)
        text = font.render("TEST GAME WORKING!", True, BLUE)
        screen.blit(text, (200, 100))
        
        pygame.display.flip()
        await asyncio.sleep(0.01)  # Essential for web compatibility
        clock.tick(60)
    
    pygame.quit()
    print("🛑 Test game ended")

if __name__ == "__main__":
    asyncio.run(main())
