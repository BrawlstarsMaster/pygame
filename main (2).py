import pygame
import random

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

BLOCK_SIZE = 30
snake_speed = 10

background_images = ["background.png", "background1.png", "background2.png"]
head_images = ["head_snake.png", "head_snake1.png", "head_snake2.png"]

font = pygame.font.Font(None, 36)

score = 0
record = 0

running = True
menu = True
game_over = False
customization = False

background_index = 0
head_index = 0

background_image = pygame.image.load(background_images[background_index])
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

head_image = pygame.image.load(head_images[head_index])
head_image = pygame.transform.scale(head_image, (BLOCK_SIZE, BLOCK_SIZE))

UP = 0
DOWN = 1
LEFT = 2
RIGHT = 3

class Snake:
    def __init__(self):
        self.length = 5
        self.positions = [((WIDTH / 2), (HEIGHT / 2))]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.color = GREEN
        self.score = 0

    def get_head_position(self):
        return self.positions[0]

    def move(self, dir):
        cur = self.get_head_position()
        x, y = cur
        if dir == UP:
            y -= BLOCK_SIZE
        elif dir == DOWN:
            y += BLOCK_SIZE
        elif dir == LEFT:
            x -= BLOCK_SIZE
        elif dir == RIGHT:
            x += BLOCK_SIZE
        self.positions.insert(0, (x, y))
        if len(self.positions) > self.length:
            self.positions.pop()

    def draw(self, surface):
        for i, p in enumerate(self.positions):
            pygame.draw.rect(surface, self.color, (p[0], p[1], BLOCK_SIZE, BLOCK_SIZE))

    def collide(self):
        if self.get_head_position() in self.positions[1:]:
            return True
        if (
            self.get_head_position()[0] < 0
            or self.get_head_position()[0] >= WIDTH
            or self.get_head_position()[1] < 0
            or self.get_head_position()[1] >= HEIGHT
        ):
            return True
        return False

def generate_food():
    x = random.randint(0, (WIDTH - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
    y = random.randint(0, (HEIGHT - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
    return (x, y)

snake = Snake()

while running:
    while menu:
        screen.fill(BLACK)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                menu = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    menu = False
                    game_over = False
                    snake = Snake()
                    food = generate_food()
                    score = 0
                if event.key == pygame.K_q:
                    running = False
                    menu = False
                if event.key == pygame.K_c:
                    menu = False
                    customization = True

        screen.blit(background_image, (0, 0))
        text = font.render("Press SPACE to play, Q to quit, C to customize", True, WHITE)
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2))

        # Score board
        score_text = font.render("Record: " + str(record) + "    Recent Score: " + str(score), True, WHITE)
        screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2 + 50))

        pygame.display.flip()

    while customization:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                customization = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    background_index = (background_index - 1) % len(background_images)
                    background_image = pygame.image.load(background_images[background_index])
                    background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))
                if event.key == pygame.K_RIGHT:
                    background_index = (background_index + 1) % len(background_images)
                    background_image = pygame.image.load(background_images[background_index])
                    background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))
                if event.key == pygame.K_UP:
                    head_index = (head_index - 1) % len(head_images)
                    head_image = pygame.image.load(head_images[head_index])
                    head_image = pygame.transform.scale(head_image, (BLOCK_SIZE, BLOCK_SIZE))
                if event.key == pygame.K_DOWN:
                    head_index = (head_index + 1) % len(head_images)
                    head_image = pygame.image.load(head_images[head_index])
                    head_image = pygame.transform.scale(head_image, (BLOCK_SIZE, BLOCK_SIZE))
                if event.key == pygame.K_SPACE:
                    customization = False
                    menu = True

        screen.blit(background_image, (0, 0))
        text = font.render("Left/Right to change background, Up/Down to change head", True, WHITE)
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2))

        # Display selected background and head index
        bg_text = font.render("Background: " + str(background_index), True, WHITE)
        screen.blit(bg_text, (WIDTH // 2 - bg_text.get_width() // 2, HEIGHT // 2 + 50))
        head_text = font.render("Head: " + str(head_index), True, WHITE)
        screen.blit(head_text, (WIDTH // 2 - head_text.get_width() // 2, HEIGHT // 2 + 100))

        pygame.display.flip()

    while not menu and not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and snake.direction != DOWN:
                    snake.direction = UP
                if event.key == pygame.K_DOWN and snake.direction != UP:
                    snake.direction = DOWN
                if event.key == pygame.K_LEFT and snake.direction != RIGHT:
                    snake.direction = LEFT
                if event.key == pygame.K_RIGHT and snake.direction != LEFT:
                    snake.direction = RIGHT

        snake.move(snake.direction)
        if snake.get_head_position() == food:
            snake.length += 1
            score += 1
            food = generate_food()
        elif snake.collide():
            game_over = True
            if score > record:
                record = score

        screen.blit(background_image, (0, 0))
        snake.draw(screen)
        pygame.draw.rect(screen, RED, (food[0], food[1], BLOCK_SIZE, BLOCK_SIZE))

        text = font.render("Score: " + str(score), True, WHITE)
        screen.blit(text, (10, 10))

        pygame.display.flip()
        pygame.time.Clock().tick(snake_speed)

        # Increase snake size over time
        if snake.length < 50:
            snake.length += 1

    while game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                game_over = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_over = False
                    menu = True
                if event.key == pygame.K_q:
                    running = False
                    game_over = False
                if event.key == pygame.K_c:
                    game_over = False
                    customization = True

        screen.fill(BLACK)
        text = font.render("Game Over", True, RED)
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2))
        text = font.render("Press SPACE to play again, Q to quit, C to customize", True, WHITE)
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 + 50))

        pygame.display.flip()

pygame.quit()


