import pygame


def main():
    pygame.init()
    pygame.display.set_caption("Flyer Fox")
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
    fps = 60
    scroll = 0
    scroll_speed = 4
    background = pygame.image.load("FF_Background.png")
    background_dummy = pygame.transform.scale(background, (1500, 700))
    foreground = pygame.image.load("FF_Foreground.jpg")
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
        
        screen.blit(background_dummy, (0, 0))
        for i in range(2):
            screen.blit(foreground, (i * 800 + scroll, 600))
        scroll -= scroll_speed
        if abs(scroll) > 89:
           scroll = 0
        
        pygame.display.update()
        clock.tick(fps)
    pygame.quit


if __name__ == "__main__":
    main()