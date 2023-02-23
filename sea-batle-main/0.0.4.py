import pygame as pg
import yadisk
import requests
import os
from random import randint, choice
from datetime import datetime, timedelta
pg.init()
SERVER = yadisk.YaDisk(token='ВАШ_ТОКЕН')
clock = pg.time.Clock()
VERSION_DATA = {'version': '0.0.4',
                'files': ['0F.png', '0T.png', '1F.png', '1T.png', '5T.png',
                          '2F.png', '2T.png', '3F.png', '3T.png', '5F.png',
                          '4F.png', '4T.png', 'info.png', 'go.png', '5M.png',
                          'setup1.png', 'setup2.png', 'page1.mp3'],
                'info': 'info.txt',
                'enc': 'Windows-1251',
                'data': 'data.txt',
                'su': '20.05.2022'}
COLORS = {'grey': (150, 150, 150), 'lilac': (100, 130, 250), 'red': (250, 40, 80),
          'blue': (40, 120, 200), 'dark': (60, 60, 60), 'green': (40, 250, 80),
          'yellow': (240, 200, 10), 'meddle': (90, 90, 100), 'dark_blue': (30, 90, 150)}


class Button:
    def __init__(self, x, y, hx, hy, text, color, screen):
        self.x, self.y, self.hx, self.hy = x, y, hx, hy
        self.name, self.col, self.nc = text, color, color
        self.screen, self.capflag = screen, False
        self.fh = hx // len(text + '12')
        if self.fh > hy * 0.75:
            self.fh = hy * 8 // 10
        self.font = pg.font.Font(None, self.fh * 3 // 2)

    def show(self, gr=None):
        if gr is not None:
            self.x = gr
        px, py = pg.mouse.get_pos()
        flag = px in range(self.x, self.x + self.hx) and py in range(self.y, self.y + self.hy)
        if flag:
            self.col = list(map(lambda dx: dx * 50 // 100, self.nc[:]))
        else:
            self.col = self.nc[:]
        r = self.hy // 10
        pg.draw.rect(self.screen, self.col, ((self.x - r, self.y), (self.hx + r * 2, self.hy)))
        pg.draw.rect(self.screen, self.col, ((self.x, self.y - r), (self.hx, self.hy + r * 2)))
        pg.draw.circle(self.screen, self.col, (self.x, self.y), r)
        pg.draw.circle(self.screen, self.col, (self.x + self.hx, self.y), r)
        pg.draw.circle(self.screen, self.col, (self.x, self.y + self.hy), r)
        pg.draw.circle(self.screen, self.col, (self.x + self.hx, self.y + self.hy), r)
        if self.name != '':
            b_text = self.font.render(self.name, True, [255 - self.col[0], 255 - self.col[1], 255 - self.col[2]])
            if self.capflag:
                self.screen.blit(b_text, (self.x + self.fh, self.y + self.fh))
            else:
                self.screen.blit(b_text, (self.x + self.hx - self.fh * len(self.name),
                                          self.y + (self.hy - self.fh) // 2))
        return flag

    def rename(self, text, color):
        self.name = text
        self.nc = color

    def get(self):
        return [self.name, self.nc]


def check():
    global VERSION_DATA
    a = os.listdir()
    rez = []
    if 'gamepic' not in a or 'gamesou' not in a:
        return VERSION_DATA['files']
    p, m = os.listdir('gamepic'), os.listdir('gamesou')
    for i in VERSION_DATA['files']:
        if i not in p and i not in m:
            rez.append(i)
        elif 'mp3' in i and i in p:
            os.replace('gamepic/' + i, 'gamesou/' + i)
        elif 'png' in i and i in m:
            os.replace('gamesou/' + i, 'gamepic/' + i)
    return rez


def enternet():
    try:
        d = requests.get('https://yandex.ru/').status_code
    except IOError:
        return [False, False]
    return [True, SERVER.check_token()]


def find_update():
    rez = []
    for item in SERVER.listdir('/app1/'):
        if '.exe' in item['name'] and item['name'] != VERSION_DATA['version'] + '.exe':
            rez.append(item['name'])
    return rez


def starting_load():
    pg.init()
    if not os.path.isdir("gamesou"):
        os.mkdir("gamesou")
    if not os.path.isdir("gamepic"):
        os.mkdir("gamepic")
    lfi, downloading = check(), 0
    if not len(lfi):
        return 1
    file_str = []
    if len(lfi) > 3:
        sch, par = 1, []
        for i in lfi[3:]:
            par.append(i)
            if sch % 4 == 0:
                file_str.append(', '.join(par))
                par.clear()
            sch += 1
        if par:
            file_str.append(', '.join(par))
    screen = pg.display.set_mode((600, 400))
    pg.display.set_caption('установка и устранение неполадок')
    load = Button(20, 300, 200, 60, 'скачать', (60, 150, 60), screen)
    canc = Button(260, 300, 200, 60, 'закрыть', (150, 60, 60), screen)
    font = pg.font.Font(None, 30)
    text2 = font.render(f'версия: {VERSION_DATA["version"]}', True, [255, 215, 0])
    while True:
        screen.fill((100, 100, 100))
        text1 = font.render(f'файлов не установлено: {len(lfi)}', True, [255, 215, 0])
        rezult = enternet()
        text3 = font.render(f'интернет работает хорошо', True, [255, 215, 0])
        text4 = font.render(f'сервер доступен', True, [255, 215, 0])
        text5 = font.render(f'осталось скачать: {", ".join(lfi)}', True, [255, 215, 0])
        if len(lfi) > 3:
            text5 = font.render(f'осталось скачать: {", ".join(lfi[0:3])}', True, [255, 215, 0])
            for i in range(len(file_str)):
                text6 = font.render(file_str[i], True, [255, 215, 0])
                screen.blit(text6, (20, 150 + i * 25))

        if not rezult[0]:
            text3 = font.render(f'нет доступа к интернету или сервису', True, [255, 215, 0])
        if not rezult[1]:
            text4 = font.render(f'проблемы с сервером', True, [255, 215, 0])
        screen.blit(text1, (20, 25))
        screen.blit(text2, (20, 50))
        screen.blit(text3, (20, 75))
        screen.blit(text4, (20, 100))
        screen.blit(text5, (20, 125))
        loadb, cancb = load.show(), canc.show()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return 0
            if event.type == pg.MOUSEBUTTONDOWN and cancb and not downloading and len(lfi):
                return 0
            elif event.type == pg.MOUSEBUTTONDOWN and cancb and not downloading and not len(lfi):
                return 1
            if event.type == pg.MOUSEBUTTONDOWN and loadb and rezult[0] and rezult[1]:
                downloading = 1
        if len(lfi) == 0:
            lfi, downloading = check(), 0
        if downloading:
            file = lfi.pop(0)
            if 'mp3' in file:
                SERVER.download('/app1/' + file, 'gamesou/' + file)
            if 'png' in file:
                SERVER.download('/app1/' + file, 'gamepic/' + file)
            sch, par, file_str = 1, [], []
            for i in lfi[3:]:
                par.append(i)
                if sch % 4 == 0:
                    file_str.append(', '.join(par))
                    par.clear()
                sch += 1
            if par:
                file_str.append(', '.join(par))
        clock.tick(30)
        pg.display.flip()


def starting():
    if 'deliteversion.txt' not in os.listdir():
        return starting_load()
    pg.init()
    with open('deliteversion.txt', mode='r', encoding=VERSION_DATA['enc']) as file:
        data = file.readlines()
    version, pu = data[0].rstrip('\n'), data[1].rstrip('\n')
    screen = pg.display.set_mode((800, 400))
    pg.display.set_caption('удаление устаревшей версии')
    load = Button(20, 300, 200, 60, 'удалить', (60, 150, 60), screen)
    canc = Button(260, 300, 200, 60, 'закрыть', (150, 60, 60), screen)
    font = pg.font.Font(None, 30)
    text2 = font.render(f'запущена версия: {VERSION_DATA["version"]}', True, [255, 215, 0])
    text1 = font.render(f'удаляемая версия: {version}', True, [255, 215, 0])
    text3 = font.render(f'путь к файлу: {pu}', True, [255, 215, 0])
    text4 = font.render(f'удаление сотрёт только файлы версии и настроек', True, [255, 215, 0])
    if pu == __file__:
        text4 = font.render('самоудаление невозможно', True, [255, 215, 0])
    elif version == VERSION_DATA['version']:
        text4 = font.render('бить своих - неправильно', True, [255, 215, 0])
    text5 = font.render('удалить папку с игрой - надёжный метод', True, [255, 215, 0])
    while True:
        screen.fill((100, 100, 100))
        screen.blit(text1, (20, 25))
        screen.blit(text2, (20, 50))
        screen.blit(text3, (20, 75))
        screen.blit(text4, (20, 100))
        screen.blit(text5, (20, 125))
        loadb, cancb = load.show(), canc.show()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return 0
            if event.type == pg.MOUSEBUTTONDOWN and cancb:
                return 0
            if event.type == pg.MOUSEBUTTONDOWN and loadb and pu != VERSION_DATA['version'] + '.exe':
                os.remove(pu)
                os.remove('deliteversion.txt')
                return starting_load()
        clock.tick(30)
        pg.display.flip()


def resort():
    global VERSION_DATA
    rezult = {}
    for i in VERSION_DATA['files']:
        if 'png' in i:
            sp = 'gamepic/'
            rezult[i.split('.')[0]] = pg.image.load(sp + i)
        else:
            sp = 'gamesou/'
    return rezult


class Cell:
    def __init__(self, x, y, hx, hy, image, color, screen):
        self.x, self.y, self.hx, self.hy = x * 11 // 10, y * 11 // 10, hx, hy
        self.image, self.col, self.nc = image, color, color
        self.screen, self.main, r = screen, color, self.hy // 10
        self.task_c, self.task_t, self.task_l = None, None, None
        if image is not None:
            self.image = pg.transform.scale(self.image, (self.hx + r * 2, self.hy + r * 2))
            self.image.set_colorkey((255, 255, 255))

    def show(self, flag_m=False, gr=None):
        r = self.hy // 10
        if gr is not None:
            self.x = gr
        px, py = pg.mouse.get_pos()
        flag = px in range(self.x - r, self.x + self.hx + r) and py in range(self.y - r, self.y + self.hy + r)
        if self.task_c is not None and not flag_m:
            if (datetime.now() - self.task_l) > timedelta(seconds=self.task_t):
                self.nc, self.task_c = self.main[:], None
            else:
                self.nc = self.task_c[:]
        if flag:
            self.col = list(map(lambda dx: dx * 50 // 100, self.nc[:]))
        else:
            self.col = self.nc[:]
        pg.draw.rect(self.screen, self.col, ((self.x - r, self.y), (self.hx + r * 2, self.hy)))
        pg.draw.rect(self.screen, self.col, ((self.x, self.y - r), (self.hx, self.hy + r * 2)))
        pg.draw.circle(self.screen, self.col, (self.x, self.y), r)
        pg.draw.circle(self.screen, self.col, (self.x + self.hx, self.y), r)
        pg.draw.circle(self.screen, self.col, (self.x, self.y + self.hy), r)
        pg.draw.circle(self.screen, self.col, (self.x + self.hx, self.y + self.hy), r)
        if self.image is not None:
            screen.blit(self.image, (self.x - r, self.y - r, self.hx + self.x, self.hy + self.y))
        return flag

    def rename(self, image, color, ang=0):
        r = self.hy // 10
        self.image, self.nc, self.main = image, color, color
        if image is not None:
            self.image = pg.transform.scale(self.image, (self.hx + r * 2, self.hy + r * 2))
            self.image = pg.transform.rotate(self.image, ang * 90)
            self.image.set_colorkey((255, 255, 255))

    def replace(self, x, y):
        self.x, self.y = x, y

    def task(self, time, color, g=0):
        if self.task_c == color or self.task_c is None:
            self.task_l, self.task_t = datetime.now(), time
            r1, g1, b1 = self.main
            r2, g2, b2 = color
            ug = 20 - g
            self.task_c = (ug * r2 + r1 * g) // 20, (ug * g2 + g1 * g) // 20, (ug * b2 + b1 * g) // 20


class Timer:
    def __init__(self, tick):
        self.tick, self.last = tick, datetime.now()

    def tk(self):
        if (datetime.now() - self.last) > timedelta(seconds=self.tick):
            self.last = datetime.now()
            return True
        return False


class Field:
    def __init__(self, screen, x, y, files):
        self.chose_ship = {5: 2, 4: 4, 3: 6, 2: 8, 1: 10}
        self.files = files
        self.D, self.pause = 20, False
        pg.display.set_caption(f'sea battle {VERSION_DATA["version"]}')
        pg.display.set_icon(self.files['go'])
        self.hxy = pg.display.get_window_size()
        self.x, self.y, self.sc = x, y, screen
        self.my_field = [[0 for i in range(self.D)] for _ in range(self.D)]
        self.en_field = [[0 for i in range(self.D)] for _ in range(self.D)]
        self.h = (self.hxy[1] // 30)
        for x in range(self.D):
            for y in range(self.D):
                self.my_field[x][y] = Cell(int(self.x + self.h * x * 1.2), int(self.y + self.h * y * 1.2),
                                           self.h, self.h, None, COLORS['blue'], self.sc)
                self.en_field[x][y] = Cell(int(self.x + self.h * x * 1.2), int(self.y + self.h * y * 1.2),
                                           self.h, self.h, None, COLORS['blue'], self.sc)

        self.ships, self.points, self.helf, self.shoots = {}, {}, 0, 0
        self.tasker = [None, None, None, None]
        self.time = Timer(0.03)
        self.task(COLORS['green'], randint(0, self.D), randint(0, self.D))

    def show(self):
        rezult = [None, None]
        for x in range(self.D):
            for y in range(self.D):
                if None not in self.tasker and not self.pause:
                    dd = ((self.tasker[2] - x) ** 2 + (self.tasker[3] - y) ** 2) ** 0.5
                    if self.tasker[0] - 0.4 <= dd <= self.tasker[0] + 0.4:
                        self.my_field[x][y].task(0.1, self.tasker[1], self.tasker[0])
                if self.my_field[x][y].show(self.pause):
                    rezult = [x, y]
        if None not in self.tasker and self.time.tk() and not self.pause:
            self.tasker[0] += 1
            if self.tasker[0] > 20:
                self.tasker = [None, None, None, None]
        return rezult

    def show_enemy(self):
        rezult = [None, None]
        for x in range(self.D):
            for y in range(self.D):
                if None not in self.tasker and not self.pause:
                    dd = ((self.tasker[2] - x) ** 2 + (self.tasker[3] - y) ** 2) ** 0.5
                    if self.tasker[0] - 0.4 <= dd <= self.tasker[0] + 0.4:
                        self.en_field[x][y].task(0.1, self.tasker[1], self.tasker[0])
                if self.en_field[x][y].show(self.pause):
                    rezult = [x, y]
        if None not in self.tasker and self.time.tk() and not self.pause:
            self.tasker[0] += 1
            if self.tasker[0] > 20:
                self.tasker = [None, None, None, None]
        return rezult

    def task(self, color, x, y):
        self.tasker = [0, color, x, y]

    def freez(self, mode):
        self.pause = mode

    def pal(self, x, y):
        rez = []
        sp = [0, 1, -1]
        for i in sp:
            for j in sp:
                if i + x < 0 or i + x >= self.D or j + y < 0 or j + y >= self.D:
                    rez.append(False)
                else:
                    if self.my_field[i + x][j + y].main != COLORS['blue']:
                        rez.append(False)
                    else:
                        rez.append(True)
        return False not in rez

    def presi_ship(self, x, y, hxy, ang):
        if ang == 1:
            ax, ay, fl1 = 0, -1 * hxy, -1
        elif ang == 0:
            ax, ay, fl1 = hxy, 0, 1
        elif ang == 3:
            ax, ay, fl1 = 0, hxy, 1
        else:
            ax, ay, fl1 = -1 * hxy, 0, -1
        rez = []
        for i in range(x, x + ax, fl1):
            rez.append([i, y])
        for j in range(y, y + ay, fl1):
            rez.append([x, j])
        color = COLORS['green']
        if self.chose_ship[hxy] == 0:
            color = COLORS['red']
        for d in rez:
            if not self.pal(d[0], d[1]):
                color = COLORS['red']
        for d in rez:
            if d[0] in range(self.D) and d[1] in range(self.D):
                self.my_field[d[0]][d[1]].task(0.08, color)
        return [rez, color == COLORS['green'], ang]

    def set_ship(self, cor, ang):
        self.chose_ship[len(cor)] -= 1
        num = 0
        self.helf += len(cor)
        while num in self.ships.keys():
            num += 1
        self.ships[num] = cor
        ships = {1: ['4T'], 2: ['0T', '3T'], 3: ['0T', '2T', '3T'], 4: ['0T', '1T', '2T', '3T'],
                 5: ['0T', '1T', '2T', '1T', '3T']}
        for i in range(len(cor)):
            self.points[(cor[i][0], cor[i][1])] = [num, ships[len(cor)][i], ang]
            self.my_field[cor[i][0]][cor[i][1]].rename(self.files[ships[len(cor)][i]], COLORS['green'], ang)
        self.task(COLORS['green'], *cor[0])

    def destroy(self, x, y):
        if (x, y) in self.points.keys():
            ship = self.ships.pop(self.points[(x, y)][0], None)
            for i in ship:
                self.points.pop((i[0], i[1]), None)
                self.my_field[i[0]][i[1]].rename(None, COLORS['blue'])
            self.chose_ship[len(ship)] += 1
            self.task(COLORS['red'], x, y)
            self.helf -= len(ship)

    def shoot_data(self, rez, cor):
        if rez != -1:
            self.shoots += 1
        if rez == 0:
            self.en_field[cor[0][0]][cor[0][1]].rename(self.files['5F'], COLORS['dark_blue'])
            self.task(COLORS['lilac'], cor[0][0], cor[0][1])
        elif rez == 2:
            self.en_field[cor[0][0]][cor[0][1]].rename(self.files['5M'], COLORS['yellow'])
            self.task(COLORS['yellow'], cor[0][0], cor[0][1])
        elif rez == 3:
            var = [[-1, -1], [-1, 0], [-1, 1], [0, -1], [0, 0], [0, 1], [1, -1], [1, 0], [1, 1]]
            for b in cor:
                for c in var:
                    pl = [b[0] + c[0], b[1] + c[1]]
                    if pl[0] in range(self.D) and pl[1] in range(self.D) and pl not in cor:
                        self.en_field[pl[0]][pl[1]].rename(self.files['5F'], COLORS['dark_blue'])
                self.en_field[b[0]][b[1]].rename(self.files['5T'], COLORS['red'])
            self.task(COLORS['red'], cor[0][0], cor[0][1])

    def ask_on_destroy(self, sh):
        for i in self.ships[sh]:
            if 'T' in self.points[(i[0], i[1])][1]:
                return True
        return False

    def attack(self, x, y):
        if self.my_field[x][y].main != COLORS['blue'] or self.my_field[x][y].nc != COLORS['blue']:
            self.task(COLORS['lilac'], x, y)
            return -1, [[x, y]]
        if (x, y) in self.points.keys():
            self.helf -= 1
            self.points[(x, y)][1] = self.points[(x, y)][1][:-1] + 'F'
            self.my_field[x][y].rename(self.files[self.points[(x, y)][1]], COLORS['yellow'], self.points[(x, y)][2])
            ship = self.points[(x, y)][0]
            if not self.ask_on_destroy(ship):
                for i in self.ships[ship]:
                    self.my_field[i[0]][i[1]].rename(self.files[self.points[(i[0], i[1])][1]], COLORS['red'],
                                                     self.points[(i[0], i[1])][2])
                var = [[-1, -1], [-1, 0], [-1, 1], [0, -1], [0, 0], [0, 1], [1, -1], [1, 0], [1, 1]]
                for b in self.ships[ship]:
                    for c in var:
                        pl = [b[0] + c[0], b[1] + c[1]]
                        if pl[0] in range(self.D) and pl[1] in range(self.D) and pl not in self.ships[ship]:
                            self.my_field[pl[0]][pl[1]].rename(self.files['5F'], COLORS['dark_blue'])
                self.task(COLORS['red'], x, y)
                return 3, self.ships[ship]
            self.task(COLORS['yellow'], x, y)
            return 2, [[x, y]]
        else:
            self.my_field[x][y].rename(self.files['5F'], COLORS['dark_blue'])
        self.task(COLORS['dark_blue'], x, y)
        return 0, [[x, y]]

    def resp(self):
        for d in self.points.keys():
            self.my_field[d[0]][d[1]].main = COLORS['blue']
            self.my_field[d[0]][d[1]].nc = COLORS['blue']

    def dbtl(self):
        for i in self.chose_ship.keys():
            if self.chose_ship[i] != 0:
                return False, i
        return True, 0

    def autopos(self):
        if self.dbtl()[0]:
            for i in range(self.D):
                for j in range(self.D):
                    self.destroy(i, j)
        else:
            while not self.dbtl()[0]:
                s1, s2, s3 = self.presi_ship(randint(1, 18), randint(1, 18), self.dbtl()[1], randint(0, 3))
                if s2:
                    self.set_ship(s1, s3)


class LeftSetupPanel:
    def __init__(self, screen, objects=[]):
        xy = pg.display.get_window_size()
        self.sc, self.col = screen, COLORS['meddle']
        self.hy, self.hx = int((xy[1] * 8.2) // 10), (xy[0] * 3) // 10
        self.x, self.y = 0, int(0.12 * xy[1])
        self.col2 = COLORS['grey']
        self.mode, self.main_x, self.timer = False, self.hx, Timer(0.02)
        self.hx = self.main_x // 25
        self.obj = objects

    def show(self):
        if self.mode and self.timer.tk() and self.hx < self.main_x:
            self.hx += self.main_x // 25
        if not self.mode and self.timer.tk() and self.hx > self.main_x // 25:
            self.hx -= self.main_x // 25
        px, py = pg.mouse.get_pos()
        r = self.hy // 20
        flag = px in range(self.x, self.x + self.hx + r) and py in range(self.y - r, self.y + self.hy + r)
        pg.draw.rect(self.sc, self.col, ((self.x, self.y), (self.hx + r, self.hy)))
        pg.draw.rect(self.sc, self.col, ((self.x, self.y - r), (self.hx, self.hy + r * 2)))
        pg.draw.circle(self.sc, self.col, (self.x + self.hx, self.y), r)
        pg.draw.circle(self.sc, self.col, (self.x + self.hx, self.y + self.hy), r)
        pg.draw.line(self.sc, self.col2, (self.x, self.y - r), (self.x + self.hx, self.y - r), 2)
        pg.draw.line(self.sc, self.col2, (self.x, self.y + self.hy + r),
                       (self.x + self.hx, self.y + self.hy + r), 2)
        pg.draw.line(self.sc, self.col2, (self.x + self.hx + r, self.y),
                       (self.x + self.hx + r, self.y + self.hy), 2)
        pg.draw.arc(self.sc, self.col2, (self.x + self.hx - r, self.y - r, r * 2, r * 2),
                    0, 1.570796, 2)
        pg.draw.arc(self.sc, self.col2, (self.x + self.hx - r, self.y + self.hy - r, r * 2, r * 2),
                    4.712389, 6.283185, 2)
        rezult = []
        if len(self.obj):
            gr = self.hx - int(self.main_x * 0.95)
            for i in self.obj:
                rezult.append(i.show(gr))
        return flag, rezult

    def hide(self, mode):
        self.mode = mode

    def collibrate(self, a, b):
        if a >= len(self.obj):
            return None
        rel = self.obj[a].fh
        for i in range(a, b):
            i = self.obj[i]
            if isinstance(i, Button):
                rel = i.fh if i.fh < rel else rel
        for i in range(a, b):
            i = self.obj[i]
            if isinstance(i, Button):
                i.fh = rel
                i.font = pg.font.Font(None, rel * 3 // 2)
                i.capflag = True


class Text:
    def __init__(self, text, x, y, color, screen):
        self.sc, self.x, self.y, self.text = screen, x, y, text
        self.color, self.font = color, pg.font.Font(None, pg.display.get_window_size()[1] // 25)

    def show(self, gr=None):
        if gr is not None:
            self.x = gr
        screen.blit(self.font.render(self.text, True, self.color), (self.x, self.y))
        return False


class TopSetupPanel:
    def __init__(self, screen):
        xy = pg.display.get_window_size()
        self.sc, self.col = screen, COLORS['dark_blue']
        self.hy, self.hx = (xy[1] * 0.9) // 10, (xy[0] * 96) // 100
        self.x, self.y = int(xy[0] * 0.02), 0
        self.col2 = COLORS['lilac']
        self.mode, self.main_x, self.timer = False, self.hx, Timer(0.02)

    def show(self):
        r, pi = self.hy // 5, 3.141593
        pg.draw.rect(self.sc, self.col, ((self.x - r, self.y), (self.hx + r * 2, self.hy)))
        pg.draw.rect(self.sc, self.col, ((self.x, self.y), (self.hx, self.hy + r)))
        pg.draw.circle(self.sc, self.col, (self.x, self.y + self.hy), r)
        pg.draw.circle(self.sc, self.col, (self.x + self.hx, self.y + self.hy), r)
        pg.draw.line(self.sc, self.col2, (self.x - r, self.y), (self.x - r, self.y + self.hy), 2)
        pg.draw.line(self.sc, self.col2, (self.x + self.hx + r, self.y), (self.x + self.hx + r, self.y + self.hy), 2)
        pg.draw.line(self.sc, self.col2, (self.x, self.y + self.hy + r), (self.x + self.hx, self.y + self.hy + r), 2)
        pg.draw.arc(self.sc, self.col2, (self.x - r, self.y + self.hy - r, r * 2, r * 2.2), 1 * pi, pi * 1.5, 2)
        pg.draw.arc(self.sc, self.col2, (self.x + self.hx - r * 1.3, self.y + self.hy - r * 1.3, r * 2.5,
                                         r * 2.5), 1.5 * pi, pi * 2, 2)



game_loop = starting()
if game_loop:
    files = resort()
    screen = pg.display.set_mode()
    pg.display.toggle_fullscreen()
    hx, hy = pg.display.get_window_size()
    hy1, hx1 = (hx * 0.9) // 10, (hy * 96) // 100
    player = Field(screen, int(hx * 0.43), int(hy * 0.115), files)
    enemy = Field(screen, int(hx * 0.43), int(hy * 0.115), files)
    enemy.autopos()
    enemy.resp()
    but = Button(int(hx * 0.145), int(hy * 0.521), int(hx * 0.145), int(hy * 0.065), 'update', COLORS['green'], screen)
    text1 = Text('проверить обновления', 30, int(hy * 0.45), COLORS['yellow'], screen)
    setup_b = Cell(int(hx1 / 20), int(hy1 * 1.5 / 20), int(hy1 * 8 / 20), int(hy1 * 8 / 20),
                   files['setup2'], COLORS['dark_blue'], screen)
    start_b = Cell(int(hx1 * 3 / 20), int(hy1 * 1.5 / 20), int(hy1 * 8 / 20),
                   int(hy1 * 8 / 20), files['info'], COLORS['dark_blue'], screen)
    close_b = Button(int(hx1 * 30 / 20), int(hy1 * 2 / 20), int(hx1 * 6 / 20),
                     int(hy1 * 9 / 20), 'выйти', COLORS['dark_blue'], screen)
    my_step, game, build, my_step_b = True, False, False, True
    ship_b_1 = Button(int(hx * 0.145), int(hy * 0.25), int(hx * 0.2), int(hy * 0.065),
                      f'линкор: {player.chose_ship[5]}', COLORS['meddle'], screen)
    ship_b_2 = Button(int(hx * 0.145), int(hy * 0.35), int(hx * 0.2), int(hy * 0.065),
                      f'крейсер: {player.chose_ship[4]}', COLORS['meddle'], screen)
    ship_b_3 = Button(int(hx * 0.145), int(hy * 0.45), int(hx * 0.2), int(hy * 0.065),
                      f'миноносец: {player.chose_ship[3]}', COLORS['meddle'], screen)
    ship_b_4 = Button(int(hx * 0.145), int(hy * 0.55), int(hx * 0.2), int(hy * 0.065),
                      f'корвет: {player.chose_ship[2]}', COLORS['meddle'], screen)
    ship_b_5 = Button(int(hx * 0.145), int(hy * 0.65), int(hx * 0.2), int(hy * 0.065),
                      f'катер: {player.chose_ship[1]}', COLORS['meddle'], screen)
    ship_b_6 = Button(int(hx * 0.145), int(hy * 0.75), int(hx * 0.2), int(hy * 0.065),
                      f'начать', COLORS['meddle'], screen)
    ship_b_7 = Button(int(hx * 0.145), int(hy * 0.85), int(hx * 0.2), int(hy * 0.065),
                      f'auto', COLORS['meddle'], screen)
    left_panel_1 = LeftSetupPanel(screen, [ship_b_1, ship_b_2, ship_b_3, ship_b_4, ship_b_5, ship_b_6, ship_b_7])
    left_panel_1.collibrate(0, 5)
    left_panel_2 = LeftSetupPanel(screen, [but, text1])
    top_panel = TopSetupPanel(screen)
    left_panel_1.hide(True)
    timer1, timer2, timer_e, timer3 = Timer(5), Timer(10), Timer(2), Timer(1)
    version_update, ship_in_hands = [], [None, 0]
    enemy_po = [randint(1, 18), randint(1, 18)]
    all_mappa = []
    for xl in range(1, 19):
        for yl in range(1, 19):
            all_mappa.append((xl, yl))
    enemy_var, enemy_task = [[-1, 0], [0, -1], [0, 0], [0, 1], [1, 0]], []
    var = [[-1, 0], [0, -1], [0, 0], [0, 1], [1, 0]]
    var_v, var_g = [[0, -1], [0, 0], [0, 1]], [[-1, 0], [0, 0], [1, 0]]
    enemy_helf = Text(f'здоровье врага: {enemy.helf}', int(hx * 0.15), int(hy * 0.25), COLORS['yellow'], screen)
    enemy_shoots = Text(f'атаки врага: {enemy.shoots}', int(hx * 0.15), int(hy * 0.35), COLORS['yellow'], screen)
    player_helf = Text(f'здоровье игрока: {player.helf}', int(hx * 0.15), int(hy * 0.45), COLORS['yellow'], screen)
    player_shoots = Text(f'атаки игрока: {player.shoots}', int(hx * 0.15), int(hy * 0.55), COLORS['yellow'], screen)
    winer, win = Text('победитель: ----', int(hx * 0.15), int(hy * 0.65), COLORS['yellow'], screen), False
    steps = Text('ходит: ----', int(hx * 0.15), int(hy * 0.75), COLORS['yellow'], screen)
    text_view = [enemy_helf, enemy_shoots, player_helf, player_shoots, winer, steps]
    enemy_iscl, engr, last_shoot = [], 'N', False
    while game_loop:
        enemy_helf.text = f'здоровье врага: {enemy.helf}'
        enemy_shoots.text = f'атаки врага: {enemy.shoots}'
        player_helf.text = f'здоровье игрока: {player.helf}'
        player_shoots.text = f'атаки игрока: {player.shoots}'
        if my_step and game:
            steps.text = 'ходит: игрок'
        elif game:
            steps.text = 'ходит: враг'
        if enemy.helf == 0 and game:
            winer.text, win = 'победитель: игрок', True
        elif player.helf == 0 and game:
            winer.text, win = 'победитель: враг', True
        screen.fill(COLORS['dark'])
        for name in text_view:
            name.show(int(hx * 0.15))
        if not game or my_step == my_step_b:
            timer_e.last = datetime.now()
        elif timer_e.tk():
            my_step = my_step_b
        if not left_panel_2.mode and not build and timer2.tk() and not game:
            player.task(COLORS[choice(list(COLORS.keys()))], randint(0, player.D), randint(0, player.D))
        if timer1.tk() and left_panel_2.mode and not build:
            entr = enternet()
            if False in entr:
                text1.text = 'обновление: нет связи'
                but.nc = COLORS['red']
            else:
                version_update = find_update()
                if len(version_update):
                    text1.text = f'доступно: {max(version_update)}'
                    but.nc = COLORS['green']
                else:
                    but.nc = COLORS['red']
                    text1.text = 'обновление: нет версий'
        top_panel.show()
        if build:
            now = left_panel_1
        else:
            now = left_panel_2
        flag, buttons = now.show()
        if not game or not my_step or win:
            pxy = player.show()
        elif my_step:
            pxy = player.show_enemy()
        a2 = False
        if None not in pxy and None not in ship_in_hands and not game:
            a1, a2, a3 = player.presi_ship(pxy[0], pxy[1], ship_in_hands[0], ship_in_hands[1] % 4)
        setup_b_f, start_b_f, close_b_f = setup_b.show(), start_b.show(), close_b.show()
        for event in pg.event.get():
            if event.type == pg.MOUSEBUTTONDOWN and (win or game):
                if close_b_f:
                    game_loop = False
                if start_b_f:
                    setup_b.rename(files['setup1'], COLORS['dark_blue'])
                    player = Field(screen, int(hx * 0.43), int(hy * 0.115), files)
                    enemy = Field(screen, int(hx * 0.43), int(hy * 0.115), files)
                    enemy.autopos()
                    enemy.resp()
                    left_panel_1.hide(True)
                    enemy_po = [randint(1, 18), randint(1, 18)]
                    enemy_var, enemy_task = [[-1, 0], [0, -1], [0, 0], [0, 1], [1, 0]], []
                    winer.text, win, game = 'победитель: ----', False, False
                    steps.text = 'ходит: ----'
                    enemy_iscl, engr, last_shoot = [], 'N', False
                    all_mappa = []
                    for xl in range(1, 19):
                        for yl in range(1, 19):
                            all_mappa.append((xl, yl))
            if event.type == pg.MOUSEBUTTONDOWN and not win:
                if close_b_f:
                    game_loop = False
                if start_b_f and not game:
                    build = True
                    left_panel_1.hx = left_panel_2.hx
                    left_panel_1.hide(left_panel_2.mode)
                elif setup_b_f:
                    build = False
                    left_panel_2.hx = left_panel_1.hx
                    left_panel_2.hide(left_panel_1.mode)
                if flag and True not in buttons:
                    if now.mode:
                        now.hide(False)
                    else:
                        now.hide(True)
                if left_panel_2.mode and buttons[0] and len(version_update) and False not in enternet():
                    down = max(version_update)
                    SERVER.download('/app1/' + down, down)
                    with open('deliteversion.txt', mode='a+', encoding=VERSION_DATA['enc']) as file:
                        file.writelines(VERSION_DATA['version'] + '\n')
                        file.writelines(VERSION_DATA['version'] + '.exe' + '\n')
                    game_loop = False
                if left_panel_1.mode and True in buttons[:5] and not game and flag:
                    lkf = buttons.index(True)
                    ship_in_hands[0] = 5 - lkf
                elif my_step and a2 and not game:
                    player.set_ship(a1, a3)
                elif my_step and not a2 and None not in pxy and not game:
                    player.task(COLORS['yellow'], *pxy)
                    player.destroy(*pxy)
                elif left_panel_1.mode and True in buttons[5:] and not game:
                    if buttons[5]:
                        player.resp()
                        now.hide(False)
                        build, game = False, True
                    elif buttons[6]:
                        player.autopos()
                        now.hide(False)
                if game and None not in pxy and my_step and my_step == my_step_b:
                    rez, cor = enemy.attack(pxy[0], pxy[1])
                    player.shoot_data(rez, cor)
                    if rez == 0:
                        my_step_b = False
                        steps.text = 'ходит: враг'
            if event.type == pg.KEYUP and not game:
                if event.key == pg.K_r:
                    ship_in_hands[1] += 1
        if build:
            for i in range(5):
                cob = player.chose_ship[5 - i]
                left_panel_1.obj[i].name = left_panel_1.obj[i].name.split(':')[0] + f': {cob}'
                if cob == 0:
                    left_panel_1.obj[i].nc = COLORS['red']
                elif ship_in_hands[0] == 5 - i:
                    left_panel_1.obj[i].nc = COLORS['green']
                else:
                    left_panel_1.obj[i].nc = COLORS['meddle']
        if not win and not my_step and my_step == my_step_b and timer3.tk():
            if len(enemy_var):
                varp = enemy_var.pop(randint(0, len(enemy_var) - 1))
                rez2, cor2 = player.attack(enemy_po[0] + varp[0], enemy_po[1] + varp[1])
                enemy.shoot_data(rez2, cor2)
                if rez2 == 0:
                    my_step_b = True
                    steps.text = 'ходит: игрок'
                elif rez2 == 2:
                    if last_shoot and engr == 'N':
                        aa1 = abs(last_shoot[0] - enemy_po[0] - varp[0])
                        aa2 = abs(last_shoot[1] - enemy_po[1] - varp[1])
                        if last_shoot[0] == enemy_po[0] + varp[0] and aa2 == 1:
                            engr = 'V'
                        elif last_shoot[1] == enemy_po[1] + varp[1] and aa1 == 1:
                            engr = 'G'
                        if aa1 > 1 or aa2 > 1:
                            last_shoot = False
                    last_shoot = [enemy_po[0] + varp[0], enemy_po[1] + varp[1]]
                    if varp != [0, 0]:
                        enemy_task += cor2
                    if [0, 1] in enemy_var and varp[1] == 0 != varp[0]:
                        enemy_var.pop(enemy_var.index([0, 1]))
                    if [1, 0] in enemy_var and varp[0] == 0 != varp[1]:
                        enemy_var.pop(enemy_var.index([1, 0]))
                    if [0, -1] in enemy_var and varp[1] == 0 != varp[0]:
                        enemy_var.pop(enemy_var.index([0, -1]))
                    if [-1, 0] in enemy_var and varp[0] == 0 != varp[1]:
                        enemy_var.pop(enemy_var.index([-1, 0]))
                elif rez2 == 3:
                    last_shoot = False
                    enemy_var, engr = var[:], 'N'
                    enemy_po = all_mappa.pop(all_mappa.index(choice(all_mappa)))
                    while enemy_po in enemy_iscl:
                        enemy_po = all_mappa.pop(all_mappa.index(choice(all_mappa)))
                    if len(enemy_task):
                        enemy_po = enemy_task.pop(0)
                elif rez2 == -1:
                    enemy_iscl += cor2
                    timer3.last = datetime.now() - timedelta(seconds=1)
            else:
                if len(enemy_task):
                    enemy_po = enemy_task.pop(0)
                    if engr == 'N':
                        enemy_var = var[:]
                    elif engr == 'G':
                        enemy_var = var_g[:]
                    elif engr == 'V':
                        enemy_var = var_v[:]
                else:
                    enemy_var = var[:]
                    enemy_po = all_mappa.pop(all_mappa.index(choice(all_mappa)))
                    while enemy_po in enemy_iscl:
                        enemy_po = all_mappa.pop(all_mappa.index(choice(all_mappa)))
        clock.tick(30)
        pg.display.flip()
