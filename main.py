import pygame


try:
    # a = input('введите через пробел 2 числа\n').split()
    a = '1100 5'.split()
    SIZE = [WIDTH, HEIGHT] = [int(a[0]), int(a[0]) - 300]
    size_of_rect = int(a[1])
    BACKGROUND = (0, 0, 0)
except Exception:
    print('Неправильный формат ввода')
    exit()


class Place:
    x = -1

    def __init__(self):
        if Place.x == -1:
            Place.x = x = 0
            Place.y = y = 0
        else:
            Place.x += 1
        y += 1 if x % 5 == 0 and x != 0 else 0
        Place.y = y
        if (x == 4 and y == 0) or (x == 0 and y == 2) or (x == 2 and y == 4):
            c = 'blue'
        elif x == 2 and y == 2:
            c = 'black'
        elif x == 4 and y == 3:
            c = 'yellow'
            Place.player = (x, y)
        else:
            c = 'white'
        return None


def krest(screen, x, y, c='orange'):
    x += 15
    y += 15
    pygame.draw.circle(screen, c, (x, y), 50, 5, draw_bottom_right=True)
    pygame.draw.line(screen, c, [x + 45, y], [x + 87, y], 5)
    pygame.draw.circle(screen, c, (x + 135, y), 50, 5, draw_bottom_left=True)
    pygame.draw.line(screen, c, [x + 135, y + 45], [x + 135, y + 94], 5)
    pygame.draw.circle(screen, c, (x + 135, y + 140), 50, 5, draw_top_left=True)
    pygame.draw.line(screen, c, [x + 45, y + 138], [x + 87, y + 138], 5)
    pygame.draw.circle(screen, c, (x, y + 140), 50, 5, draw_top_right=True)
    pygame.draw.line(screen, c, [x, y + 45], [x, y + 94], 5)


def player(screen, x, y, c):
    x += 75
    y += 60
    pygame.draw.polygon(screen, c, ([x, y], [x + 20, y], [x + 20, y + 20],
                        [x + 10, y + 20], [x + 20, y + 40], [x, y + 40], [x + 10, y + 20],
                                    [x, y + 20], [x, y]), 0)


def draw(screen):
    screen.fill(BACKGROUND)
    lol = (HEIGHT // size_of_rect)

    for i in range(WIDTH):
        for j in range(HEIGHT):
            x = (w := WIDTH - 300) - (w - lol * i)
            y = (h := WIDTH - 300) - lol * j - lol
            if (i == 4 and j == 0) or (i == 0 and j == 2) or (i == 2 and j == 4):
                c = 'blue'
            elif i == 2 and j == 2:
                continue
            elif i == 4 and j == 3:
                c = 'yellow'
            else:
                c = 'white'
            print(c, (x, y), lol, (w, h), (i, j))
            pygame.draw.rect(screen, c, (x + 5, y + 5, lol - 10, lol - 10), 5)
            if (i % 4 != 0 or j % 4 != 0) and (i + j) % 2 == 0:
                # krest(screen, x, y)
                pass
            elif i == 0 and j == 0:
                player(screen, x, y, 'green')
            elif i == 4 and j == 0:
                player(screen, x, y, 'white')
    # krest(screen, 850, 630)
    pygame.draw.rect(screen, 'blue', (850, 200, 150, 200), 5, border_radius=15)
    pygame.draw.rect(screen, 'red', (850, 420, 150, 200), 5, border_radius=15)
    pygame.draw.line(screen, 'white', (820, 0), (820, 800), 20)


# if __name__ == '__main__':
#     pygame.init()
#     screen = pygame.display.set_mode(SIZE)
#     pygame.display.set_caption('desert')
#     draw(screen)
#     pygame.display.flip()
#     running = True
#     while running:
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 running = False
#             if event.type == pygame.MOUSEBUTTONDOWN:
#                 pass
#         draw(screen)
#     pygame.quit()

#

#
#
class Player:
    '''Базовый класс игроков
от него передаются все основные хар-ки:
Цвет, Кол-в воды, основные действия'''
    def __init__(self, coords=(0, 0), color=None, canteen=1):
        self.coords = coords
        self.color = color
        self.max_canteen = canteen
        self.equippack = []

    def get_can_move(self, coords):
        x1, y1 = self.coords
        x2, y2 = coords
        if abs(sum((x1 - x2, y1, y2))) == 1:
            return True
        return False

    def move(self, coords):
        if self.get_can_move(coords):
            self.coords = coords

    def remove_sand(self, coords):
        if self.coords == coords:
            pass
        elif self.get_can_move(coords):
            pass # TODO придумать что-нибудь с песчаныйми маркерами

    def dig_place(self):
        pass # TODO придумать что-нибудь с раскопками

    def take_detail(self):
        pass # TODO придумать, как, где хранятся данные про детали


class Archeologist(Player):
    '''"Быстрый копатель" Археолог
за 1 действие он убирает до 2 песчаных маркеров
красный, 4 воды'''
    def __init__(self, coords=(0, 0), color='red', canteen=3):
        super().__init__(coords, color, canteen)


class Climber(Player):
    '''Скаут
при перемещении может взять "в путь" с собой до 1 игрока
чёрный, 3 воды'''
    def __init__(self, coords=(0, 0), color='black', canteen=3):
        super().__init__(coords, color, canteen)


class Explorer(Player):
    '''Исследователь
может перемещаться по диогонали
зелёный, 4 воды'''
    def __init__(self, coords=(0, 0), color='green', canteen=4):
        super().__init__(coords, color, canteen)


class Meterologist(Player):
    '''Метеоролог
белый, 4 воды'''
    def __init__(self, coords=(0, 0), color='white', canteen=4):
        super().__init__(coords, color, canteen)


class Navigator(Player):
    '''Навигатор
жёлтый, 4 воды'''
    def __init__(self, coords=(0, 0), color='yellow', canteen=4):
        super().__init__(coords, color, canteen)


class WaterCarrier(Player):
    '''Хранитель воды
может за 1 действие "достать" из колодца 2 порции воды
Синий, 5 порций'''
    def __init__(self, coords=(0, 0), color='blue', canteen=5):
        super().__init__(coords, color, canteen)


class Board:
    def krest(self, screen, coords,  c='orange'):
        print(coords)
        x = coords[0] + 10
        y = coords[1] + 10
        pygame.draw.circle(screen, c, (x, y), 50, 5, draw_bottom_right=True)
        pygame.draw.line(screen, c, [x + 45, y], [x + 87, y], 5)
        pygame.draw.circle(screen, c, (x + 135, y), 50, 5, draw_bottom_left=True)
        pygame.draw.line(screen, c, [x + 135, y + 45], [x + 135, y + 94], 5)
        pygame.draw.circle(screen, c, (x + 135, y + 140), 50, 5, draw_top_left=True)
        pygame.draw.line(screen, c, [x + 45, y + 138], [x + 87, y + 138], 5)
        pygame.draw.circle(screen, c, (x, y + 140), 50, 5, draw_top_right=True)
        pygame.draw.line(screen, c, [x, y + 45], [x, y + 94], 5)

    def __init__(self, width=800, height=800, left=0, top=0, cell_size=160):
        self.width = width
        self.height = height
        self.board = [[p := Place()] * width for _ in range(height)]
        self.left = left
        self.top = top
        self.cell_size = cell_size
        self.krest(screen, (850, 630))

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self, screen):
        lol = (HEIGHT // size_of_rect)
        for j in range(5):
            for i in range(5):
                x = (w := WIDTH - 300) - (w - lol * j)
                y = (h := WIDTH - 300) - lol * i - lol
                if (y == 4 and x == 0) or (y == 0 and x == 2) or (y == 2 and x == 4):
                    c = 'blue'
                elif y == 2 and x == 2:
                    continue
                elif y == 4 and x == 3:
                    c = 'yellow'
                else:
                    c = 'white'
                print(c, (x, y), lol, (w, h), (y, x))
                pygame.draw.rect(screen, c, (x + 5, y + 5, lol - 10, lol - 10), 5)
                if (y % 4 != 0 or x % 4 != 0) and (y + x) % 2 == 0:
                    self.krest(screen, x, y)
                elif y == 0 and x == 0:
                    player(screen, x, y, 'green')

    def get_click(self, mouse_pos):
        pos = self.get_cell(mouse_pos)
        self.on_click(pos)

    def on_click(self, cell_coords):
        if cell_coords:
            x, y = cell_coords
            self.board[y][x] = not self.board[y][x]

    def get_cell(self, mouse_pos):
        cell_x = (mouse_pos[0] - self.left) // self.cell_size
        cell_y = (mouse_pos[1] - self.top) // self.cell_size
        if cell_x < 0 or cell_x >= self.width or cell_y < 0 or cell_y >= self.height:
            return None
        return cell_x, cell_y


if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode(SIZE)
    pygame.display.set_caption('desert')
    board = Board()
    board.render(screen)
    pygame.draw.rect(screen, 'blue', (850, 200, 150, 200), 5, border_radius=15)
    pygame.draw.rect(screen, 'red', (850, 420, 150, 200), 5, border_radius=15)
    pygame.draw.line(screen, 'white', (820, 0), (820, 800), 20)
    pygame.display.flip()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                pass
    pygame.quit()

# import pygame
# from math import pi
#
# # Initialize the game engine
# pygame.init()
#
# # Define the colors we will use in RGB format
# BLACK = (0, 0, 0)
# WHITE = (255, 255, 255)
# BLUE = (0, 0, 255)
# GREEN = (0, 255, 0)
# RED = (255, 0, 0)
#
# # Set the height and width of the screen
# size = [400, 300]
# screen = pygame.display.set_mode(size)
#
# pygame.display.set_caption("Example code for the draw module")
#
# # Loop until the user clicks the close button.
# done = False
# clock = pygame.time.Clock()
#
# while not done:
#
#     # This limits the while loop to a max of 10 times per second.
#     # Leave this out and we will use all CPU we can.
#     clock.tick(10)
#
#     for event in pygame.event.get():  # User did something
#         if event.type == pygame.QUIT:  # If user clicked close
#             done = True  # Flag that we are done so we exit this loop
#
#     # All drawing code happens after the for loop and but
#     # inside the main while done==False loop.
#
#     # Clear the screen and set the screen background
#     screen.fill(WHITE)
#
#     # Draw on the screen a GREEN line from (0, 0) to (50, 30)
#     # 5 pixels wide.
#     pygame.draw.line(screen, GREEN, [0, 0], [50, 30], 5)
#
#     # Draw on the screen 3 BLACK lines, each 5 pixels wide.
#     # The 'False' means the first and last points are not connected.
#     pygame.draw.lines(screen, BLACK, False, [[0, 80], [50, 90], [200, 80], [220, 30]], 5)
#
#     # Draw on the screen a GREEN line from (0, 50) to (50, 80)
#     # Because it is an antialiased line, it is 1 pixel wide.
#     pygame.draw.aaline(screen, GREEN, [0, 50], [50, 80], True)
#
#     # Draw a rectangle outline
#     pygame.draw.rect(screen, BLACK, [75, 10, 50, 20], 2)
#
#     # Draw a solid rectangle
#     pygame.draw.rect(screen, BLACK, [150, 10, 50, 20])
#
#     # Draw a rectangle with rounded corners
#     pygame.draw.rect(screen, GREEN, [115, 210, 70, 40], 10, border_radius=15)
#     pygame.draw.rect(screen, RED, [135, 260, 50, 30], 0, border_radius=10, border_top_left_radius=0,
#                      border_bottom_right_radius=15)
#
#     # Draw an ellipse outline, using a rectangle as the outside boundaries
#     pygame.draw.ellipse(screen, RED, [225, 10, 50, 20], 2)
#
#     # Draw an solid ellipse, using a rectangle as the outside boundaries
#     pygame.draw.ellipse(screen, RED, [300, 10, 50, 20])
#
#     # This draws a triangle using the polygon command
#     pygame.draw.polygon(screen, BLACK, [[100, 100], [0, 200], [200, 200]], 5)
#
#     # Draw an arc as part of an ellipse.
#     # Use radians to determine what angle to draw.
#     pygame.draw.arc(screen, BLACK, [210, 75, 150, 125], 0, pi / 2, 2)
#     pygame.draw.arc(screen, GREEN, [210, 75, 150, 125], pi / 2, pi, 2)
#     pygame.draw.arc(screen, BLUE, [210, 75, 150, 125], pi, 3 * pi / 2, 2)
#     pygame.draw.arc(screen, RED, [210, 75, 150, 125], 3 * pi / 2, 2 * pi, 2)
#
#     # Draw a circle
#     pygame.draw.circle(screen, BLUE, [60, 250], 40)
#
#     # Draw only one circle quadrant
#     pygame.draw.circle(screen, BLUE, [250, 250], 40, 0, draw_top_right=True)
#     pygame.draw.circle(screen, RED, [250, 250], 40, 30, draw_top_left=True)
#     pygame.draw.circle(screen, GREEN, [250, 250], 40, 20, draw_bottom_left=True)
#     pygame.draw.circle(screen, BLACK, [250, 250], 40, 10, draw_bottom_right=True)
#
#     # Go ahead and update the screen with what we've drawn.
#     # This MUST happen after all the other drawing commands.
#     pygame.display.flip()
#
# # Be IDLE friendly
# pygame.quit()