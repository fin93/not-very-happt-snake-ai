import pygame, random, math
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")
clock = pygame.time.Clock()


class Snake:
    def __init__(self, width=4, block_size=10):
        self.width = width
        self.block_size = block_size
        self.directions = {'right': self.block_size, 'left': -self.block_size, 'up': -self.block_size, 'down': self.block_size}
        self.direction = 'right'
        self.is_grow = 0
        self.prev = 0
        self.body = [[WIDTH // 2, HEIGHT // 2]]
        self.options = {}
        self.yes = 0
        self.available = ['up', 'down', 'left', 'right']
        self.depth = 1
        self.future = self.body[0]
        for i in range(1, self.width):  self.body.append([WIDTH // 2 - self.block_size * i, HEIGHT // 2])
    
    def decide(self, pos, depth=1):
        if not depth:       
            return math.hypot(pos[0] - apple.position[0], pos[1] - apple.position[1])

        if depth < self.depth:    self.direction = min(self.options, key=self.options.get)
        
        
        self.options.clear()
        for i in self.available:
            if i == 'down' or i == 'up':
                y = [pos[0], pos[1] + self.directions[i]]
                if not y in self.body:  
                    self.options[i] = self.decide(y, depth-1)
            elif i == 'right' or i == 'left':       
                y = [pos[0] + self.directions[i], pos[1]]
                if not y in self.body:  
                    self.options[i] = self.decide(y, depth-1)
        
        
        if len(self.options) != 0:
            if depth == self.depth:
                self.direction = min(self.options, key=self.options.get)
        

    def move(self, keys):
        if keys[pygame.K_RIGHT] or keys[pygame.K_d] and self.direction != 'left':
            self.direction = 'right'
            self.yes = 1
        elif keys[pygame.K_LEFT] or keys[pygame.K_a] and self.direction != 'right':
            self.direction = 'left'
            self.yes = 1
        elif keys[pygame.K_UP] or keys[pygame.K_w] and self.direction != 'down':
            self.direction = 'up'
            self.yes = 1
        elif keys[pygame.K_DOWN] or keys[pygame.K_s] and self.direction != 'up':
            self.direction = 'down'
            self.yes = 1
        else:   self.yes = 0

    def move_construct(self):
        self.body.pop()
        if self.yes:
            if self.direction == 'right' or self.direction == 'left':       
                x = [self.body[0][0] + self.directions[self.direction], self.body[0][1] + self.block_size]
            elif self.direction == 'down' or self.direction == 'up':
                x = [self.body[0][0] + self.block_size, self.body[0][1] + self.directions[self.direction]]
        else:
            if self.direction == 'right' or self.direction == 'left':       
                x = [self.body[0][0] + self.directions[self.direction], self.body[0][1]]
            elif self.direction == 'down' or self.direction == 'up':
                x = [self.body[0][0], self.body[0][1] + self.directions[self.direction]]
        
        if not x in self.body:
            self.body.insert(0, x)
        else:   print(len(self.body))

    def draw(self, on=1):
        if on:
            pygame.draw.circle(screen, (220, 220, 220), self.body[0], 9)
            for part in range(1, len(self.body)):
                pygame.draw.circle(screen, (120, 120, 120), self.body[part], 9)

    def grow(self):
        self.body.append(self.body[-1])

    def update(self):
        self.move_construct()
        self.draw()



class Apples:
    def __init__(self, block_size=10):
        self.position = [random.randint(1, WIDTH / 20 - 20) * 40, random.randint(1, HEIGHT / 20 - 20) * 60]
        self.block_size = block_size
        self.next = [0, 0]
        self.direction = 'right'
        self.keys = []

    def new(self, body):
        while self.position in body:
            self.position = [random.randint(1, WIDTH / 20 - 20) * 40, random.randint(1, HEIGHT / 20 - 20) * 60]
    
    def draw(self, on=1):
        if on:
            pygame.draw.circle(screen, (255, 100, 100), self.position, 9)
    
    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT] or keys[pygame.K_d] and self.direction != 'left':
            self.direction = 'right'
        elif keys[pygame.K_LEFT] or keys[pygame.K_a] and self.direction != 'right':
            self.direction = 'left'
        elif keys[pygame.K_UP] or keys[pygame.K_w] and self.direction != 'down':
            self.direction = 'up'
        elif keys[pygame.K_DOWN] or keys[pygame.K_s] and self.direction != 'up':
            self.direction = 'down'
        self.move_update()

    def move_update(self):
        if self.direction == 'right': self.next = [self.block_size, 0]
        elif self.direction == 'left': self.next = [-self.block_size, 0]
        elif self.direction == 'up': self.next = [0, -self.block_size]
        elif self.direction == 'down': self.next = [0, self.block_size]
        self.position[0] += self.next[0]
        self.position[1] += self.next[1]

    def update(self):
        self.move()
        self.draw()


snake = Snake(30)
apple = Apples()
framerate = 30
def main():
    yup = 0
    while True:
        yup += 1
        clock.tick(framerate)
        screen.fill((0, 0, 0))
        
        pygame.display.set_caption("Snake Game - FPS: " + str(clock.get_fps()))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        if not yup % 7:
            snake.decide(snake.body[0])
        snake.update()
        apple.update()

        if apple.position in snake.body:
            snake.grow()
            apple.new(snake.body)
        
        

        pygame.display.update()

while True:
    main()