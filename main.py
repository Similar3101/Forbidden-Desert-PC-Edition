import pygame


try:
    a = '1100 5'.split()
    SIZE = [WIDTH, HEIGHT] = [int(a[0]), int(a[0]) - 300]
    size_of_rect = int(a[1])
    BACKGROUND = (0, 0, 0)
except Exception:
    print('Неправильный формат ввода')
    exit()

dict_of_place = {0: 'green',
                 1: 'red',
                 2: 'red',
                 3: 'yellow',
                 4: 'yellow',
                 5: 'orange',
                 6: 'orange',
                 7: 'grey',
                 8: 'grey',
                 9: 'blue',
                 10: 'blue',
                 11: 'blue',
                 12: 'brown',
                 13: 'white',
                 14: 'white',
                 15: 'white',
                 16: 'white',
                 17: 'white',
                 18: 'white',
                 19: 'white',
                 20: 'white',
                 21: 'white',
                 22: 'white',
                 23: 'white',
                 24: 'white'}

list_of_place = [1, 3, 16, 10, 14,
          15, 6, 23, 24, 22,
          8, 13, 12, 17, 5,
          4, 9, 18, 19, 2,
          20, 0, 21, 7, 11]

opened_list = [0, 9, 10, 11, 12]


class Player:
    '''Базовый класс игроков
от него передаются все основные хар-ки:
Цвет, Кол-в воды, основные действия'''
    def __init__(self, coords=(0, 0), color=None, canteen=1):
        self.coords = coords
        self.color = color
        self.max_canteen = canteen
        self.equippack = []

    def get_can_move(self, coords, color):
        x1, y1 = self.coords
        x2, y2 = coords
        if (abs(x1 - x2) == 1 and y1 == y2) or (abs(y1 - y2) == 1 and x1 == x2):
            if color != 'brown':
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

    def take_detail(self, board, id_detail):
        # TODO придумать, как определять детали
        board.have_detail[id_detail] = True

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

    def get_can_move(self, coords, color):
        x1, y1 = self.coords
        x2, y2 = coords
        if color != 'brown':
            if (abs(x1 - x2) == 1 and y1 == y2) or (abs(y1 - y2) == 1 and x1 == x2):
                return True
            elif abs(x1 - x2) == 1 and abs(y1 - y2) == 1:
                return True
        return False

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


list_of_players = [Explorer()]


class Place:
    '''Клетки Пустыни'''
    def __init__(self, coords=0, image=None):
        self.coords = [coords // 5, coords % 5]
        self.color = dict_of_place[list_of_place[coords]] if list_of_place[coords] in opened_list else 'white'
        self.len_of_sandblock = 0
        self.players_on_place = [Explorer(coords=self.coords)] if self.color == 'green' else []
        self.is_digged = False
        self.can_move = True
        self.image = image

    def draw(self, size):
        a, b = self.coords[0], self.coords[1]
        x, y = (a * size) + 5, (b * size) + 5
        if not self.is_digged:
            pygame.draw.rect(screen, self.color, (x, y, size - 10, size - 10), 5)
        else:
            pygame.draw.rect(screen, self.color, (x, y, size - 10, size - 10))

    def draw_sandblock(self):
        x, y = (self.coords[0] * 160) + 10, (self.coords[1] * 160) + 10
        pygame.draw.circle(screen, 'orange', (x, y), 50, 5, draw_bottom_right=True)
        pygame.draw.line(screen, 'orange', [x + 45, y], [x + 87, y], 5)
        pygame.draw.circle(screen, 'orange', (x + 135, y), 50, 5, draw_bottom_left=True)
        pygame.draw.line(screen, 'orange', [x + 135, y + 45], [x + 135, y + 94], 5)
        pygame.draw.circle(screen, 'orange', (x + 135, y + 140), 50, 5, draw_top_left=True)
        pygame.draw.line(screen, 'orange', [x + 45, y + 138], [x + 87, y + 138], 5)
        pygame.draw.circle(screen, 'orange', (x, y + 140), 50, 5, draw_top_right=True)
        pygame.draw.line(screen, 'orange', [x, y + 45], [x, y + 94], 5)

    def add_sandblock(self):
        if not self.len_of_sandblock:
            self.draw_sandblock()
        self.len_of_sandblock += 1
        if self.len_of_sandblock >= 2:
            self.can_move = False

    def add_player(self, player):
        self.players_on_place.append(player)


class Board:
    def krest(self, screen, coords, c='orange'):
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
        self.board = [[Place(a * 5 + b) for b in range(0, 5)] for a in range(0, 5)]
        self.left = left
        self.top = top
        self.cell_size = cell_size
        self.have_detail = [False, False, False, False]
        self.krest(screen, (850, 630))

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self, screen):
        lol = (HEIGHT // size_of_rect)
        for j in range(5):
            for i in range(5):
                place = self.board[j][i]
                place.draw(lol)
                if (j % 4 != 0 or i % 4 != 0) and (j + i) % 2 == 0\
                        and not (j == 2 and i == 2):
                    place.add_sandblock()
                for player in place.players_on_place:
                    x, y, c = j * 160 + 75, i * 160 + 60, player.color
                    pygame.draw.polygon(screen, c, ([x, y], [x + 20, y], [x + 20, y + 20],
                                                    [x + 10, y + 20], [x + 20, y + 40], [x, y + 40],
                                                    [x + 10, y + 20],
                                                    [x, y + 20], [x, y]), 0)
                if place.len_of_sandblock:
                    place.draw_sandblock()

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


def lol():
    pygame.draw.rect(screen, 'blue', (850, 200, 150, 200), 5, border_radius=15)
    pygame.draw.rect(screen, 'red', (850, 420, 150, 200), 5, border_radius=15)
    pygame.draw.line(screen, 'white', (820, 0), (820, 800), 20)


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
    i = 0
    player = board.board[4][1].players_on_place[0]
    len_of_action = 4
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.pos[0] < 800:
                    x, y = event.pos[0] // 160, event.pos[1] // 160
                    if len_of_action:
                        if player.get_can_move((x, y), board.board[x][y].color):
                            board.board[x][y].add_player(player)
                            a, b = player.coords
                            board.board[a][b].players_on_place = []
                            player.coords = x, y
                            len_of_action -= 1
                            print((x, y), (player.coords, board.board[x][y].players_on_place), len_of_action)
        screen.fill((0, 0, 0))
        lol()
        board.render(screen)
        pygame.display.flip()
    pygame.quit()