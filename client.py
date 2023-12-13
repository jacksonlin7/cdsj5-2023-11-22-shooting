import socket, json, threading, pygame, random, sys

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('172.16.172.218', 3000))

data_obj = {}
running = True

def server_transfer_data():
    global data_obj, running
    while running:
        data_length = client.recv(5)
        data_length = int(data_length.decode('utf-8'))
        data = client.recv(data_length)
        data = data.decode('utf-8')
        data_obj = json.loads(data)

threading.Thread(target=server_transfer_data, daemon=True).start()

pygame.init()

WIDTH, HEIGHT = 500, 400
window = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

SERVER_IP, SERVER_PORT = socket.gethostbyname(socket.gethostname()), 3000

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y) -> None:
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill((0, 0, 255))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y

class Target(pygame.sprite.Sprite):
    def __init__(self, x, y) -> None:
        super().__init__()
        self.image = pygame.Surface((20, 20))
        self.image.fill((0, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y

class Medkit(pygame.sprite.Sprite):
    def __init__(self, x, y) -> None:
        super().__init__()
        self.image = pygame.Surface((20, 20))
        self.image.fill((100, 100, 255))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int) -> None:
        super().__init__()
        self.image = pygame.Surface((20, 5))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y

class Score(pygame.sprite.Sprite):
    def __init__(self, x, y) -> None:
        super().__init__()
        self.font = pygame.font.SysFont('Arial', 28, True, False)
        self.image = self.font.render('Score: ' + 'None', True, (0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y

class Health(pygame.sprite.Sprite):
    def __init__(self, x, y) -> None:
        super().__init__()
        self.font = pygame.font.SysFont('Arial', 28, True, False)
        self.image = self.font.render('Health: ' + 'None', True, (0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y

sprites = pygame.sprite.Group()

while True:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit(pygame.quit)

    sprites.empty()

    for obj in data_obj.values():
        if obj['type'] == 'Player':
            sprites.add(Player(obj['x'], obj['y']))
        
        elif obj['type'] == 'Target':
            sprites.add(Target(obj['x'], obj['y']))

        elif obj['type'] == 'Medkit':
            sprites.add(Medkit(obj['x'], obj['y']))

        elif obj['type'] == 'Bullet':
            sprites.add(Bullet(obj['x'], obj['y']))

        elif obj['type'] == 'Score':
            sprites.add(Score(obj['x'], obj['y']))

        elif obj['type'] == 'Health':
            sprites.add(Health(obj['x'], obj['y']))

    window.fill((255, 255, 255))
    sprites.draw(window)
    pygame.display.update()
