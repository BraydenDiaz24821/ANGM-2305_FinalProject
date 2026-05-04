import pygame
import random


def main():

    # pygame activation & basic definitions
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
    fps = 60
    scroll = 0
    scroll_speed = 4
    pipe_frequency = 3000
    last_pipe = pygame.time.get_ticks() - pipe_frequency
    score = 0
    pass_pipe = False
    font = pygame.font.SysFont("Bauhaus 93", 100)
    font_color = (255, 0, 0)
    background = pygame.image.load("FF_Background.png")
    background_dummy = pygame.transform.scale(background, (1500, 700))
    foreground = pygame.image.load("FF_Foreground.jpg")
    pipe_group = pygame.sprite.Group()
    player_group = pygame.sprite.Group()
    player = PlayerObject(200, -300)
    player_group.add(player)
    player_flight = False
    pipe_movement = False
    bf_movement = False
    score_counter = False
    intro = True
    game_end = False
    visibility = True
    running = True

    while running:

        # player gravity & y-axis limiters
        if player_flight == True:
            player.vel += 0.5
            if player.vel > 8:
                player.vel = 8
            if player.rect.bottom < 1301:
                player.rect.y += int(player.vel)
            if player.rect.bottom >= 1300:
                game_end = True
                visibility = False
                score_counter = False
            if player.rect.bottom <= -301:
                game_end = True
                visibility = False
                score_counter = False

        # pipe spawn & x-axis movement
        if pipe_movement == True:
            time_now = pygame.time.get_ticks()
            if time_now - last_pipe > pipe_frequency:
                pipe_height = random.randint(-150, 150)
                top_pipe = PipeObject(2000, 460 + pipe_height, -1)
                bottom_pipe = PipeObject(2000, 460 + pipe_height, 1)
                pipe_group.add(top_pipe)
                pipe_group.add(bottom_pipe)
                last_pipe = time_now
    
        # background & foreground image spawn
        screen.blit(background_dummy, (0, 0))
        for i in range(2):
            screen.blit(foreground, (i * 800 + scroll, 600))
        if bf_movement == True:
            scroll -= scroll_speed
            if abs(scroll) > 89:
                scroll = 0

        # intro image spawn
        if intro == True:
            intro_image = pygame.image.load("FF_Intro.png")
            intro_image_dummy = pygame.transform.scale(intro_image, (1500, 1000))
            screen.blit(intro_image_dummy, (0, -50))

        # game-end image spawn
        if game_end == True:
            gameEnd_image = pygame.image.load("FF_GameEnd.png")
            gameEnd_image_dummy = pygame.transform.scale(gameEnd_image, (1500, 1000))
            screen.blit(gameEnd_image_dummy, (0, -50))

        # player start & quit
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            if event.type == pygame.KEYDOWN and player_flight == False:
                if event.key == pygame.K_LSHIFT:
                    player_flight = True
                    pipe_movement = True
                    bf_movement = True
                    score_counter = True
                    intro = False
                if event.key == pygame.K_RSHIFT:
                    player_flight = True
                    pipe_movement = True
                    bf_movement = True
                    score_counter = True
                    intro = False
        
        # sprite visibility
        if visibility == True:
            pipe_group.draw(screen)
            pipe_group.update()
            player_group.draw(screen)
            player_group.update()

        # player-pipe collision 
        if pygame.sprite.groupcollide(player_group, pipe_group, False, False):
            visibility = False
            player_flight = False
            pipe_movement = False
            bf_movement = False
            score_counter = False
            game_end = True
 
        # player-pipe score counter
        if score_counter == True:
            def draw_text(text, font, text_col, x, y):
                img = font.render(text, True, text_col)
                screen.blit(img, (x, y))
            if len(pipe_group) > 0:
                if player_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.left\
                    and player_group.sprites()[0].rect.right < pipe_group.sprites()[0].rect.right\
                    and pass_pipe == False:
                    pass_pipe = False
                if pass_pipe == False:
                    if player_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.right:
                        score += 1 / 8.5 / 2
                        pass_pipe = False
            draw_text(str(round(score)), font, font_color, int(100 / 2), 20)

        pygame.display.update()
        clock.tick(fps)
    pygame.quit


class PlayerObject(pygame.sprite.Sprite):
    
    # player sprite spawn & animation
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
        self.vel = 0
        self.press = False

    # player jump motion
    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] == 1 and self.clicked == False:
            self.clicked = True
            self.press = True
            self.vel = -10
        if keys[pygame.K_SPACE] == 0:
            self.clicked = False
        self.counter += 1
        swap_cooldown = 5
        if self.counter > swap_cooldown:
            self.counter = 0
            self.index += 1
            if self.index >= len(self.images):
                self.index = 0
        self.image = self.images[self.index]
        self.image = pygame.transform.rotate(self.images[self.index], self.vel * -1)


class PipeObject(pygame.sprite.Sprite):
    
    # pipe sprite spawn & positioning
    def __init__(self, x, y, position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("FF_PipeObject.jpeg")
        self.rect = self.image.get_rect()
        if position == -1:
            self.rect.topleft = [x, y + int(470 / 2)]
        if position == 1:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect.bottomleft = [x, y - int(470 / 2)]

    # pipe offscreen deletion
    def update(self):
        self.rect.x -= 5
        if self.rect.right < 0:
            self.kill()


if __name__ == "__main__":
    main()