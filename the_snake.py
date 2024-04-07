import random
import pygame

# Инициализация PyGame:
pygame.init()

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

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 10

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


class GameObject:
    """Базовый класс игровых объектов."""

    def __init__(self, position, body_color):
        self.position = position
        self.body_color = body_color

    def draw(self, surface):
        """Класс для отрисовки объектов."""
        pass  # Этот метод будет переопределен в дочерних классах


class Apple(GameObject):
    """Класс для яблока."""

    def __init__(self):
        x = random.randint(0, GRID_WIDTH - 1) * GRID_SIZE
        y = random.randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        position = (x, y)
        super().__init__(position, APPLE_COLOR)

    def draw(self, surface):
        """Класс для отрисовки яблок."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(surface, self.body_color, rect)
        pygame.draw.rect(surface, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Класс для змейки."""

    def __init__(self):
        x = GRID_WIDTH // 2 * GRID_SIZE
        y = GRID_HEIGHT // 2 * GRID_SIZE
        super().__init__((x, y), SNAKE_COLOR)
        self.positions = [(x, y)]
        self.direction = RIGHT
        self.next_direction = None
        self.length = 1
        self.last = None

    def draw(self, surface):
        """для отрисовки змейки."""
        for position in self.positions[:-1]:
            rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(surface, self.body_color, rect)
            pygame.draw.rect(surface, BORDER_COLOR, rect, 1)
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(surface, self.body_color, head_rect)
        pygame.draw.rect(surface, BORDER_COLOR, head_rect, 1)

    def move(self):
        """для перемещения змейки."""
        self.update_direction()
        head_x, head_y = self.positions[0]
        dx, dy = self.direction
        new_head = (
            (head_x + dx * GRID_SIZE) % SCREEN_WIDTH,
            (head_y + dy * GRID_SIZE) % SCREEN_HEIGHT
        )
        if new_head in self.positions:
            raise Exception('Game Over - Snake Collided with Itself')
        self.last = self.positions[-1]
        self.positions.insert(0, new_head)
        if len(self.positions) > self.length:
            self.positions.pop()

    def update_direction(self):
        """для обновления действий змейки."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def change_direction(self, direction):
        """для изменения движения змейки."""
        if direction in (UP, DOWN, LEFT, RIGHT):
            self.next_direction = direction

    def eat(self, apple):
        """Класс для проверки съеденных яблок."""
        if self.positions[0] == apple.position:
            self.length += 1
            apple.position = (
                random.randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                random.randint(0, GRID_HEIGHT - 1) * GRID_SIZE
            )


def handle_keys(game_object):
    """Функция обработки действий пользователя:"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWM and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """Основная функция игры:"""
    snake = Snake()
    apple = Apple()

    running = True
    while running:
        clock.tick(SPEED)

        handle_keys(snake)
        snake.move()

        try:
            snake.eat(apple)
        except Exception as e:
            print(e)
            running = False

        # Отрисовка игровых объектов:
        screen.fill(BOARD_BACKGROUND_COLOR)
        snake.draw(screen)
        apple.draw(screen)
        pygame.display.update()

    pygame.quit()


if __name__ == '__main__':
    main()
