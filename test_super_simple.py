import asyncio
import pygame

print("Starting pygame...")
pygame.init()

screen = pygame.display.set_mode((400, 300))
pygame.display.set_caption("Test")

print("Pygame initialized!")

async def main():
    print("Main function started!")
    
    running = True
    frame = 0
    
    while running:
        frame += 1
        if frame % 60 == 0:
            print(f"Frame {frame}")
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        screen.fill((255, 0, 0))  # Red background
        pygame.display.flip()
        
        await asyncio.sleep(0)  # Essential for Pygbag
    
    print("Main function ended!")
    pygame.quit()

if __name__ == "__main__":
    print("Running asyncio.run(main())")
    asyncio.run(main())
