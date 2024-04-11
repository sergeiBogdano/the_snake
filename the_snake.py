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
DIRECTIONS = [UP, DOWN, LEFT, RIGHT]

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

    def __init__(self, body_color=SNAKE_COLOR):
        self.body_color = body_color
        self.position = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

    def draw(self):
        """Метод для отрисовки объектов."""
        pass


class Apple(GameObject):
    """Класс для яблока."""

    def __init__(self, snake_positions=None):
        super().__init__(body_color=APPLE_COLOR)
        self.randomize_position(snake_positions)

    def randomize_position(self, snake_positions=None):
        """Метод для случайного изменения позиции яблока."""
        while True:
            self.position = (
                random.randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                random.randint(0, GRID_HEIGHT - 1) * GRID_SIZE
            )
            if snake_positions is None or self.position not in snake_positions:
                break

    def draw(self):
        """Метод для отрисовки яблока."""
        rect = pg.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, self.body_color, rect)
        pg.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Класс для змейки."""

    def __init__(self):
        super().__init__(body_color=SNAKE_COLOR)
        self.reset()

    def draw(self):
        """Метод для отрисовки змейки."""
        screen.fill(BOARD_BACKGROUND_COLOR)  # Заливаем фон экрана

        for position in self.positions:
            rect = pg.Rect(position, (GRID_SIZE, GRID_SIZE))
            pg.draw.rect(screen, self.body_color, rect)
            pg.draw.rect(screen, BORDER_COLOR, rect, 1)

    def move(self):
        """Метод для перемещения змейки."""
        current_direction_x, current_direction_y = self.direction
        head_x, head_y = self.get_head_position()  # Получаем позицию головы змейки

        # Вычисляем новую позицию головы змейки
        new_head_x = (head_x + current_direction_x * GRID_SIZE) % SCREEN_WIDTH
        new_head_y = (head_y + current_direction_y * GRID_SIZE) % SCREEN_HEIGHT

        # Обновляем позицию головы змейки
        self.position = (new_head_x, new_head_y)

        # Вставляем новую позицию головы в начало списка позиций змейки
        self.positions.insert(0, self.position)

        # Проверяем столкновение головы с телом змейки
        if self.position in self.positions[1:]:
            self.reset()
            return

        # Обрезаем список позиций, чтобы сохранить длину змейки
        if len(self.positions) > self.length:
            self.positions.pop()

    def update_direction(self):
        """Метод для обновления направления движения змейки."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None


    def reset(self):
        """Метод для сброса состояния змейки."""
        self.direction = random.choice(DIRECTIONS)
        self.next_direction = None
        self.length = 1
        self.positions = [self.position]

    def get_head_position(self):
        """Метод для получения текущей позиции головы змейки."""
        return self.positions[0]


def handle_keys(game_object):
    """Функция обработки действий пользователя."""
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


def main():
    """Основная функция игры."""
    pg.init()

    snake = Snake()
    apple = Apple(snake.positions)

    while True:
        clock.tick(SPEED)

        handle_keys(snake)
        snake.update_direction()
        snake.move()
        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position(snake.positions)


        snake.draw()
        apple.draw()
        pg.display.update()

    pg.quit()


if __name__ == '__main__':
    main()
