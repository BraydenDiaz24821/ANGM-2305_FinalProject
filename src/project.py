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
    player_group = pygame.sprite.Group()
    player = PlayerObject(200, int(936 / 2))
    player_group.add(player)
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
        player_group.draw(screen)
        player_group.update()
 
        pygame.display.update()
        clock.tick(fps)
    pygame.quit


class PlayerObject(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        self.index = 0
        self.counter = 0
        for num in range(1, 4):
            img = pygame.image.load(f"FF_PlayerObject{num}.png")
            self.images.append(img)
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]

    def update(self):
        self.counter += 1
        swap_cooldown = 5
        if self.counter > swap_cooldown:
            self.counter = 0
            self.index += 1
            if self.index >= len(self.images):
                self.index = 0
        self.image = self.images[self.index]


if __name__ == "__main__":
    main()