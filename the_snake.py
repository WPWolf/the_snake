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
        self.position = ((SCREEN_HEIGHT // 2), (SCREEN_HEIGHT // 2))
        self.body_color = None

    def draw(self):
        """Метод отрисовки объектов"""
        pass


class Apple(GameObject):
    """Класс 'Apple' наследуется от основного"""

    def __init__(self):
        super().__init__()
        self.position = (((randint(0, (SCREEN_HEIGHT - GRID_SIZE)
                                   // GRID_SIZE)) * GRID_SIZE),
                         ((randint(0, (SCREEN_HEIGHT - GRID_SIZE)
                                   // GRID_SIZE)) * GRID_SIZE))
        self.body_color = APPLE_COLOR

    def draw(self):
        """Метод отрисовки объекта класса 'Apple' на экране"""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

    # Устанавливает новую позицию яблока
    @staticmethod
    def randomize_position(snake=None):
        """
        Статичный метод для рандомизации нового
        местоположения объекта 'Apple' на экране
        """
        position = snake[0]
        while position in snake:
            position = (((randint(0, (SCREEN_HEIGHT - GRID_SIZE)
                                  // GRID_SIZE)) * GRID_SIZE),
                        ((randint(0, (SCREEN_HEIGHT - GRID_SIZE)
                                  // GRID_SIZE)) * GRID_SIZE))
        return position


class Snake(GameObject):
    """Класс 'Snake' наследуется от основного"""

    def __init__(self):
        super().__init__()
        self.positions = [((SCREEN_HEIGHT // 2), (SCREEN_HEIGHT // 2))]
        self.last = None
        self.body_color = SNAKE_COLOR
        self.direction = choice([UP, DOWN, LEFT, RIGHT])
        self.length = 1

    @staticmethod
    def get_head_position(position, direction):
        """
        Статичный метод для определения положения головы 'змеи'
        на экране в зависимости от направления движения
        """
        # Оси абцисс и ординат для определения координат головы
        x = position[0][0] + (direction[0] * GRID_SIZE)
        y = position[0][1] + (direction[1] * GRID_SIZE)
        if x < 0:
            x += SCREEN_WIDTH
        elif x >= SCREEN_WIDTH:
            x -= SCREEN_WIDTH

        if y < 0:
            y += SCREEN_HEIGHT
        elif y >= SCREEN_HEIGHT:
            y -= SCREEN_HEIGHT

        head_position = (x, y)
        return head_position

    @property
    def update_direction(self):
        """Обновление направления движения объекта класса 'Snake'"""
        return choice([UP, DOWN, LEFT, RIGHT])

    def reset(self):
        """Метод сброса объекта класса 'Snake' в исходное состояние"""
        while self.length > 0:
            self.last = self.positions[self.length - 1]
            self.positions.pop(self.length - 1)
            self.draw()
            self.length -= 1

        self.positions.insert(0, ((SCREEN_HEIGHT // 2), (SCREEN_HEIGHT // 2)))
        self.direction = self.update_direction
        self.length = 1

    def draw(self):
        """Метод для отрисовки объекта класса 'Snake' на экране"""
        if len(self.positions) > 0:
            for position in self.positions[:-1]:
                rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
                pygame.draw.rect(screen, self.body_color, rect)
                pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

    # Отрисовка головы змейки
            head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, self.body_color, head_rect)
            pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

# Затирание последнего сегмента
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def move(self, head_pos, apple_pos):
        """Метод обновляет позицию объекта класса 'Snake'"""
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


def handle_keys(game_object):
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


def main():
    """Основная функция кода"""
    # Инициализация PyGame:
    pygame.init()
    # Тут нужно создать экземпляры классов.
    apple = Apple()
    snake = Snake()

    while True:
        clock.tick(SPEED)
        apple.draw()
        snake.draw()
        pygame.display.update()
        handle_keys(snake)

        head_pos = snake.get_head_position(snake.positions, snake.direction)
        snake.move(head_pos, apple.position)
        if head_pos == apple.position:
            apple.position = apple.randomize_position(snake.positions)


if __name__ == '__main__':
    main()
