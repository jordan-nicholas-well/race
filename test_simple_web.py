#!/usr/bin/env python3
"""
Super simple web test to identify the issue.
"""

import asyncio
import pygame
import sys

print("🚀 Simple web test starting...")

# Simple constants to avoid import issues
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
COLORS = {
    'BLACK': (0, 0, 0),
    'WHITE': (255, 255, 255),
    'RED': (255, 0, 0),
    'GREEN': (0, 255, 0),
    'BLUE': (0, 0, 255)
}

class SimpleGame:
    def __init__(self):
        print("🎮 Initializing simple game...")
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Simple Web Test")
        self.clock = pygame.time.Clock()
        self.running = True
        self.frame_count = 0
        print("✅ Simple game initialized")

    async def run(self):
        print("🔄 Starting simple game loop...")
        
        while self.running:
            self.frame_count += 1
            
            # Debug every 60 frames
            if self.frame_count % 60 == 0:
                print(f"🔄 Frame {self.frame_count}")
            
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    print("🚪 Quit event")
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        print("🚪 Escape pressed")
                        self.running = False
                    else:
                        print(f"⌨️ Key pressed: {event.key}")
            
            # Simple render
            self.screen.fill(COLORS['BLACK'])
            
            # Draw a simple colored rectangle that changes
            color_index = (self.frame_count // 60) % 3
            colors = [COLORS['RED'], COLORS['GREEN'], COLORS['BLUE']]
            color = colors[color_index]
            
            pygame.draw.rect(self.screen, color, (100, 100, 200, 100))
            
            # Draw text
            font = pygame.font.Font(None, 36)
            text = f"Frame {self.frame_count}"
            text_surface = font.render(text, True, COLORS['WHITE'])
            self.screen.blit(text_surface, (50, 50))
            
            text2 = "Press ESC to exit, any key to test input"
            text2_surface = font.render(text2, True, COLORS['WHITE'])
            self.screen.blit(text2_surface, (50, 300))
            
            # Update display
            pygame.display.flip()
            self.clock.tick(60)
            
            # Yield for web
            await asyncio.sleep(0)
        
        print("🏁 Simple game loop ended")

async def main():
    print("🌟 Main function starting...")
    
    try:
        game = SimpleGame()
        await game.run()
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        pygame.quit()
        print("🔚 Pygame quit")

if __name__ == "__main__":
    print("🎯 Script started")
    asyncio.run(main())
