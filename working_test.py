import asyncio
import pygame

# Initialize outside of any function
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Racing Test")
clock = pygame.time.Clock()

# Game state variables
running = True
player_x = 400
player_y = 300
frame_count = 0

async def main():
    global running, player_x, player_y, frame_count
    
    # Print to see if main function is called
    print("🎮 Main function started!")
    
    while running:
        frame_count += 1
        
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        # Get keys
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player_x -= 3
        if keys[pygame.K_RIGHT]:
            player_x += 3
        if keys[pygame.K_UP]:
            player_y -= 3
        if keys[pygame.K_DOWN]:
            player_y += 3
        
        # Keep player on screen
        player_x = max(25, min(775, player_x))
        player_y = max(25, min(575, player_y))
        
        # Render
        screen.fill((0, 50, 100))  # Dark blue background
        
        # Draw player as yellow circle
        pygame.draw.circle(screen, (255, 255, 0), (int(player_x), int(player_y)), 20)
        
        # Draw simple UI
        font = pygame.font.Font(None, 36)
        text = f"Frame: {frame_count}"
        text_surface = font.render(text, True, (255, 255, 255))
        screen.blit(text_surface, (10, 10))
        
        instructions = font.render("Use arrow keys to move", True, (255, 255, 255))
        screen.blit(instructions, (10, 50))
        
        # Update display
        pygame.display.flip()
        clock.tick(60)
        
        # Critical: yield control
        await asyncio.sleep(0)
    
    pygame.quit()

# Start the game - this is the critical pattern for Pygbag
asyncio.run(main())
