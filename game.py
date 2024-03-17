import pygame
import random

pygame.init()

clock = pygame.time.Clock()
fps = 60

screen_width = 860
screen_height = 900

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Luna's adventures")  

font = pygame.font.SysFont('Bauhaus 93', 60)  
white = (255, 255, 255)  

ground_scroll = 0
scroll_speed = 4
flying = False
game_over = False
monster_gap = 350
monster_frequency = 1800  
last_monster = pygame.time.get_ticks() - monster_frequency
score = 0
pass_monster = False

bg = pygame.image.load('image/bg_01.png')
ground_img = pygame.image.load('image/ground.png')
button_img = pygame.image.load('image/restart.png')
small_button_img = pygame.transform.scale(button_img, (100, 50))

class Button:
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def draw(self, screen):
        action = False
        pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1:
                action = True

        screen.blit(self.image, (self.rect.x, self.rect.y))  

        return action


class BackButton:
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def draw(self, screen):
        action = False
        pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1:
                action = True

        screen.blit(self.image, (self.rect.x, self.rect.y))

        return action

def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

class Luna(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        self.index = 0
        self.counter = 0
        for num in range(1, 4):
            img = pygame.image.load(f"image/Luna{num}.png")
            img = pygame.transform.scale(img, (int(img.get_width() / 2), int(img.get_height() / 2)))
            self.images.append(img)
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.vel = 0
        self.clicked = False

    def update(self):
        global flying, score, game_over
        if flying:
            self.vel += 0.5
            if self.vel > 8:
                self.vel = 8
            if self.rect.bottom < 768:
                self.rect.y += int(self.vel)
            if pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
                self.clicked = True
                self.vel = -10
                score += 1
            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False

        if not game_over:
            if pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
                self.clicked = True
                self.vel = -10
            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False

            flap_cooldown = 5
            self.counter += 1

            if self.counter > flap_cooldown:
                self.counter = 0
                self.index += 1
                if self.index >= len(self.images):
                    self.index = 0
                self.image = self.images[self.index]

            self.image = pygame.transform.rotate(self.images[self.index], self.vel * -2)
        else:
            self.image = pygame.transform.rotate(self.images[self.index], -90)

class Monster(pygame.sprite.Sprite):
    def __init__(self, x, y, position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("image/monster1.png")
        self.rect = self.image.get_rect()
        if position == 1:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect.bottomleft = [x, y - int(monster_gap / 2)]
        elif position == -1:
            self.rect.topleft = [x, y + int(monster_gap / 2)]
        self.passed = False

    def update(self):
        global score
        self.rect.x -= scroll_speed
        if self.rect.right < 0:
            self.kill()
        if not self.passed and self.rect.right < flappy.rect.centerx:
            self.passed = True
            score += 1

def reset_game(score):
    monster_group.empty()
    flappy.rect.x = 100
    flappy.rect.y = int(screen_height / 2)
    score = 0  
    return score

def main_menu():
    run_menu = True
    main_menu_bg = pygame.image.load('image/bgmenu.png')
    start_button_img = pygame.image.load('image/start.png')
    quit_button_img = pygame.image.load('image/quit.png')
    back_button = BackButton(340, 250, pygame.image.load('image/home.png'))


    while run_menu:
        screen.blit(main_menu_bg, (0, 0))
        start_button_rect = start_button_img.get_rect(center=(screen_width / 2, 420))
        screen.blit(start_button_img, start_button_rect)
        quit_button_rect = quit_button_img.get_rect(center=(screen_width / 2, 720))
        screen.blit(quit_button_img, quit_button_rect)
        pygame.display.update()
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run_menu = False
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if start_button_rect.collidepoint(mouse_pos):
                    run_menu = False  
                elif quit_button_rect.collidepoint(mouse_pos):
                    run_menu = False  
                    pygame.quit()
                    quit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if start_button_rect.collidepoint(mouse_pos):
                    run_menu = False  
                elif quit_button_rect.collidepoint(mouse_pos):
                    run_menu = False  
                    pygame.quit()
                    quit()

main_menu()

button = Button((screen_width - small_button_img.get_width()) // 2,
                (screen_height - small_button_img.get_height()) // 2,
                small_button_img)

back_button = BackButton(340, 250, back_button)  

monster_group = pygame.sprite.Group() 
Luna_group = pygame.sprite.Group() 
flappy = Luna(100, int(screen_height / 2))
Luna_group.add(flappy)

run = True
score = 0  

while run:
    clock.tick(fps)
    screen.blit(bg, (0, 0))
    monster_group.draw(screen)
    Luna_group.draw(screen)
    Luna_group.update()
    screen.blit(ground_img, (ground_scroll, 768))
    draw_text(str(score), font, white, int(screen_width / 2), 20)

    if len(monster_group) > 0:
        if Luna_group.sprites()[0].rect.left > monster_group.sprites()[0].rect.left \
                and Luna_group.sprites()[0].rect.right < monster_group.sprites()[0].rect.right \
                and pass_monster == False:
            pass_monster = True
        if pass_monster == True:
            if Luna_group.sprites()[0].rect.left > monster_group.sprites()[0].rect.right:
                score += 1
                pass_monster = False

    if pygame.sprite.groupcollide(Luna_group, monster_group, False, False) or flappy.rect.top < 0:
        game_over = True

    for monster in monster_group:
        if not monster.passed and monster.rect.right < flappy.rect.centerx:
            monster.passed = True
            score += 1

    if game_over:
        if button.draw(screen):
            game_over = False
            score = reset_game(score)

        if back_button.draw(screen): 
            main_menu()  

    if flappy.rect.bottom >= 768:
        game_over = True
        flying = False

    if flying and not game_over:
        time_now = pygame.time.get_ticks()
        if time_now - last_monster > monster_frequency:
            monster_height = random.randint(-100, 100)
            btm_monster = Monster(screen_width, int(screen_height / 2) + monster_height, -1)
            top_monster = Monster(screen_width, int(screen_height / 2) + monster_height, 1)
            monster_group.add(btm_monster)
            monster_group.add(top_monster)
            last_monster = time_now
        monster_group.update()
        ground_scroll -= scroll_speed
        if abs(ground_scroll) > 35:
            ground_scroll = 0

    if game_over:
        if button.draw(screen):
            game_over = False
            score = reset_game(score)

        if back_button.draw(screen):  
            main_menu()  

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN and flying == False and game_over == False:
            flying = True

    pygame.display.update()

pygame.quit()
