import pygame, random

pygame.init()

WIDTH, HEIGHT = 500, 400
window = pygame.display.set_mode((WIDTH, HEIGHT))
running = True
clock = pygame.time.Clock()

class Player(pygame.sprite.Sprite):
    def __init__(self) -> None:
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill((0, 0, 255))
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 4, HEIGHT // 2)
        self.score = 0
        self.cd = 0

    def update(self):
        if self.cd > 0:
            self.cd -= 1

        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.cd <= 0:
            sprites.add(Bullet(self.rect.right, self.rect.centery - 2.5))
            self.cd = 5

        if keys[pygame.K_UP]:
            self.rect.y -= 5
        if keys[pygame.K_DOWN]:
            self.rect.y += 5

        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT

class Target(pygame.sprite.Sprite):
    def __init__(self) -> None:
        super().__init__()
        self.image = pygame.Surface((20, 20))
        self.image.fill((0, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 2 + WIDTH // 4, HEIGHT // 2)
        self.score = 0

    def update(self):
        pass

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int) -> None:
        super().__init__()
        self.image = pygame.Surface((20, 5))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = (x, y)

    def update(self):
        self.rect.x += 8
        if self.rect.left > WIDTH:
            self.kill()
        if self.rect.collideobjects([target]):
            player.score += 1
            print(player.score)
            target.rect.y = random.randint(30, HEIGHT - 30)
            self.kill()

class Score(pygame.sprite.Sprite):
    def __init__(self) -> None:
        super().__init__()
        self.font = pygame.font.SysFont('Arial', 28, True, False)
        self.image = self.font.render(str(player.score), True, (0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 8 * 7, HEIGHT // 8)
    
    def update(self) -> None:
        self.image = self.font.render(str(player.score), True, (0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 8 * 7, HEIGHT // 8)

player = Player()
target = Target()

sprites = pygame.sprite.Group()
sprites.add(player)
sprites.add(target)
sprites.add(Score())

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
