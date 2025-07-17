import asyncio
import pygame

# Initialize pygame immediately at module load
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Racing Game")
clock = pygame.time.Clock()

# Simple game state
car1_x, car1_y = 200, 250
car2_x, car2_y = 200, 350
running = True

async def main():
    global car1_x, car1_y, car2_x, car2_y, running
    
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        # Handle input
        keys = pygame.key.get_pressed()
        
        # Player 1 (WASD)
        if keys[pygame.K_w]:
            car1_y -= 3
        if keys[pygame.K_s]:
            car1_y += 3
        if keys[pygame.K_a]:
            car1_x -= 3
        if keys[pygame.K_d]:
            car1_x += 3
        
        # Player 2 (Arrows)
        if keys[pygame.K_UP]:
            car2_y -= 3
        if keys[pygame.K_DOWN]:
            car2_y += 3
        if keys[pygame.K_LEFT]:
            car2_x -= 3
        if keys[pygame.K_RIGHT]:
            car2_x += 3
        
        # Keep cars on screen
        car1_x = max(20, min(WIDTH-20, car1_x))
        car1_y = max(20, min(HEIGHT-20, car1_y))
        car2_x = max(20, min(WIDTH-20, car2_x))
        car2_y = max(20, min(HEIGHT-20, car2_y))
        
        # Render
        screen.fill((0, 100, 0))  # Green background
        
        # Draw track
        pygame.draw.rect(screen, (255, 255, 255), (50, 50, WIDTH-100, HEIGHT-100), 5)
        pygame.draw.rect(screen, (255, 255, 255), (100, 100, WIDTH-200, HEIGHT-200), 5)
        
        # Draw cars
        pygame.draw.circle(screen, (255, 0, 0), (car1_x, car1_y), 15)  # Red car
        pygame.draw.circle(screen, (0, 0, 255), (car2_x, car2_y), 15)  # Blue car
        
        # Draw instructions
        font = pygame.font.Font(None, 24)
        text1 = font.render("Player 1 (Red): WASD", True, (255, 255, 255))
        text2 = font.render("Player 2 (Blue): Arrow Keys", True, (255, 255, 255))
        screen.blit(text1, (10, 10))
        screen.blit(text2, (10, 35))
        
        pygame.display.flip()
        clock.tick(60)
        
        # Critical for Pygbag
        await asyncio.sleep(0)

# Pygbag expects this exact pattern
if __name__ == "__main__":
    asyncio.run(main())
