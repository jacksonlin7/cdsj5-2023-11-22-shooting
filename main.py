import pygame, random, socket

pygame.init()

WIDTH, HEIGHT = 500, 400
window = pygame.display.set_mode((WIDTH, HEIGHT))
running = True
clock = pygame.time.Clock()

score = 0
health = 10

class Player(pygame.sprite.Sprite):
    def __init__(self, id: int) -> None:
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill((0, 0, 255))
        self.rect = self.image.get_rect()
        self.rect.center = (self.rect.width, HEIGHT // 2)
        self.score = 0
        self.cd = 0
        self.id = id
        self.medkit_generate_level = 1

    def update(self):
        if self.cd > 0:
            self.cd -= 1

        if self.score // 5 == self.medkit_generate_level:
            sprites.add(Medkit())
            self.medkit_generate_level += 1

        keys = pygame.key.get_pressed()
        if self.id == 1:
            if keys[pygame.K_SPACE] and self.cd <= 0:
                sprites.add(Bullet(self.rect.right, self.rect.centery - 2.5))
                self.cd = 5

        if self.id == 2:
            if keys[pygame.K_q] and self.cd <= 0:
                sprites.add(Bullet(self.rect.right, self.rect.centery - 2.5))
                self.cd = 5

        if self.id == 1:
            if keys[pygame.K_UP]:
                self.rect.y -= 5
            if keys[pygame.K_DOWN]:
                self.rect.y += 5

        if self.id == 2:
            if keys[pygame.K_w]:
                self.rect.y -= 5
            if keys[pygame.K_s]:
                self.rect.y += 5

        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT

        if health <= 0:
            self.kill()

class Target(pygame.sprite.Sprite):
    def __init__(self) -> None:
        super().__init__()
        self.current_direction = random.randint(0, 1)
        self.current_pos = 0
        self.image = pygame.Surface((20, 20))
        self.image.fill((0, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH, random.randint(30, HEIGHT - 30))

    def update(self):
        global health, score
        self.rect.x -= 3

        if self.rect.x < 0:
            self.rect.centerx = WIDTH
            if health > 0:
                health -= 1

        if self.current_direction == 0:
            self.rect.y -= random.randint(5, 8)
            self.current_pos += 1
            if self.current_pos > 10:
                self.current_pos = 0
                self.current_direction = 1

        if self.current_direction == 1:
            self.rect.y += random.randint(5, 8)
            self.current_pos += 1
            if self.current_pos > 10:
                self.current_pos = 0
                self.current_direction = 0

        if health <= 0:
            self.kill()

        if self.rect.collideobjects([bullet for bullet in sprites if type(bullet) == Bullet]):
            self.rect.collideobjects([bullet for bullet in sprites if type(bullet) == Bullet]).kill()
            score += 1
            self.rect.y = random.randint(30, HEIGHT - 30)
            self.rect.centerx = WIDTH

class Medkit(pygame.sprite.Sprite):
    def __init__(self) -> None:
        super().__init__()
        self.current_direction = random.randint(0, 1)
        self.current_pos = 0
        self.image = pygame.Surface((20, 20))
        self.image.fill((100, 100, 255))
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH, random.randint(30, HEIGHT - 30))

    def update(self):
        global health, score
        self.rect.x -= 3

        if self.rect.x < 0:
            self.kill()

        if self.current_direction == 0:
            self.rect.y -= random.randint(5, 8)
            self.current_pos += 1
            if self.current_pos > 10:
                self.current_pos = 0
                self.current_direction = 1

        if self.current_direction == 1:
            self.rect.y += random.randint(5, 8)
            self.current_pos += 1
            if self.current_pos > 10:
                self.current_pos = 0
                self.current_direction = 0

        if health <= 0:
            self.kill()

        if self.rect.collideobjects([player1, player2]):
            health += 1
            self.rect.y = random.randint(30, HEIGHT - 30)
            self.kill()

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int) -> None:
        super().__init__()
        self.image = pygame.Surface((20, 5))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = (x, y)

    def update(self):
        global health, score
        self.rect.x += 8
        if self.rect.left > WIDTH:
            self.kill()

class Score(pygame.sprite.Sprite):
    def __init__(self) -> None:
        super().__init__()
        self.font = pygame.font.SysFont('Arial', 28, True, False)
        self.image = self.font.render('Score: ' + str(score), True, (0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 8 * 7, HEIGHT // 8)
    
    def update(self) -> None:
        global health, score
        self.image = self.font.render('Score: ' + str(score), True, (0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 8 * 7, HEIGHT // 8)

class Health(pygame.sprite.Sprite):
    def __init__(self) -> None:
        super().__init__()
        global health, score
        self.font = pygame.font.SysFont('Arial', 28, True, False)
        self.image = self.font.render('Health: ' + str(health), True, (0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.center = (self.rect.width // 2 + 12, HEIGHT // 8)
    
    def update(self) -> None:
        global health, score
        self.image = self.font.render('Health: ' + str(health), True, (0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.center = (self.rect.width // 2 + 12, HEIGHT // 8)

player1 = Player(1)
player2 = Player(2)


sprites = pygame.sprite.Group()
for i in range(3):
    sprites.add(Target())
sprites.add(player1)
sprites.add(player2)
sprites.add(Score())
sprites.add(Health())

while running:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    sprites.update()

    window.fill((255, 255, 255))
    sprites.draw(window)
    pygame.display.update()

pygame.quit()
