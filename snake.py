import pygame
import sys
import random
import json

pygame.init()

WIDTH, HEIGHT = 800, 600
CELL_SIZE = 20
FPS = 10

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

class Snake:
    def __init__(self):
        self.length = 1
        self.positions = [((WIDTH // 2), (HEIGHT // 2))]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.color = RED

    def get_head_position(self):
        return self.positions[0]

    def update(self):
        cur = self.get_head_position()
        x, y = self.direction
        new = (((cur[0] + (x*CELL_SIZE)) % WIDTH), (cur[1] + (y*CELL_SIZE)) % HEIGHT)
        if len(self.positions) > 2 and new in self.positions[2:]:
            self.reset()
        else:
            self.positions.insert(0, new)
            if len(self.positions) > self.length:
                self.positions.pop()

    def reset(self):
        self.length = 1
        self.positions = [((WIDTH // 2), (HEIGHT // 2))]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])

    def render(self, surface):
        for p in self.positions:
            pygame.draw.rect(surface, self.color, (p[0], p[1], CELL_SIZE, CELL_SIZE))

class Fruit:
    def __init__(self):
        self.position = (0, 0)
        self.color = WHITE
        self.randomize_position()

    def randomize_position(self):
        self.position = (random.randint(0, (WIDTH // CELL_SIZE) - 1) * CELL_SIZE,
                         random.randint(0, (HEIGHT // CELL_SIZE) - 1) * CELL_SIZE)

    def render(self, surface):
        pygame.draw.rect(surface, self.color, (self.position[0], self.position[1], CELL_SIZE, CELL_SIZE))

def save_score(name, score):
    try:
        with open("snake_scores.json", "r") as file:
            scores = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        scores = []

    scores.append({"name": name, "score": score})

    with open("snake_scores.json", "w") as file:
        json.dump(scores, file)

def load_scores():
    try:
        with open("snake_scores.json", "r") as file:
            scores = json.load(file)
        return scores
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def show_high_scores():
    print("\nHigh Scores:")
    scores = load_scores()
    scores.sort(key=lambda x: x["score"], reverse=True)
    for i, score_entry in enumerate(scores[:5]):
        print(f"{i + 1}. {score_entry['name']}: {score_entry['score']}")


screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Змейка")
clock = pygame.time.Clock()

snake = Snake()
fruit = Fruit()

score = 0
player_name = ""

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                snake.direction = UP
            elif event.key == pygame.K_DOWN:
                snake.direction = DOWN
            elif event.key == pygame.K_LEFT:
                snake.direction = LEFT
            elif event.key == pygame.K_RIGHT:
                snake.direction = RIGHT

    snake.update()

    if snake.get_head_position() == fruit.position:
        snake.length += 1
        score += 1
        fruit.randomize_position()

    screen.fill(BLACK)
    snake.render(screen)
    fruit.render(screen)

    pygame.display.flip()
    clock.tick(FPS)

    if snake.get_head_position() in snake.positions[1:]:
        print(f"Ты проиграл! Твои очки от Вокамоне: {score}")
        if score > 0:
            player_name = input("Введи свое имя: ")
            save_score(player_name, score)
        show_high_scores()
        print('спасибо, что поиграли в меня:)')
        pygame.quit()
        sys.exit()
