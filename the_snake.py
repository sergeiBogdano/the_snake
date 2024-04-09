import random

import pygame as pg

# Инициализация PyGame:
pg.init()

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвета:
BOARD_BACKGROUND_COLOR = (0, 0, 0)
BORDER_COLOR = (93, 216, 228)
APPLE_COLOR = (255, 0, 0)
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 10

# Настройка игрового окна:
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pg.display.set_caption('Змейка')

# Настройка времени:
clock = pg.time.Clock()


class GameObject:
    """Базовый класс игровых объектов."""

    def __init__(self, position=(0, 0), body_color=SNAKE_COLOR):
        self.position = position
        self.body_color = body_color

    def draw(self):
        """Метод для отрисовки объектов."""
        pass


class Apple(GameObject):
    """Класс для яблока."""

    def __init__(self, snake_position, body_color=APPLE_COLOR):
        super().__init__(body_color=body_color)
        self.randomize_position(snake_position)

    def randomize_position(self, snake_position):
        """Метод для случайного изменения позиции яблока."""
        while True:
            new_position = (
                random.randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                random.randint(0, GRID_HEIGHT - 1) * GRID_SIZE
            )
            if new_position != snake_position:
                self.position = new_position
                break

    def draw(self):
        """Метод для отрисовки яблока."""
        rect = pg.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, self.body_color, rect)
        pg.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Класс для змейки."""

    def __init__(self, center_position, body_color=SNAKE_COLOR):
        super().__init__(position=center_position, body_color=body_color)
        self.direction = RIGHT
        self.next_direction = None
        self.length = 0
        self.tail = []

    def draw(self):
        """Метод для отрисовки змейки на экране."""
        rect = pg.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, self.body_color, rect)
        pg.draw.rect(screen, BORDER_COLOR, rect, 1)

        for segment in self.tail:
            rect = pg.Rect(segment, (GRID_SIZE, GRID_SIZE))
            pg.draw.rect(screen, self.body_color, rect)
            pg.draw.rect(screen, BORDER_COLOR, rect, 1)

    def move(self):
        """Метод для перемещения змейки."""
        if self.length > 0:
            self.tail.insert(0, self.position)
            if len(self.tail) > self.length:
                self.tail.pop()

        dx, dy = self.direction
        self.position = (
            (self.position[0] + dx * GRID_SIZE) % SCREEN_WIDTH,
            (self.position[1] + dy * GRID_SIZE) % SCREEN_HEIGHT
        )

    def update_direction(self):
        """Метод для обновления направления движения змейки."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def eat(self, apple):
        """Метод для проверки съедания яблока змейкой."""
        if self.position == apple.position:
            self.length += 1
            apple.randomize_position(self.tail + [self.position])

    def reset(self, center_position):
        """Метод для сброса состояния змейки."""
        self.position = center_position
        self.direction = RIGHT
        self.next_direction = None
        self.length = 0
        self.tail = []


def handle_keys(game_object):
    """Функция обработки действий пользователя."""
    global SPEED
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            raise SystemExit
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pg.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pg.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pg.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT
            elif event.key == pg.K_EQUALS:
                SPEED += 1
            elif event.key == pg.K_MINUS:
                SPEED = max(1, SPEED - 1)


def handle_keys(game_object):
    """Функция обработки действий пользователя."""
    global SPEED

    keys_pressed = pg.key.get_pressed()

    if keys_pressed[pg.K_UP] and game_object.direction != DOWN:
        game_object.next_direction = UP
    elif keys_pressed[pg.K_DOWN] and game_object.direction != UP:
        game_object.next_direction = DOWN
    elif keys_pressed[pg.K_LEFT] and game_object.direction != RIGHT:
        game_object.next_direction = LEFT
    elif keys_pressed[pg.K_RIGHT] and game_object.direction != LEFT:
        game_object.next_direction = RIGHT
    elif keys_pressed[pg.K_EQUALS]:
        SPEED += 1
    elif keys_pressed[pg.K_MINUS]:
        SPEED = max(1, SPEED - 1)
    elif keys_pressed[pg.K_ESCAPE]:
        pg.quit()
        raise SystemExit


def main():
    """Основная функция игры."""
    center_x = SCREEN_WIDTH // 2
    center_y = SCREEN_HEIGHT // 2
    snake = Snake((center_x, center_y))
    apple = Apple(snake.position)
    apple.randomize_position(snake.position)

    running = True
    while running:
        clock.tick(SPEED)

        handle_keys(snake)
        snake.update_direction()
        snake.move()
        snake.eat(apple)

        if snake.position in snake.tail:
            snake.reset((center_x, center_y))

        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    running = False
        screen.fill(BOARD_BACKGROUND_COLOR)
        snake.draw()
        apple.draw()
        pg.display.update()

    pg.quit()


if __name__ == '__main__':
    main()
