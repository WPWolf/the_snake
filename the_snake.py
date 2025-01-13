from random import choice, randint

import pygame

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
SPEED = 20

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


class GameObject:
    """Основной объект"""

    def __init__(self) -> None:
        self.position = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))
        self.body_color = None

    def draw(self: object) -> None:
        """Метод отрисовки объектов"""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Apple(GameObject):
    """Класс 'Apple' наследуется от основного"""

    def __init__(self) -> None:
        super().__init__()
        self.position = self.randomize_position()
        self.body_color = APPLE_COLOR

    def draw(self: object) -> None:
        """Метод отрисовки объекта класса 'Apple' на экране"""
        super().draw()

    @staticmethod
    def randomize_position(snake_pos: list[tuple] = None) -> tuple:
        """
        Статичный метод для рандомизации нового
        местоположения объекта 'Apple' на экране
        """
        while True:
            position = (((randint(0, (SCREEN_HEIGHT - GRID_SIZE)
                                  // GRID_SIZE)) * GRID_SIZE),
                        ((randint(0, (SCREEN_HEIGHT - GRID_SIZE)
                                  // GRID_SIZE)) * GRID_SIZE))
            if snake_pos:
                if position not in snake_pos:
                    break
            else:
                break
        return position


class Snake(GameObject):
    """Класс 'Snake' наследуется от основного"""

    def __init__(self) -> None:
        self.reset()

    @staticmethod
    def get_head_position(position: list[tuple]) -> tuple:
        """
        Статичный метод для определения текущего
        положения головы 'змеи' на экране
        """
        return position[0]

    @property
    def update_direction(self: object) -> tuple:
        """Обновление направления движения объекта класса 'Snake'"""
        return choice([UP, DOWN, LEFT, RIGHT])

    def reset(self: object) -> None:
        """Метод сброса объекта класса 'Snake' в исходное состояние"""
        super().__init__()
        self.body_color = SNAKE_COLOR
        self.positions = [self.position]
        self.direction = self.update_direction
        self.length = 1
        self.last = None
        # Очистка игрового поля при начале новой игры
        pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR,
                         ((0, 0), (SCREEN_WIDTH, SCREEN_HEIGHT)))

    def draw(self: object) -> None:
        """Метод для отрисовки объекта класса 'Snake' на экране"""
        if len(self.positions) > 0:
            for position in self.positions[:-1]:
                rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
                pygame.draw.rect(screen, self.body_color, rect)
                pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

            # Отрисовка головы змейки
            super().draw()

        # Затирание последнего сегмента
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def move(self: object, head_pos: tuple, apple_pos: tuple) -> None:
        """Метод обновляет позицию объекта класса 'Snake'"""
        # Оси абцисс и ординат для определения координат головы
        x = head_pos[0] + (self.direction[0] * GRID_SIZE)
        y = head_pos[1] + (self.direction[1] * GRID_SIZE)
        if x < 0:
            x += SCREEN_WIDTH
        elif x >= SCREEN_WIDTH:
            x -= SCREEN_WIDTH

        if y < 0:
            y += SCREEN_HEIGHT
        elif y >= SCREEN_HEIGHT:
            y -= SCREEN_HEIGHT

        head_pos = (x, y)
        if head_pos == apple_pos:
            self.positions.insert(0, head_pos)
            self.last = None
            self.length += 1

        elif head_pos in self.positions:
            self.reset()

        else:
            self.positions.insert(0, head_pos)
            self.last = self.positions[self.length]
            self.positions.pop(self.length)


def handle_keys(game_object: object) -> None:
    """Метод обработки входящих нажатий"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit

        elif event.type == pygame.KEYDOWN:
            if (event.key == pygame.K_UP or event.key == pygame.K_w
                    and game_object.direction != DOWN):
                game_object.direction = UP

            elif (event.key == pygame.K_DOWN or event.key == pygame.K_s
                    and game_object.direction != UP):
                game_object.direction = DOWN

            elif (event.key == pygame.K_LEFT or event.key == pygame.K_a
                    and game_object.direction != RIGHT):
                game_object.direction = LEFT

            elif (event.key == pygame.K_RIGHT or event.key == pygame.K_d
                    and game_object.direction != LEFT):
                game_object.direction = RIGHT
            elif (event.key == pygame.K_ESCAPE):
                game_object.reset()


def main() -> None:
    """Основная функция кода"""
    # Инициализация PyGame:
    pygame.init()
    # Тут нужно создать экземпляры классов.
    apple = Apple()
    snake = Snake()

    while True:
        clock.tick(SPEED)
        apple.draw()
        snake.position = snake.get_head_position(snake.positions)
        snake.draw()
        pygame.display.update()
        handle_keys(snake)
        snake.move(snake.position, apple.position)
        if snake.position == apple.position:
            apple.position = apple.randomize_position(snake.positions)


if __name__ == '__main__':
    main()
