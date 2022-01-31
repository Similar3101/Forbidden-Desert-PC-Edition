import pygame
import os
import random


try:
    SIZE = [WIDTH, HEIGHT] = [1300, 800]
    size_of_rect = 5
    BACKGROUND = (0, 0, 0)
except Exception:
    exit()

dict_of_place = {0: '1.png',
                 1: '15.png',
                 2: '16.png',
                 3: '19.png',
                 4: '20.png',
                 5: '13.png',
                 6: '14.png',
                 7: '17.png',
                 8: '18.png',
                 9: '3.png',
                 10: '3.png',
                 11: '4.png',
                 12: '22.png',
                 13: '11.png',
                 14: '11.png',
                 15: '11.png',
                 16: '5.png',
                 17: '6.png',
                 18: '7.png',
                 19: '8.png',
                 20: '9.png',
                 21: '10.png',
                 22: '12.png',
                 23: '1.png',
                 24: '21.png',
                 25: 'red',
                 26: 'yellow',
                 27: 'orange',
                 28: 'grey'}


list_of_places = [1, 3, 16, 10, 14,
          15, 6, 23, 24, 22,
          8, 13, 12, 17, 5,
          4, 9, 18, 19, 2,
          20, 0, 21, 7, 11]
list_of_place = []
while list_of_places:
    place = random.choice(list_of_places)
    while place == 12 and len(list_of_place) != 12:
        place = random.choice(list_of_places)
    while place != 12 and len(list_of_place) == 12:
        place = 12
    if place == 0:
        coords_of_player = (len(list_of_place) // 5,len(list_of_place) % 5)
    list_of_place.append(place)
    list_of_places.remove(place)

opened_list = [0, 9, 10, 11, 12]
dos = ['11', '11', '11', '21', '21', '21', '31', '31', '31', '41', '41', '41',
       '12', '12', '22', '22', '32', '32', '42', '42',
       '13', '23', '33', '43',
       's', 's', 's', 's',
       'l', 'l', 'l']
deck_of_storm = []
while dos:
    card = random.choice(dos)
    dos.remove(card)
    deck_of_storm.append(card)


class Player:
    '''Базовый класс игроков
от него передаются все основные хар-ки:
Цвет, Кол-в воды, основные действия'''
    def __init__(self, place, coords=(0, 0), color=None, canteen=1):
        self.coords = tuple(coords)
        self.color = color
        self.max_canteen = canteen
        self.canteen = canteen
        self.equippack = []
        self.in_tunnel = False
        self.place = place

    def get_can_move(self, place):
        x1, y1 = self.coords
        x2, y2 = place.coords
        if place.color != 'brown' and place.can_move and self.place.can_move:
            if (abs(x1 - x2) == 1 and y1 == y2) or (abs(y1 - y2) == 1 and x1 == x2):
                self.place = place
                return True
            elif self.place.opened_image == 'asset//11.png' and self.place.is_digged:
                if place.is_digged and place.opened_image == 'asset//11.png':
                    self.place = place
                    return True
        return False

    def move(self, coords):
        x, y = self.coords
        x1, y1 = coords
        board.board[x1][y1].add_player(player)
        board.board[x][y].del_player(self)
        player.coords = x1, y1
        return True

    def remove_sand(self, place):
        coords = place.coords[0] * 5 + place.coords[1]
        nplace = Place(coords)
        nplace.len_of_sandblock, nplace.color = place.len_of_sandblock, place.color
        if tuple(self.coords) == tuple(place.coords) or self.get_can_move(nplace):
            if place.len_of_sandblock:
                place.len_of_sandblock -= 1
                if place.len_of_sandblock <= 1:
                    place.can_move = True
                    player.can_move = True
                return True
        return False

    def dig_place(self, place, board):
        if place.len_of_sandblock:
            self.remove_sand(place)
            return True
        elif place.type_of_place == '21.png' and False not in board.have_detail:
            pygame.quit()
        else:
            place.is_digged = True
            if place.type_of_place not in ['yellow', 'red', 'orange', 'grey']:
                place.get_coords_of_detail(board)
            return True
        return False

    def take_detail(self, place, board):
        if place.is_digged:
            if not place.len_of_sandblock:
                if place.detail:
                    id = place.detail.pop(0)
                    board.have_detail[id[1] - 25] = True
                    return True
        return False


class Archeologist(Player):
    '''"Быстрый копатель" Археолог
за 1 действие он убирает до 2 песчаных маркеров
красный, 4 воды'''
    def __init__(self, place, coords=(0, 0), color='red', canteen=3):
        super().__init__(place, coords, color, canteen)


class Climber(Player):
    '''Скаут
на него не действуют песчанные маркеры, всегда спокойно ходит
при перемещении может взять "в путь" с собой до 1 игрока
чёрный, 3 воды'''
    def __init__(self, place, coords=(0, 0), color='black', canteen=3):
        super().__init__(place, coords, color, canteen)

    def get_can_move(self, coords, place):
        x1, y1 = self.coords
        x2, y2 = coords
        if (abs(x1 - x2) == 1 and y1 == y2) or (abs(y1 - y2) == 1 and x1 == x2):
            if place.color != 'brown':
                return True
        return False


class Explorer(Player):
    '''Исследователь
может перемещаться по диогонали
зелёный, 4 воды'''
    def __init__(self, place, coords=(0, 0), color='green', canteen=4):
        super().__init__(place, coords, color, canteen)

    def get_can_move(self, place):
        x1, y1 = self.coords
        x2, y2 = place.coords
        if place.color != '22.png' and place.can_move and self.place.can_move:
            if (abs(x1 - x2) == 1 and y1 == y2) or (abs(y1 - y2) == 1 and x1 == x2):
                return True
            elif abs(x1 - x2) == 1 and abs(y1 - y2) == 1:
                return True
            elif self.place.opened_image == 'asset\\11.png' and self.place.is_digged:
                if place.is_digged and place.opened_image == 'asset\\11.png':
                    self.place = place
                    return True
        return False


class Meteorologist(Player):
    '''Метеоролог
"предсказывает" бурю, доставая карты
белый, 4 воды'''
    def __init__(self, place, coords=(0, 0), color='white', canteen=4):
        super().__init__(place, coords, color, canteen)


class Navigator(Player):
    '''Навигатор
может перемещать другий игроков
жёлтый, 4 воды'''
    def __init__(self, place, coords=(0, 0), color='yellow', canteen=4):
        super().__init__(place, coords, color, canteen)


class WaterCarrier(Player):
    '''Хранитель воды
может за 1 действие "достать" из колодца 2 порции воды
Синий, 5 порций'''
    def __init__(self, place, coords=(0, 0), color='blue', canteen=5):
        super().__init__(place, coords, color, canteen)


class Place:
    '''Клетки Пустыни'''
    def __init__(self, coords=0):
        self.coords = [coords // 5, coords % 5]
        self.color = dict_of_place[list_of_place[coords]] if list_of_place[coords] in opened_list else '1.png'
        self.len_of_sandblock = 0
        self.is_digged = False
        self.can_move = True
        self.closed_image = os.path.join('asset', self.color)
        self.detail = []
        self.type_of_place = list_of_place[coords]
        self.opened_image = os.path.join('asset', dict_of_place[self.type_of_place])
        self.players_on_place = [Explorer(self, coords=self.coords)] if self.type_of_place == 0 else []

    def draw(self, size):
        a, b = self.coords
        x, y = (a * size) + 5, (b * size) + 5
        a = pygame.image.load(self.opened_image if self.is_digged else self.closed_image)
        sprite = pygame.sprite.Sprite()
        sprite.image = a
        sprite.image.set_colorkey((0, 0, 0))
        sprite.image.convert_alpha()
        sprite.rect = sprite.image.get_rect()
        sprite.rect.x, sprite.rect.y = x, y
        return sprite


    def draw_sandblock(self):
        x, y = (self.coords[0] * 160) + 6, (self.coords[1] * 160) + 6
        a = pygame.image.load('asset//k1.png' if self.len_of_sandblock == 1 else 'asset//k2.png')
        sprite = pygame.sprite.Sprite()
        sprite.image = a
        sprite.image.set_colorkey((0, 0, 0))
        sprite.rect = sprite.image.get_rect()
        sprite.image.convert_alpha()
        sprite.rect.x, sprite.rect.y = x, y
        return sprite

    def add_sandblock(self):
        a = None
        if not self.len_of_sandblock:
            a = self.draw_sandblock()
        self.len_of_sandblock += 1
        if self.len_of_sandblock >= 2:
            self.can_move = False
            for player in self.players_on_place:
                player.can_move = False
        return a

    def add_player(self, player):
        self.players_on_place.append(player)
        player.place = self

    def del_player(self, player):
        self.players_on_place.pop(self.players_on_place.index(player))

    def replace_the_coords(self, new_place):
        self.coords, new_place.coords = new_place.coords, self.coords
        self.detail, new_place.detail = new_place.detail, self.detail
        for player in self.players_on_place:
            player.coords = tuple(new_place.coords)
            new_place.add_player(player)
            self.del_player(player)
        for player in new_place.players_on_place:
            player.coords = tuple(self.coords)
            self.add_player(player)
            new_place.del_player(player)

    def get_coords_of_detail(self, board):
        if self.type_of_place == 1:
            board.coords_of_detail[0][1] = self.coords[1]
        elif self.type_of_place == 2:
            board.coords_of_detail[0][0] = self.coords[0]
        elif self.type_of_place == 3:
            board.coords_of_detail[1][1] = self.coords[1]
        elif self.type_of_place == 4:
            board.coords_of_detail[1][0] = self.coords[0]
        elif self.type_of_place == 5:
            board.coords_of_detail[2][1] = self.coords[1]
        elif self.type_of_place == 6:
            board.coords_of_detail[2][0] = self.coords[0]
        elif self.type_of_place == 7:
            board.coords_of_detail[3][1] = self.coords[1]
        elif self.type_of_place == 8:
            board.coords_of_detail[3][0] = self.coords[0]
        for detail in board.coords_of_detail:
            if None in detail:
                continue
            ind = board.coords_of_detail.index(detail) + 25
            color_of_detail = dict_of_place[ind]
            j, i = detail
            if [color_of_detail, ] not in board.board[j][i].detail:
                board.board[j][i].detail.append([color_of_detail, ind])


class CardDeck:
    def __init__(self, board, level=1):
        self.board = board
        self.coords = (2, 2)
        self.level = level
        self.deck_of_storm = deck_of_storm
        self.used_dos = []
        self.deck_of_eqip = []
        self.dict_of_direction = {'1': 'right',
                      '2': 'up',
                      '3': 'left',
                      '4': 'down',
                      's': 'sun',
                      'l': 'level'}

    def draw(self, size):
        a, b = self.coords[0], self.coords[1]
        x, y = (a * size) + 5, (b * size) + 5
        pygame.draw.rect(screen, self.color, (x, y, size - 10, size - 10), 5)


    def get_stormcard(self):
        try:
            last_card = self.deck_of_storm.pop(0)
        except IndexError:
            self.deck_of_storm = self.used_dos
            while self.used_dos:
                card = random.choice(self.used_dos)
                self.used_dos.remove(card)
                deck_of_storm.append(card)
            last_card = self.deck_of_storm.pop(0)
        finally:
            if last_card == 's':
                return 's'
            elif last_card == 'l':
                return 'l'
            else:
                direction, len_of_move = self.dict_of_direction[last_card[0]], int(last_card[1])
                self.used_dos.append(last_card)

            return direction, len_of_move

    def get_eqip(self):
        pass

    def get_can_move(self, card):
        direction, len_of_move = card
        x, y = x1, y1 = self.coords
        if direction == 'down' and (y := y1 + len_of_move) >= 5:
            return False
        if direction == 'up' and (y := y1 - len_of_move) < 0:
            return False
        if direction == 'right' and (x := x1 + len_of_move) >= 5:
            return False
        if direction == 'left' and (x := x1 - len_of_move) < 0:
            return False
        self.new_coords = (x, y)
        print(self.new_coords)
        return True

    def get_len_stormcard(self, minus):
        if self.level == 1:
            return 2
        if self.level > 1 and self.level < 5:
            return 3
        if self.level > 4 and self.level < 9:
            return 4
        if self.level > 8 and self.level < 12:
            return 5
        if self.level > 11 and self.level < 14:
            return 6
        if self.level == 14:
            pygame.quit()

    def move_the_storm(self, card):
        if self.get_can_move(card):
            x, y = self.coords
            x1, y1 = self.new_coords
            self.board.board[x][y], self.board.board[x1][y1] = self.board.board[x1][y1], self.board.board[x][y]
            old_place, new_place = self.board.board[x][y], self.board.board[x1][y1]
            old_place.replace_the_coords(new_place)
            a = old_place.add_sandblock()
            self.coords = self.new_coords
        return x1, y1

    def summon_sun(self, players):
        for player in players:
            if not player.in_tunnel:
                player.canteen -= 1
                if player.canteen == 0:
                    pygame.quit()

    def level_up(self):
        self.level += 1


class Board:
    def draw_krest(self, screen, coords, c='orange'):
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
        self.coords_of_detail = [[None, None], [None, None], [None, None], [None, None]]
        self.have_detail = [False, False, False, False]
        self.draw_krest(screen, (850, 630))
        self.sprites = pygame.sprite.Group()
        for j in range(5):
            for i in range(5):
                place = self.board[j][i]
                if (j % 4 != 0 or i % 4 != 0) and (j + i) % 2 == 0 \
                    and not (j == 2 and i == 2):
                    self.sprites.add(place.add_sandblock())

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self, screen):
        lol = (HEIGHT // size_of_rect)
        sprites = pygame.sprite.Group()
        sprites.add(draw_card())
        for j in range(5):
            for i in range(5):
                place = self.board[j][i]
                sprites.add(place.draw(lol))
                if place.len_of_sandblock:
                    sprites.add(place.draw_sandblock())
                for detail in place.detail:
                    x, y = j * 160 + 45, i * 160 + 40
                    pygame.draw.rect(screen, detail[0], (x, y, 80, 80))
                for player in place.players_on_place:
                    x, y, color = j * 160 + 75, i * 160 + 60, player.color
                    sprite = pygame.sprite.Sprite()
                    sprite.image = pygame.image.load(f'asset//p{color}.png')
                    sprite.image.set_colorkey((0, 0, 0))
                    sprite.rect = sprite.image.get_rect()
                    sprite.image.convert_alpha()
                    sprite.rect.x, sprite.rect.y = x, y
                    sprites.add(sprite)
        sprites.draw(screen)


def draw_card():
    sprite1 = pygame.sprite.Sprite()
    sprite2 = pygame.sprite.Sprite()
    sprite3 = pygame.sprite.Sprite()
    sprite1.image = pygame.image.load('asset//d1.png')
    sprite1.rect = sprite1.image.get_rect()
    sprite1.rect.x, sprite1.rect.y = 850, 200
    sprite2.image = pygame.image.load('asset//d2.png')
    sprite2.rect = sprite1.image.get_rect()
    sprite2.rect.x, sprite2.rect.y = 850, 420
    sprite3.image = pygame.image.load('asset//k1.png')
    sprite3.rect = sprite1.image.get_rect()
    sprite3.rect.x, sprite3.rect.y = 850, 0
    return sprite1, sprite2, sprite3


if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode(SIZE)
    pygame.display.set_caption('desert')
    board = Board()
    board.render(screen)
    deck = CardDeck(board)
    pygame.display.flip()
    running = True
    which_player = 0
    player = board.board[coords_of_player[0]][coords_of_player[1]].players_on_place[0]
    players = [player]
    len_of_action = 4
    len_of_minus = 0
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.pos[0] < 800:
                    x, y = event.pos[0] // 160, event.pos[1] // 160
                    place = board.board[x][y]
                    action = False
                    if len_of_action:
                        if event.button == 1 and player.get_can_move(place):
                            action = player.move((x, y))
                            print((x, y), (player.coords, board.board[x][y].players_on_place), len_of_action)
                        elif event.button == 3:
                            if player.coords == (x, y):
                                if not place.is_digged:
                                    action = player.dig_place(place, board)
                                else:
                                    action = player.take_detail(place, board)
                            else:
                                action = player.remove_sand(place)
                                print(place.len_of_sandblock)
                    len_of_action -= 1 if action else 0
                    print(len_of_action)
                if not len_of_action:
                    for _ in range(deck.get_len_stormcard(len_of_minus)):
                        card = deck.get_stormcard()
                        if len(card) == 2:
                            deck.move_the_storm(card)
                        elif card == 's':
                            deck.summon_sun(which_player)
                        elif card == 'l':
                            deck.level_up()
                    len_of_minus = 0
                    len_of_action = 4
                    player = players[which_player if which_player < len(players) else 0]
        screen.fill((180, 100, 0))
        draw_card()
        board.render(screen)
        pygame.display.flip()
    pygame.quit()