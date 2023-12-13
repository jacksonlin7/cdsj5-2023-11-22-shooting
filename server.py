import pygame, random, socket, threading, time, json

pygame.init()

WIDTH, HEIGHT = 500, 400
window = pygame.display.set_mode((WIDTH, HEIGHT))
running = True
clock = pygame.time.Clock()

SERVER_IP, SERVER_PORT = socket.gethostbyname(socket.gethostname()), 3000

medkit_generate_level = 1
score = 0
health = 1000000000

def handle_client(client: socket.socket, ip: tuple):
    players.update({
        f'{ip[0]}:{ip[1]}': Player()
    })

    while running:
        data = {}
        for sprite in sprites.sprites():
            data.update({
                f'{type(sprite).__name__}-{sprite.id}': {
                    'id': sprite.id,
                    'type': type(sprite).__name__,
                    'x': sprite.rect.x,
                    'y': sprite.rect.y
                }
            })
        
        data = json.dumps(data)
        data = data.encode('utf-8')
        data_length = len(data)
        data_length = str(data_length) + ' ' * (5 - len(str(data_length)))
        data_length = data_length.encode('utf-8')

        client.send(data_length)
        client.send(data)

    sprites.remove(players[f'{ip[0]}:{ip[1]}'])
    del players[f'{ip[0]}:{ip[1]}']

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((SERVER_IP, SERVER_PORT))
    server.listen(5)

    while running:
        threading.Thread(target=handle_client, args=list(server.accept()), daemon=True).start()

    server.close()

class Player(pygame.sprite.Sprite):
    def __init__(self) -> None:
        super().__init__()
        self.id = random.randint(10000, 99999)
        self.image = pygame.Surface((50, 50))
        self.image.fill((0, 0, 255))
        self.rect = self.image.get_rect()
        self.rect.center = (self.rect.width, HEIGHT // 2)
        self.cd = 0

    def update(self):
        global medkit_generate_level, score, health

        if self.cd > 0:
            self.cd -= 1

        if score // 5 == medkit_generate_level:
            sprites.add(Medkit())
            medkit_generate_level += 1

        if self == players[f'{SERVER_IP}:{SERVER_PORT}']:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE] and self.cd <= 0:
                sprites.add(Bullet(self.rect.right, self.rect.centery - 2.5))
                self.cd = 5

        if self == players[f'{SERVER_IP}:{SERVER_PORT}']:
            if keys[pygame.K_UP]:
                self.rect.y -= 5
            if keys[pygame.K_DOWN]:
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
        self.id = random.randint(10000, 99999)
        self.current_direction = random.randint(0, 1)
        self.current_pos = 0
        self.image = pygame.Surface((20, 20))
        self.image.fill((0, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH, random.randint(30, HEIGHT - 30))

    def update(self):
        global medkit_generate_level, score, health

        self.rect.x -= 3

        if self.rect.x < 0:
            self.rect.centerx = WIDTH
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

        for p in sprites.sprites():
            if type(p) == Player:
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
        self.id = random.randint(10000, 99999)
        self.current_direction = random.randint(0, 1)
        self.current_pos = 0
        self.image = pygame.Surface((20, 20))
        self.image.fill((100, 100, 255))
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH, random.randint(30, HEIGHT - 30))

    def update(self):
        global medkit_generate_level, score, health

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

        if self.rect.collideobjects([ p for p in sprites.sprites() if type(p) == Player ]):
            health += 1
            self.rect.y = random.randint(30, HEIGHT - 30)
            self.kill()

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int) -> None:
        super().__init__()
        self.id = random.randint(10000, 99999)
        self.image = pygame.Surface((20, 5))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = (x, y)

    def update(self):
        self.rect.x += 8
        if self.rect.left > WIDTH:
            self.kill()

class Score(pygame.sprite.Sprite):
    def __init__(self) -> None:
        super().__init__()
        self.id = random.randint(10000, 99999)
        global medkit_generate_level, score, health
        self.font = pygame.font.SysFont('Arial', 28, True, False)
        self.image = self.font.render('Score: ' + str(score), True, (0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 8 * 7, HEIGHT // 8)
    
    def update(self) -> None:
        global medkit_generate_level, score, health
        self.image = self.font.render('Score: ' + str(score), True, (0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 8 * 7, HEIGHT // 8)

class Health(pygame.sprite.Sprite):
    def __init__(self) -> None:
        super().__init__()
        self.id = random.randint(10000, 99999)
        global medkit_generate_level, score, health
        self.font = pygame.font.SysFont('Arial', 28, True, False)
        self.image = self.font.render('Health: ' + str(health), True, (0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.center = (self.rect.width // 2 + 12, HEIGHT // 8)
    
    def update(self) -> None:
        global medkit_generate_level, score, health
        self.image = self.font.render('Health: ' + str(health), True, (0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.center = (self.rect.width // 2 + 12, HEIGHT // 8)

players: dict = {
    f'{SERVER_IP}:{SERVER_PORT}': Player()
}

sprites = pygame.sprite.Group()
for i in range(3):
    sprites.add(Target())
sprites.add(Score())
sprites.add(Health())

threading.Thread(target=start_server, daemon=True).start()

while running:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    for player in players.values():
        if player not in sprites.sprites():
            sprites.add(player)
    sprites.update()

    window.fill((255, 255, 255))
    sprites.draw(window)
    pygame.display.update()

pygame.quit()
