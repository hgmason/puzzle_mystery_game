'''PYGAME WINDOW SETUP'''
import os
import time
import random
import math
import numpy as np
from PIL import Image
import cv2

import sys
import os

def resource_path(relative_path):
    try:
    # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

x = 100
y = 50
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (x,y)
import pygame, sys
from pygame.locals import *

# set up pygame
pygame.init()
pygame.font.init()
pygame.mixer.init()

'''EVERYTHING FROM ALL PUZZLES'''
assets = resource_path("assets/")
sounds = resource_path("sounds/")
music = resource_path("music/")
sprites = resource_path("sprites/")

sound_dict = {}
for sound_file in os.listdir(sounds):
    sound_dict[sound_file] = pygame.mixer.Sound(sounds+sound_file)

def write_list(file,array):
    if len(array) == 0:
        return
    for i in array[:-1]:
        #print(i)
        file.write(i+",")
    file.write(array[len(array)-1])
    return

def save_game():
    SH = SceneHandler()
    SH.set_background("saving")
    SH.windowSurface.blit(SH.background, (0,0))
    pygame.display.update()
    file = open(assets+"save_file.txt","w")
    file.write(str(spot)+"\n")
    write_list(file,friends)
    file.write("\n")
    write_list(file,met)
    file.write("\n")
    write_list(file,clues)
    file.close()
    return

def load_game():
    #return
    global friends
    global met
    global clues
    global spot
    try:
        file = open(assets+"save_file.txt")
    except:
        #print('no save file')
        return False
    contents = file.read()
    file.close()
    lines = contents.split("\n")
    spot = int(lines[0])
    friends = lines[1].split(",")
    met = lines[2].split(",")
    clues = [L for L in lines[3].split(",") if len(L) > 0]
    return spot > 0

def play_sound(filename):
    #soundObj = pygame.mixer.Sound(sounds+filename+".wav")
    #soundObj.play()
    sound_dict[filename+".wav"].play()

def play_song(filename, vol = .5):
    vol = vol / 4
    #return
    pygame.mixer.music.load(music+filename+".wav")
    pygame.mixer.music.set_volume(vol)
    pygame.mixer.music.play(-1)

def stop_song():
    pygame.mixer.music.stop()

def safe_wait(delay = 0, key = None, mouse = None):
    start = time.time()
    if key == None and mouse == None:
        while (time.time() - start < delay):
            for event in pygame.event.get():
                if event.type == pygame.locals.QUIT:
                    save_game()
                    pygame.quit()
                    sys.exit()
        return
    else:
        while True:
            for event in pygame.event.get():
                if event.type == KEYDOWN and key != None:
                    if event.key == key:
                        return
                if event.type == MOUSEBUTTONDOWN and mouse != None:
                    return event.pos
                if event.type == pygame.locals.QUIT:
                    save_game()
                    pygame.quit()
                    sys.exit()
    return

class WineGame:
    def __init__(self, windowSurface, window_width, window_height):
        self.windowSurface = windowSurface
        self.window_width = window_width
        self.window_height = window_height
        self.done = False
        self.front = pygame.image.load(assets+'cabinet_front.png')
        self.bottles = [[0,1,2,3], [4,5,6,7], [3,6,2,4], [7,1,1,2], [0,1,5,0], [4,8,5,5], [7,3,8,6], [8,0,3,4], [6,8,7,2], [], []]
        #self.bottles = [[0,0,0,0], [1,1,1,1], [2,2,2,2], [3,3,3,3], [4,4,4,4], [5,5,5,5], [6,6,6,6], [7,7,8,8], [8,8,7,7], [], []]
        self.colors = [(105, 17, 27), (117, 201, 113), (88, 25, 114), (227, 208, 117), (212, 150, 167), (155, 245, 255), (134, 113, 201), (227, 98, 51), (105, 157, 0)]
        self.selected = -1
        self.help_visible = False
        self.help_square = [1133, 60 ,55,55]
        self.continue_square = [109,550,317-109,598-550]

    def setup(self, skip_help = False):
        #set up the initial stuff
        background = pygame.image.load(assets+'emily_house.jpg')
        self.windowSurface.blit(background, (0,0))
        self.help_icon = pygame.image.load(assets+'help.png')
        self.backup_pos = (10,620)
        self.draw_bottles()
        self.backup_square = (self.backup_pos[0],self.backup_pos[1],100,75)
        self.won = False
        if not skip_help:
            self.display_help()
            play_song("emily",.25)
        return

    def draw_bottles(self):
        background = pygame.image.load(assets+'emily_house.jpg')
        self.windowSurface.blit(background, (0,0))
        pygame.draw.rect(self.windowSurface, (0,0,0), (362, 108, 919-362, 640-108))
        left_top = (391, 187)
        right_bot = (891, 367)
        width = (right_bot[0] - left_top[0])//6
        height = (right_bot[1] - left_top[1])//4
        squares = []
        for i in range(6):
            bottle = self.bottles[i]
            for j in range(len(bottle)):
                x = left_top[0] + width*i
                y = left_top[1] + height*(3-j)
                pygame.draw.rect(self.windowSurface, self.colors[bottle[j]], (x,y,width,height))
                square = [x,y,x+width, y+height]
            x = left_top[0] + width*i
            y = left_top[1]
            squares.append([x,y,x+width,y+height*4])
        left_top = (452, 438)
        right_bot = (830, 616)
        width = (right_bot[0] - left_top[0])//5
        height = (right_bot[1] - left_top[1])//4
        for i in range(5):
            bottle = self.bottles[6+i]
            for j in range(len(bottle)):
                x = left_top[0] + width*i
                y = left_top[1] + height*(3-j)
                pygame.draw.rect(self.windowSurface, self.colors[bottle[j]], (x,y,width,height))
                square = [x,y,x+width, y+height]
            x = left_top[0] + width*i
            y = left_top[1]
            squares.append([x,y,x+width,y+height*4])
        self.windowSurface.blit(self.front, (0,0))
        self.squares = squares
        self.highlight_bottle(self.selected)
        reset = pygame.image.load(assets+'reset.png')
        self.windowSurface.blit(reset, (0,0))
        self.windowSurface.blit(self.help_icon, [self.help_square[0],self.help_square[1]])
        backup = pygame.image.load(assets+'backup.png')
        self.windowSurface.blit(backup, self.backup_pos)
        return

    def highlight_bottle(self, i):
        if i < 0:
            return
        highlight = pygame.image.load(assets+'highlight'+str(i+1)+'.png')
        self.windowSurface.blit(highlight, (0,0))
        play_sound("click")

    def is_in(self, pos):
        count = 0
        for square in self.squares:
            if pos[0] >= square[0] and pos[0] <= square[2] and pos[1] >= square[1] and pos[1] <= square[3]:
                return count
            count = count + 1
        return -1

    def handle_click(self, pos):
        if self.help_visible:
            if self.is_in_single(pos, self.continue_square):
                self.hide_help()
                play_sound("click")
            return
        else:
            if self.is_in_single(pos, self.help_square):
                self.display_help()
                play_sound("click")
                return
            if self.is_in_single(pos, self.backup_square):
                self.done = True
                return
        reset = (1154, 636)
        if abs(pos[0] - reset[0]) < 50 and abs(pos[1] - reset[1]) < 50:
            self.__init__(self.windowSurface, self.window_width, self.window_height)
            self.setup(True)
            play_sound("click")
            return

        i = self.is_in(pos)
        if i == self.selected:
            i = -1
        old = self.selected
        self.selected = i
        src = self.bottles[old]
        if i == -1 or old == -1:
            self.draw_bottles()
            self.check_is_done()
            return
        dst = self.bottles[self.selected]
        if len(src) == 0:
            None
        elif len(dst) == 0:
            self.bottles[self.selected].append(src[len(src)-1])
            self.bottles[old] = src[0:-1]
            self.selected = -1
            play_sound("pour")
        elif len(dst) >= 4:
            self.draw_bottles()
            return
        elif dst[len(dst)-1] == src[len(src)-1]:
            self.bottles[self.selected].append(src[len(src)-1])
            self.bottles[old] = src[0:-1]
            self.selected = -1
            play_sound("pour")

        self.draw_bottles()
        self.check_is_done()

        return

    def check_is_done(self):
        for bottle in self.bottles:
            if len(bottle) != 0 and len(bottle) != 4:
                return
            if len(bottle) == 4:
                for i in range(1,4):
                    if bottle[i] != bottle[0]:
                        return
        self.done = True
        self.won = True
        play_sound("win")
        return

    def update(self):
        return
    def handle_move(self,pos):
        return
    def handle_release(self,pos):
        return
    def display_help(self):
        pygame.image.save(self.windowSurface, assets+"temp.jpg")
        help= pygame.image.load(assets+"wine_help.jpg")
        self.windowSurface.blit(help, (0,0))
        self.help_visible = True

    def hide_help(self):
        temp = pygame.image.load(assets+"temp.jpg")
        self.windowSurface.blit(temp, (0,0))
        self.help_visible = False
        backup = pygame.image.load(assets+'backup.png')
        self.windowSurface.blit(backup, self.backup_pos)

    def is_in_single(self, pos, square):
        if pos[0] >= square[0] and pos[0] <= square[0]+square[2] and pos[1] >= square[1] and pos[1] <= square[1]+square[3]:
            return True
        return False

class ElectricGame:
    def __init__(self, windowSurface, window_width, window_height):
        self.windowSurface = windowSurface
        self.window_width = window_width
        self.window_height = window_height
        self.done = False
        self.high = pygame.image.load(assets+'high.png')
        self.low = pygame.image.load(assets+'low.png')
        self.off = pygame.image.load(assets+'off.png')
        self.help_visible = False
        self.help_square = [1133, 60 ,55,55]
        self.continue_square = [125, 563, 335-125, 607-563]

    def setup(self, skip_help = False):
        #set up the initial stuff
        background = pygame.image.load(assets+'quentin_room.jpg')
        self.windowSurface.blit(background, (0,0))
        gray = pygame.image.load(assets+'gray_insert.png')
        self.windowSurface.blit(gray, (0,0))
        panel = pygame.image.load(assets+'panel.png')
        self.windowSurface.blit(panel, (0,0))
        reset = pygame.image.load(assets+'reset.png')
        self.windowSurface.blit(reset, (0,0))
        self.help_icon = pygame.image.load(assets+'help.png')
        self.windowSurface.blit(self.help_icon, [self.help_square[0],self.help_square[1]])
        self.backup_pos = (10,620)
        self.backup_square = (self.backup_pos[0],self.backup_pos[1],100,75)
        self.won = False

        square_size = 100
        buffer = 40

        left_top = (379, 120)
        size = 4*square_size+3*buffer
        #pygame.draw.rect(windowSurface, (128, 128, 128), (left_top[0]-25, left_top[1]-10, size+25*2, size+10*2))
        s = pygame.Surface((size+25*2,size+10*2))
        s.set_alpha(175)                # alpha level
        s.fill((128,128,128))
        self.windowSurface.blit(s, (left_top[0]-25, left_top[1]-10))

        squares = []

        for j in range(4):
            for i in range(4):
                x = left_top[0] + i*(square_size + buffer)
                y = left_top[1] + j*(square_size + buffer)
                #pygame.draw.rect(windowSurface, (128, 128, 128), (x,y, square_size, square_size))
                self.windowSurface.blit(self.high, (x,y))
                squares.append([x,y,x+square_size,y+square_size])
        self.squares = squares
        self.statuses = ["high" for square in self.squares]
        if not skip_help:
            self.display_help()
            play_song("quentin")
        else:
            backup = pygame.image.load(assets+'backup.png')
            self.windowSurface.blit(backup, self.backup_pos)
        return

    def is_in(self, pos):
        count = 0
        for square in self.squares:
            if pos[0] >= square[0] and pos[0] <= square[2] and pos[1] >= square[1] and pos[1] <= square[3]:
                return count
            count = count + 1
        return -1

    def handle_click(self, pos):
        if self.help_visible:
            if self.is_in_single(pos, self.continue_square):
                self.hide_help()
                play_sound("click")
            return
        else:
            if self.is_in_single(pos, self.help_square):
                self.display_help()
                play_sound("click")
                return
            if self.is_in_single(pos, self.backup_square):
                self.done = True
                return
        reset = (1154, 636)
        if abs(pos[0] - reset[0]) < 50 and abs(pos[1] - reset[1]) < 50:
            self.__init__(self.windowSurface, self.window_width, self.window_height)
            self.setup(True)
            play_sound("click")
            return
        i = self.is_in(pos)
        if i < 0:
            return
        play_sound("click")
        bb = [0, 4, -4]
        if i not in [3,7,11,15]:
            bb.append(1)
        if i not in [0,4,8,12]:
            bb.append(-1)
        for b in bb:
            self.inc_status(i+b)
        self.check_is_done()
        return

    def check_is_done(self):
        for status in self.statuses:
            if status != "off":
                return
        self.done = True
        self.won = True
        play_sound("win")
        return

    def inc_status(self, i):
        if i < 0 or i > 15:
            return
        x,y,_,_ = self.squares[i]
        if self.statuses[i] == "off":
            self.statuses[i] = "low"
            self.windowSurface.blit(self.low, (x,y))
        elif self.statuses[i] == "high":
            self.statuses[i] = "off"
            self.windowSurface.blit(self.off, (x,y))
        elif self.statuses[i] == "low":
            self.statuses[i] = "high"
            self.windowSurface.blit(self.high, (x,y))
        return
    def update(self):
        return
    def handle_move(self,pos):
        return
    def handle_release(self,pos):
        return
    def display_help(self):
        pygame.image.save(self.windowSurface, assets+"temp.jpg")
        help= pygame.image.load(assets+"power_help.jpg")
        self.windowSurface.blit(help, (0,0))
        self.help_visible = True

    def hide_help(self):
        temp = pygame.image.load(assets+"temp.jpg")
        self.windowSurface.blit(temp, (0,0))
        self.help_visible = False
        backup = pygame.image.load(assets+'backup.png')
        self.windowSurface.blit(backup, self.backup_pos)

    def is_in_single(self, pos, square):
        if pos[0] >= square[0] and pos[0] <= square[0]+square[2] and pos[1] >= square[1] and pos[1] <= square[1]+square[3]:
            return True
        return False

class MatchingGame:
    def __init__(self, windowSurface, window_width, window_height):
        self.windowSurface = windowSurface
        self.visible = []
        self.left = [i for i in range(15)]
        self.window_width = window_width
        self.window_height = window_height
        self.done = False
        self.help_visible = False
        self.help_square = [1133, 60 ,55,55]
        self.continue_square = [780,523,991-780,569-523]
    def setup(self, skip_help = False):
        #set up the initial stuff
        self.desktop = pygame.image.load(assets+'desktop2.jpg')
        self.windowSurface.blit(self.desktop, (0,0))
        positions = [[i,j] for j in range(3) for i in range(5)]
        random.shuffle(positions)
        back = pygame.image.load(assets+"back.jpg")
        left_top = (522, 212)
        #left_top = [290,260]
        spacing = (140 - 128)
        squares = []
        for i in range(15):
            x = left_top[0] + positions[i][0]*(128+spacing)
            y = left_top[1] + positions[i][1]*(128+spacing)
            self.windowSurface.blit(back, (x,y))
            square = [x, y, x+128, y+128, False] #left, top, right, bottom, matched?
            squares.append(square)
        self.squares = squares
        self.help_icon = pygame.image.load(assets+'help.png')
        self.windowSurface.blit(self.help_icon, [self.help_square[0],self.help_square[1]])
        self.backup_pos = (10,620)
        self.backup_square = (self.backup_pos[0],self.backup_pos[1],100,75)
        self.won = False
        self.need_update = False
        if not skip_help:
            self.display_help()
            play_song("hannah")
        return
    def is_in(self, pos):
        count = 0
        for square in self.squares:
            if pos[0] >= square[0] and pos[0] <= square[2] and pos[1] >= square[1] and pos[1] <= square[3]:
                if square[4] == False:
                    return count
                else:
                    return -1
            count = count + 1
        return -1
    def clear_all(self):
        self.windowSurface.blit(self.desktop, (0,0))
        image = pygame.image.load(assets+"back.jpg")
        for square in self.squares:
            x,y,_,_,matched = square
            if not matched:
                self.windowSurface.blit(image, (x,y))
        self.windowSurface.blit(self.help_icon, [self.help_square[0],self.help_square[1]])
        backup = pygame.image.load(assets+'backup.png')
        self.windowSurface.blit(backup, self.backup_pos)
        return

    def show_bias(self):
        #self.windowSurface.blit(self.desktop, (0,0))
        #image = pygame.image.load(assets+"card7.jpg")
        #x = self.window_width//2 - 128//2
        #y = self.window_height//2 - 128//2
        #self.windowSurface.blit(image, (x,y))
        self.done = True
        self.won = True
        play_sound("win")
        #safe_wait(key = 13, mouse = True)
        safe_wait(1)
        return

    def handle_click(self, pos):
        if self.help_visible:
            if self.is_in_single(pos, self.continue_square):
                self.hide_help()
                play_sound("click")
            return
        else:
            if self.is_in_single(pos, self.help_square):
                self.display_help()
                play_sound("click")
                return
            if self.is_in_single(pos, self.backup_square):
                self.done = True
                return
        square_i = self.is_in(pos)
        if square_i < 0:
            return
        if square_i in self.visible:
            self.clear_all()
            play_sound('flip')
            self.visible = []
            pygame.display.update()
            return
        square = self.squares[square_i]
        filename = assets+"card"+str(square_i%8)+".jpg"
        image = pygame.image.load(filename)
        x,y,_,_,_ = square
        self.windowSurface.blit(image, (x,y))
        self.visible.append(square_i)
        if len(self.left) == 1:
            pygame.display.update()
            time.sleep(.2)
            self.show_bias()
            return
        if len(self.visible) == 2:
            if self.visible[0]%8 == self.visible[1]%8:
                self.squares[self.visible[0]][4] = True
                self.squares[self.visible[1]][4] = True
                self.left.remove(self.visible[0])
                self.left.remove(self.visible[1])
                self.need_update = True
                #time.sleep(.2)
                #self.visible = []
                #self.clear_all()
                play_sound('match')
            else:
                play_sound('flip')
        else:
            play_sound("flip")

        if len(self.visible) >= 2:
            self.need_update = True

        return
    def update(self):
        if self.need_update != True:
            return
        safe_wait(.7)
        self.clear_all()
        self.visible = []
        self.need_update = False

        return
    def handle_move(self,pos):
        return
    def handle_release(self,pos):
        return
    def display_help(self):
        pygame.image.save(self.windowSurface, assets+"temp.jpg")
        help= pygame.image.load(assets+"matching_help.jpg")
        self.windowSurface.blit(help, (0,0))
        self.help_visible = True

    def hide_help(self):
        temp = pygame.image.load(assets+"temp.jpg")
        self.windowSurface.blit(temp, (0,0))
        self.help_visible = False
        backup = pygame.image.load(assets+'backup.png')
        self.windowSurface.blit(backup, self.backup_pos)

    def is_in_single(self, pos, square):
        if pos[0] >= square[0] and pos[0] <= square[0]+square[2] and pos[1] >= square[1] and pos[1] <= square[1]+square[3]:
            return True
        return False

class MosaicGame:
    def __init__(self, windowSurface, window_width, window_height):
        loading = pygame.image.load(assets+'mosaic_loading.jpg')
        windowSurface.blit(loading, (0,0))
        pygame.display.update()
        self.windowSurface = windowSurface
        self.window_width = window_width
        self.window_height = window_height
        self.regions = np.array(Image.open(assets+"regions.bmp"))[:,:,2]
        pos_vals = [0,1,2,5,7,9,10,11,12,13,14,16,17,19,20,22,23,24,25,27,28,29,30,31,32,34,35,36,37,38,39,40,41,43,44,45,46,47,48,49,50,51,52,54,58,59,60,62,63,64,65,66,67,68,69,70,72,73,74,75,77,79,81,82,83,85,86,89,90,91,92,93,94,95,96,97,98,101,102,103,104,105,107,108,109,110,112,113,115,116,117,118,119,120,122,124,125,126,128,129,130,131,132,133,134,135,136,137,138,139,140,141,143,146,147]
        Z = np.zeros(self.regions.shape)
        kernel = np.ones((5,5),np.uint8)
        for v in pos_vals:
            R = (self.regions == v).astype(np.float32())
            O = cv2.morphologyEx(R, cv2.MORPH_OPEN, kernel)
            Z = Z + O*(v+1)
        self.regions = Z

        #self.solution = np.array(Image.open(assets+"solution.bmp").crop((58,29,737,700))).astype(int)
        #self.solution = np.array(Image.open(assets+"solution.bmp").crop((0,0,737,700))).astype(int)
        self.solution = np.array(Image.open(assets+"solution.bmp")).astype(int)
        self.outline = desktop = pygame.image.load(assets+"thick_outline.png")
        self.done = False
        self.colors = [[250, 250, 0], [213, 0, 220], [255, 114, 0], [255, 10, 0], [0, 255, 85], [0, 53, 190], [0, 255, 255], [128, 128, 128]]
        self.names = ["Hope", "Lauren", "Tim", "Quentin", "Hannah", "Emily", "Azriel", "Remove"]
        self.current_color = 0
        self.font = pygame.font.SysFont('Comic Sans MS', 20)
        self.done = False
        self.correct = []
        self.texture = np.array(Image.open(assets+"texture.png"))/255
        self.help_visible = False
        self.help_square = [35, 37 ,55,55]
        self.continue_square = [511,578,722-511,627-578]
        self.current_vals = []

    def setup(self, skip_help = False):
        #set up the initial stuff
        desktop = pygame.image.load(assets+'wood.jpg')
        self.windowSurface.blit(desktop, (0,0))
        blank = pygame.image.load(assets+'blank2.png')
        self.windowSurface.blit(blank, (0,0))
        self.windowSurface.blit(self.outline, (0,0))
        self.make_menu()
        reset = pygame.image.load(assets+'reset.png')
        self.windowSurface.blit(reset, (0,0))
        self.help_icon = pygame.image.load(assets+'help.png')
        self.windowSurface.blit(self.help_icon, [self.help_square[0],self.help_square[1]])
        self.backup_pos = (10,620)
        self.backup_square = (self.backup_pos[0],self.backup_pos[1],100,75)
        self.won = False
        if not skip_help:
            self.display_help()
            play_song("mallory")
        return

    def make_menu(self):
        wood = pygame.image.load(assets+'menu_wood.png')
        self.windowSurface.blit(wood, (0,0))
        left_top = (810, 80)
        bot = 580
        square_size = (bot - left_top[1])//4
        colors = self.colors
        names = self.names
        squares = []
        c = 0
        for i in range(4):
            for j in range(2):
                x = left_top[0] + j*(square_size+20)
                y = left_top[1] + i*(square_size+20)
                coords = [x-5,y-5, square_size+10, square_size+10]
                #pygame.draw.rect(self.windowSurface, colors[c], coords)
                if c == self.current_color:
                    pygame.draw.rect(self.windowSurface, (255,255,255), coords)
                spool = pygame.image.load(assets+self.names[c].lower()+'_spool.png')
                self.windowSurface.blit(spool, (x,y))
                #name_surface = self.font.render(names[c], False, (0,0,0))
                #self.windowSurface.blit(name_surface,(x+20,y+20))
                square = [x,y, x+square_size, y+square_size]
                squares.append(square)
                c = c + 1
        self.squares = squares

    def make_RBGA(self, I):
        rgbArray = np.zeros((I.shape[0],I.shape[1],4), 'int')
        rgbArray[..., 0] = I//255*self.colors[self.current_color][0]
        rgbArray[..., 1] = I//255*self.colors[self.current_color][1]
        rgbArray[..., 2] = I//255*self.colors[self.current_color][2]
        if self.current_color != 7:
            rgbArray = rgbArray * self.texture
        rgbArray[..., 3] = (I > 0).astype('int')*255
        rgbArray = rgbArray.astype('uint8')
        img = Image.fromarray(rgbArray)
        return img

    def paste_image(self, image):
        #where image is PIL image
        raw_str = image.tobytes("raw", 'RGBA')
        pygame_surface = pygame.image.fromstring(raw_str, image.size, 'RGBA')
        self.windowSurface.blit(pygame_surface, (0,0))
    def is_in(self, pos):
        count = 0
        for square in self.squares:
            if pos[0] >= square[0] and pos[0] <= square[2] and pos[1] >= square[1] and pos[1] <= square[3]:
                return count
            count = count + 1
        return -1
    def handle_click(self, pos):
        if self.help_visible:
            if self.is_in_single(pos, self.continue_square):
                self.hide_help()
                play_sound("click")
            return
        else:
            if self.is_in_single(pos, self.help_square):
                self.display_help()
                play_sound("click")
                return
            if self.is_in_single(pos, self.backup_square):
                self.done = True
                return
        reset = (1154, 636)
        if abs(pos[0] - reset[0]) < 50 and abs(pos[1] - reset[1]) < 50:
            self.__init__(self.windowSurface, self.window_width, self.window_height)
            self.setup(True)
            play_sound("click")
            return
        val = self.regions[(pos[1],pos[0])]
        if val > 250 or val == 0:
            i = self.is_in(pos)
            if i >= 0:
                self.current_color = i
                play_sound("click")
            self.make_menu()
            return
        a = self.solution[(pos[1],pos[0])].astype(int)
        if a.sum() < 210:
            #print("black","asum",a.sum(),"a",a)
            return #black area
        to_paste = (self.regions == val).astype(int)*255
        to_paste = self.make_RBGA(to_paste)
        self.paste_image(to_paste)
        self.windowSurface.blit(self.outline, (0,0))
        b = np.array(self.colors[self.current_color]).astype(int)
        diff = sum([abs(d) for d in (a-b).flatten()])
        #print((self.regions == val).astype(int).sum(), diff < 30 and val not in self.correct, diff)
        self.current_vals.append(val)
        play_sound("sew")
        #print("diff",diff,"val",val,"asum",a.sum(),"a",a)
        if diff < 90:
            if val not in self.correct:
                self.correct.append(val)
                #play_sound("win")
        else:
            #play_sound("invalid")
            if val in self.correct:
                self.correct.remove(val)
                #play_sound("kill")

        #print(len(self.correct))
        #print(len(self.correct))
        self.check_if_won()

        return
    def check_if_won(self):
        #24 per piece
        #6*24 = 144
        #29 starters
        #144 - 30 = 114
        #print(len(self.correct))
        if len(self.correct) == 115:
            self.done = True
            self.won = True
            play_sound("win")
        return
    def update(self):
        return
    def handle_move(self,pos):
        return
    def handle_release(self,pos):
        return
    def display_help(self):
        pygame.image.save(self.windowSurface, assets+"temp.jpg")
        help= pygame.image.load(assets+"mosaic_help.jpg")
        self.windowSurface.blit(help, (0,0))
        self.help_visible = True

    def hide_help(self):
        #self.draw_all()
        temp = pygame.image.load(assets+"temp.jpg")
        self.windowSurface.blit(temp, (0,0))
        self.help_visible = False
        backup = pygame.image.load(assets+'backup.png')
        self.windowSurface.blit(backup, self.backup_pos)

    def is_in_single(self, pos, square):
        if pos[0] >= square[0] and pos[0] <= square[0]+square[2] and pos[1] >= square[1] and pos[1] <= square[1]+square[3]:
            return True
        return False

class FelonyEscape:
    def __init__(self, windowSurface, window_width, window_height):
        self.windowSurface = windowSurface
        self.window_width = window_width
        self.window_height = window_height
        self.done = False
        self.cop_i = 3
        self.you_i = 14
        self.need_update = False
        self.help_visible = False
        self.help_square = [35, 37 ,55,55]
        self.continue_square = [268, 568, 478-268, 617-568]

    def setup(self, skip_help = False):
        #set up the initial stuff
        background = pygame.image.load(assets+'lauren_room.jpg')
        self.windowSurface.blit(background, (0,0))
        self.phone = pygame.image.load(assets+'phone.png')
        self.windowSurface.blit(self.phone, (0,0))
        self.reset = pygame.image.load(assets+'reset.png')
        self.windowSurface.blit(self.reset, (0,0))
        self.you = pygame.image.load(assets+'pink.png')
        self.cop = pygame.image.load(assets+'red.png')
        self.help_icon = pygame.image.load(assets+'help.png')
        self.windowSurface.blit(self.help_icon, [self.help_square[0],self.help_square[1]])
        self.backup_pos = (10,620)
        self.backup_square = (self.backup_pos[0],self.backup_pos[1],100,75)
        self.won = False

        grid = []
        square_size = 100
        buffer = 40

        left_top = (247, 148)
        width = 90
        height = 85
        for j in range(5):
            for i in range(7):
                x = left_top[0] + i*width
                y = left_top[1] + j*height
                #pygame.draw.rect(self.windowSurface, (random.randint(0,255), random.randint(0,255), random.randint(0,255)), (x,y,width,height))
                grid.append((x,y))
        self.grid = grid
        self.can_go = []

        self.can_go.append([2,3])
        self.can_go.append([1,2,3])
        self.can_go.append([1,2])
        self.can_go.append([1])
        self.can_go.append([2,3])
        self.can_go.append([1,2,3])
        self.can_go.append([1])

        self.can_go.append([0,3])
        self.can_go.append([0,2,3])
        self.can_go.append([1,2])
        self.can_go.append([1])
        self.can_go.append([0,3])
        self.can_go.append([0,3])
        self.can_go.append([3])

        self.can_go.append([0,3])
        self.can_go.append([0])
        self.can_go.append([2,3])
        self.can_go.append([1,2,3])
        self.can_go.append([0,1])
        self.can_go.append([0,2,3])
        self.can_go.append([0,1,3])

        self.can_go.append([0,3])
        self.can_go.append([2,3])
        self.can_go.append([0,1,3])
        self.can_go.append([0,2,3])
        self.can_go.append([1,2])
        self.can_go.append([0,1])
        self.can_go.append([0,3])

        self.can_go.append([0,2])
        self.can_go.append([0,1])
        self.can_go.append([0,2])
        self.can_go.append([0,1,2])
        self.can_go.append([1])
        self.can_go.append([2])
        self.can_go.append([0,1])

        self.draw_positions()

        #buttons
        self.squares = []
        self.squares.append([938,289,1006,328])
        self.squares.append([893,340,960,380])
        self.squares.append([980,340,1047,380])
        self.squares.append([938,384,1006,434])
        for square in self.squares:
            x,y,x1,y1 = square
            rect = [x,y,x1-x,y1-y]
        if not skip_help:
            self.display_help()
            play_song("lauren")
        return

    def draw_positions(self):
        self.windowSurface.blit(self.phone, (0,0))
        self.windowSurface.blit(self.reset, (0,0))
        self.windowSurface.blit(self.you, self.grid[self.you_i])
        self.windowSurface.blit(self.cop, self.grid[self.cop_i])
        backup = pygame.image.load(assets+'backup.png')
        self.windowSurface.blit(backup, self.backup_pos)
        return

    def draw_all(self):
        background = pygame.image.load(assets+'lauren_room.jpg')
        self.windowSurface.blit(background, (0,0))
        self.windowSurface.blit(self.help_icon, [self.help_square[0],self.help_square[1]])
        self.draw_positions()
        return

    def is_in(self, pos):
        count = 0
        for square in self.squares:
            if pos[0] >= square[0] and pos[0] <= square[2] and pos[1] >= square[1] and pos[1] <= square[3]:
                return count
            count = count + 1
        return -1

    def handle_click(self, pos):
        if self.help_visible:
            if self.is_in_single(pos, self.continue_square):
                self.hide_help()
                play_sound("click")
            return
        else:
            if self.is_in_single(pos, self.help_square):
                self.display_help()
                play_sound("click")
                return
            if self.is_in_single(pos, self.backup_square):
                self.done = True
                return
        reset = (1154, 636)
        if abs(pos[0] - reset[0]) < 50 and abs(pos[1] - reset[1]) < 50:
            self.__init__(self.windowSurface, self.window_width, self.window_height)
            self.setup(True)
            play_sound("click")
            return
        i = self.is_in(pos)
        if i < 0:
            return
        if i in self.can_go[self.you_i]:
            if i == 0:
                self.you_i = self.you_i - 7
            elif i == 1:
                self.you_i = self.you_i - 1
            elif i == 2:
                self.you_i = self.you_i + 1
            elif i == 3:
                self.you_i = self.you_i + 7
        else:
            play_sound("invalid")
            return
        self.update_cop()
        self.draw_all()
        self.check_is_done()
        return

    def update_cop(self):
        play_sound("slide")
        #self.need_update = True
        #return
        self.need_update = True
        you_col = self.you_i%7
        you_row = (self.you_i)//7
        cop_col = self.cop_i%7
        cop_row = (self.cop_i)//7
        if you_col < cop_col and 1 in self.can_go[self.cop_i]:
            self.cop_i = self.cop_i - 1
        elif you_col > cop_col and 2 in self.can_go[self.cop_i]:
            self.cop_i = self.cop_i + 1
        elif you_row < cop_row and 0 in self.can_go[self.cop_i]:
            self.cop_i = self.cop_i - 7
        elif you_row > cop_row and 3 in self.can_go[self.cop_i]:
            self.cop_i = self.cop_i + 7
        else:
            self.need_update = False
        if self.cop_i == self.you_i:
            self.__init__(self.windowSurface, self.window_width, self.window_height)
            self.setup(True)
            play_sound('kill')
            return

        return

    def check_is_done(self):
        if self.you_i == 3:
            self.done = True
            play_sound("win")
            self.won = True
        return

    def update(self):
        if self.need_update != True:
            return
        self.need_update = False
        you_col = self.you_i%7
        you_row = (self.you_i)//7
        cop_col = self.cop_i%7
        cop_row = (self.cop_i)//7
        if you_col < cop_col and 1 in self.can_go[self.cop_i]:
            self.cop_i = self.cop_i - 1
        elif you_col > cop_col and 2 in self.can_go[self.cop_i]:
            self.cop_i = self.cop_i + 1
        elif you_row < cop_row and 0 in self.can_go[self.cop_i]:
            self.cop_i = self.cop_i - 7
        elif you_row > cop_row and 3 in self.can_go[self.cop_i]:
            self.cop_i = self.cop_i + 7
        else:
            return
        safe_wait(.3)
        if self.cop_i == self.you_i:
            self.__init__(self.windowSurface, self.window_width, self.window_height)
            self.setup(True)
            play_sound('kill')
            return
        self.draw_positions()
        self.check_is_done()
    def handle_move(self,pos):
        return
    def handle_release(self,pos):
        return
    def display_help(self):
        help= pygame.image.load(assets+"escape_help.jpg")
        self.windowSurface.blit(help, (0,0))
        self.help_visible = True

    def hide_help(self):
        self.draw_all()
        self.help_visible = False
        backup = pygame.image.load(assets+'backup.png')
        self.windowSurface.blit(backup, self.backup_pos)

    def is_in_single(self, pos, square):
        if pos[0] >= square[0] and pos[0] <= square[0]+square[2] and pos[1] >= square[1] and pos[1] <= square[1]+square[3]:
            return True
        return False

class CookieGame:
    def __init__(self, windowSurface, window_width, window_height):
        self.windowSurface = windowSurface
        self.window_width = window_width
        self.window_height = window_height
        self.done = False
        self.help_visible = False
        self.help_square = [965, 39 ,55,55]
        self.continue_square = [955,355,1170-955,408-355]

    def setup(self, skip_help = False):
        #set up the initial stuff
        self.background = pygame.image.load(assets+'hope_room.jpg')
        self.windowSurface.blit(self.background, (0,0))
        self.cookie_display = pygame.image.load(assets+'cookie_display.png')
        self.windowSurface.blit(self.cookie_display, (0,0))
        self.reset = pygame.image.load(assets+'reset.png')
        self.windowSurface.blit(self.reset, (50, 40))
        self.help_icon = pygame.image.load(assets+'help.png')
        self.windowSurface.blit(self.help_icon, [self.help_square[0],self.help_square[1]])
        self.backup_pos = (383,17)
        self.backup_square = (self.backup_pos[0],self.backup_pos[1],100,75)
        self.won = False
        self.pressed = False
        self.selected = -1
        width = 137
        height = 133
        left_top = (45,24)
        count = 0
        filenames = ["chip_heart.png","choc_heart.png","suga_heart.png","chip_star.png","choc_star.png","suga_star.png","chip_moon.png","choc_moon.png","suga_moon.png"]
        #C1 A1 B1 C2 A2 B2 C3 A3 B3
        # 0  1  2  3  4  5  6  7  8
        #4 5 2
        #3 0 6
        #1 7 8
        self.answer = [4,5,2,3,0,6,1,7,8]
        self.current = [-1 for i in self.answer]

        shadows = ["heart.png","heart.png","heart.png","star.png","star.png","star.png","moon.png","moon.png","moon.png"]
        squares = []
        self.cookies = []
        self.shadows = []
        for j in range(5):
            for i in range(2):
                if count < 9:
                    x = left_top[0] + i*width
                    y = left_top[1] + j*height
                    shadow = pygame.image.load(assets+shadows[count])
                    self.windowSurface.blit(shadow, (x+5,y+5))
                    cookie = pygame.image.load(assets+filenames[count])
                    self.windowSurface.blit(cookie, (x,y))
                    squares.append([x,y,width,height])
                    self.cookies.append(cookie)
                    self.shadows.append(shadow)
                count = count + 1
        self.squares = squares
        left_top = (457, 173)
        dests = []
        for j in range(3):
            for i in range(3):
                x = left_top[0] + i*width
                y = left_top[1] + j*height
                dests.append([x,y,width,height])
        self.dests = dests
        if not skip_help:
            self.display_help()
            play_song("hope")
        return
    def display_help(self):
        help= pygame.image.load(assets+"cookie_help.jpg")
        self.windowSurface.blit(help, (0,0))
        self.help_visible = True

    def hide_help(self):
        self.draw_all()
        self.help_visible = False
        backup = pygame.image.load(assets+'backup.png')
        self.windowSurface.blit(backup, self.backup_pos)

    def is_in(self, pos):
        count = 0
        for square in self.squares:
            if pos[0] >= square[0] and pos[0] <= square[0]+square[2] and pos[1] >= square[1] and pos[1] <= square[1]+square[3]:
                return count
            count = count + 1
        return -1

    def is_in_single(self, pos, square):
        if pos[0] >= square[0] and pos[0] <= square[0]+square[2] and pos[1] >= square[1] and pos[1] <= square[1]+square[3]:
            return True
        return False

    def handle_click(self, pos):
        #print(pos)
        if self.help_visible:
            if self.is_in_single(pos, self.continue_square):
                self.hide_help()
                play_sound("click")
        else:
            if self.is_in_single(pos, self.help_square):
                self.display_help()
                play_sound("click")
                return
            if self.is_in_single(pos, self.backup_square):
                self.done = True
                return
            reset = [1154, 636]
            reset[0] = reset[0] + 50
            reset[1] = reset[1] + 40
            if abs(pos[0] - reset[0]) < 50 and abs(pos[1] - reset[1]) < 50:
                self.__init__(self.windowSurface, self.window_width, self.window_height)
                self.setup(True)
                play_sound("click")
                return
            i = self.is_in(pos)
            if i < 0:
                return
            self.pressed = True
            self.selected = i
            return

    def handle_move(self, pos):
        if self.pressed:
            x,y,w,h = self.squares[self.selected]
            self.squares[self.selected] = [pos[0] - w//2, pos[1] - h//2, w, h]
            self.draw_all()
        return

    def handle_release(self, pos):
        if self.pressed:
            play_sound("cookie")
            count = 0
            min_dist = float('inf')
            min_count = 0
            for square in self.dests:
                x,y,w,h = square
                centx = x + w//2
                centy = y + h//2
                dist = (centx - pos[0])**2 + (centy - pos[1])**2
                if dist < min_dist:
                    min_dist = dist
                    min_count = count
                count = count + 1
            #print(min_count, dist)
            min_dist = math.sqrt(min_dist)
            if min_dist < 100:
                self.squares[self.selected] = self.dests[min_count]
                self.draw_all()
                self.current[min_count] = self.selected
                self.check_is_done()
            else:
                for i in range(len(self.current)):
                    if self.current[i] == self.selected:
                        self.current[i] = -1
        self.pressed = False
        return

    def draw_all(self):
        self.windowSurface.blit(self.background, (0,0))
        self.windowSurface.blit(self.cookie_display, (0,0))
        self.windowSurface.blit(self.reset, (50, 40))
        for i in range(8,-1,-1):
            x,y,_,_ = self.squares[i]
            cookie = self.cookies[i]
            shadow = self.shadows[i]
            self.windowSurface.blit(shadow, (x+5,y+5))
            self.windowSurface.blit(cookie, (x,y))
        self.windowSurface.blit(self.help_icon, [self.help_square[0],self.help_square[1]])
        backup = pygame.image.load(assets+'backup.png')
        self.windowSurface.blit(backup, self.backup_pos)
        return

    def check_is_done(self):
        if self.current == self.answer:
            self.done = True
            play_sound('win')
            self.won = True
        return

    def update(self):
        return

class ScheduleGame:
    def __init__(self, windowSurface, window_width, window_height):
        self.windowSurface = windowSurface
        self.window_width = window_width
        self.window_height = window_height
        self.done = False
        self.help_visible = False
        self.help_square = [965, 39 ,55,55]
        self.continue_square = [955,307,1170-955,408-355]

    def setup(self, skip_help = False):
        #set up the initial stuff
        self.background = pygame.image.load(assets+'tim_room.jpg')
        self.windowSurface.blit(self.background, (0,0))
        self.schedule_display = pygame.image.load(assets+'overlay.png')
        self.windowSurface.blit(self.schedule_display, (0,0))
        self.reset = pygame.image.load(assets+'reset.png')
        self.windowSurface.blit(self.reset, (50, 40))
        self.help_icon = pygame.image.load(assets+'help.png')
        self.windowSurface.blit(self.help_icon, [self.help_square[0],self.help_square[1]])
        self.pressed = False
        self.selected = -1
        width = 400
        height = 50
        left_top = (18,24)
        count = 0
        filenames = [str(i)+".png" for i in range(6)]
        self.answer = [5,0,4,2,1,3]
        self.current = [-1 for i in self.answer]
        self.backup_pos = (10,620)
        self.backup_square = (self.backup_pos[0],self.backup_pos[1],100,75)
        self.won = False

        squares = []
        self.panels = []
        for i in range(6):
            x = left_top[0]
            y = left_top[1] + i*(height+30)
            panel = pygame.image.load(assets+filenames[i])
            self.windowSurface.blit(panel, (x,y))
            squares.append([x,y,width,height])
            self.panels.append(panel)
        self.squares = squares

        left_top = (530, 238)
        dests = []
        for i in range(6):
            x = left_top[0]
            y = left_top[1] + i*69
            squares.append([x,y,x+400,y+50])
            dests.append([x,y,400,50])

        self.dests = dests
        if not skip_help:
            self.display_help()
            play_song("tim")
        else:
            backup = pygame.image.load(assets+'backup.png')
            self.windowSurface.blit(backup, self.backup_pos)
        return

    def display_help(self):
        help= pygame.image.load(assets+"schedule_help.jpg")
        self.windowSurface.blit(help, (0,0))
        self.help_visible = True

    def hide_help(self):
        self.draw_all()
        self.help_visible = False
        backup = pygame.image.load(assets+'backup.png')
        self.windowSurface.blit(backup, self.backup_pos)

    def is_in(self, pos):
        count = 0
        for square in self.squares:
            if pos[0] >= square[0] and pos[0] <= square[0]+square[2] and pos[1] >= square[1] and pos[1] <= square[1]+square[3]:
                return count
            count = count + 1
        return -1

    def is_in_single(self, pos, square):
        if pos[0] >= square[0] and pos[0] <= square[0]+square[2] and pos[1] >= square[1] and pos[1] <= square[1]+square[3]:
            return True
        return False

    def handle_click(self, pos):
        #print(pos)
        if self.help_visible:
            if self.is_in_single(pos, self.continue_square):
                self.hide_help()
                play_sound("click")
        else:
            if self.is_in_single(pos, self.help_square):
                self.display_help()
                play_sound("click")
                return
            if self.is_in_single(pos, self.backup_square):
                self.done = True
                return
            reset = [1154, 636]
            reset[0] = reset[0] + 50
            reset[1] = reset[1] + 40
            if abs(pos[0] - reset[0]) < 50 and abs(pos[1] - reset[1]) < 50:
                self.__init__(self.windowSurface, self.window_width, self.window_height)
                self.setup(True)
                play_sound("click")
                return
            i = self.is_in(pos)
            if i < 0:
                return
            self.pressed = True
            self.selected = i
            return

    def handle_move(self, pos):
        if self.pressed:
            x,y,w,h = self.squares[self.selected]
            self.squares[self.selected] = [pos[0] - w//2, pos[1] - h//2, w, h]
            self.draw_all()
        return

    def handle_release(self, pos):
        if self.pressed:
            play_sound("cookie")
            count = 0
            min_dist = float('inf')
            min_count = 0
            for square in self.dests:
                x,y,w,h = square
                centx = x + w//2
                centy = y + h//2
                dist = (centx - pos[0])**2 + (centy - pos[1])**2
                if dist < min_dist:
                    min_dist = dist
                    min_count = count
                count = count + 1
            #print(min_count, dist)
            min_dist = math.sqrt(min_dist)
            if min_dist < 100:
                self.squares[self.selected] = self.dests[min_count]
                self.draw_all()
                self.current[min_count] = self.selected
                self.check_is_done()
            else:
                for i in range(len(self.current)):
                    if self.current[i] == self.selected:
                        self.current[i] = -1
        self.pressed = False
        return

    def draw_all(self):
        self.windowSurface.blit(self.background, (0,0))
        self.windowSurface.blit(self.schedule_display, (0,0))
        self.windowSurface.blit(self.reset, (50, 40))
        for i in range(5,-1,-1):
            x,y,_,_ = self.squares[i]
            panel = self.panels[i]
            self.windowSurface.blit(panel, (x,y))
        self.windowSurface.blit(self.help_icon, [self.help_square[0],self.help_square[1]])
        backup = pygame.image.load(assets+'backup.png')
        self.windowSurface.blit(backup, self.backup_pos)
        return

    def check_is_done(self):
        if self.current == self.answer:
            self.done = True
            self.won = True
            play_sound('win')
        return

    def update(self):
        return

class KeyPuzzle:
        def __init__(self, windowSurface, window_width, window_height, clues):
            self.windowSurface = windowSurface
            self.window_width = window_width
            self.window_height = window_height
            self.clues = clues
            self.num_clues = len(clues)
            self.won = False
            self.done = False
            self.current = ""
            self.need_update = False

        def setup(self, skip_help = False):
            #set up the initial stuff
            self.font = pygame.font.SysFont('Comic Sans MS', 30)
            self.draw_all()
            squares = []
            square_size = 40
            xx = [936,880, 941, 1002, 876,938,999,875,942,1002]
            yy = [368,176,180,176,240,241,242,296,303,307]
            for i in range(10):
                x = xx[i]
                y = yy[i]
                #pygame.draw.rect(self.windowSurface, (128, 128, 128), (x,y, square_size, square_size))
                #self.windowSurface.blit(self.high, (x,y))
                squares.append([x,y,x+square_size,y+square_size])
            self.squares = squares
            backup = pygame.image.load(assets+'backup.png')
            self.windowSurface.blit(backup, self.backup_pos)
            return

        def draw_all(self):
            background = pygame.image.load(assets+'hannah_front_door.jpg')
            self.windowSurface.blit(background, (0,0))
            lock = pygame.image.load(assets+'lock.png')
            self.windowSurface.blit(lock, (0,0))
            self.backup_pos = (10,620)
            self.backup_square = (self.backup_pos[0],self.backup_pos[1],100,75)
            clue_pos_x = 125
            clue_pos_yy = [124, 317, 525]
            for i in range(self.num_clues):
                clue = pygame.image.load(assets+"clue"+str(i)+'.png')
                self.windowSurface.blit(clue, (0,0))
                text = self.font.render(self.clues[i], True, (0,0,0))
                self.windowSurface.blit(text, (clue_pos_x,clue_pos_yy[i],0,0))
            backup = pygame.image.load(assets+'backup.png')
            self.windowSurface.blit(backup, self.backup_pos)
            return

        def is_in(self, pos):
            count = 0
            for square in self.squares:
                if pos[0] >= square[0] and pos[0] <= square[2] and pos[1] >= square[1] and pos[1] <= square[3]:
                    return count
                count = count + 1
            return -1

        def handle_click(self, pos):
            if self.is_in_single(pos, self.backup_square):
                self.done = True
                return
            i = self.is_in(pos)
            if i < 0:
                return
            play_sound("click")
            self.current = self.current + str(i)
            if len(self.current) == 3:
                self.need_update = True
            text = self.font.render(self.current, True, (255,255,255))
            self.windowSurface.blit(text, (882,124,0,0))
            return

        def check_is_done(self):
            if self.current != "731" or self.num_clues != 3:
                    return
            self.done = True
            self.won = True
            play_sound("win")
            return

        def update(self):
            if self.need_update:
                safe_wait(.5)
                self.check_is_done()
                self.draw_all()
                if self.current != "731":
                    play_sound("invalid")
                self.current = ""

                #print('do an update')
                self.need_update = False
            return
        def handle_move(self,pos):
            return
        def handle_release(self,pos):
            return
        def is_in_single(self, pos, square):
            if pos[0] >= square[0] and pos[0] <= square[0]+square[2] and pos[1] >= square[1] and pos[1] <= square[1]+square[3]:
                return True
            return False

# set up the window
window_width = 1280
window_height = 720
windowSurface = pygame.display.set_mode((window_width, window_height), 0, 32)
pygame.display.set_caption('Save Mallory')
'''END PYGAME SETUP'''

'''runs a game with a given name'''
#def run_game(game_name):
def run_game(Game):
    #games = [ScheduleGame,CookieGame, FelonyEscape, WineGame, ElectricGame, MatchingGame, MosaicGame]
    #names = ["ScheduleGame","CookieGame", "FelonyEscape", "WineGame", "ElectricGame", "MatchingGame", "MosaicGame"]
    #Game = games[names.index(game_name)]
    if Game != KeyPuzzle:
        G = Game(windowSurface, window_width, window_height)
    else:
        G = Game(windowSurface, window_width, window_height, clues)
    G.setup()
    pygame.display.update()
    keyword = ""
    passcode = "jojobestboy"
    # run the game loop
    while not G.done:
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONDOWN:
                #print(event.pos)
                G.handle_click(event.pos)
                pygame.display.update()
                G.update()
            if event.type == MOUSEMOTION:
                G.handle_move(event.pos)
            if event.type == MOUSEBUTTONUP:
                G.handle_release(event.pos)
            if event.type == QUIT:
                save_game()
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                keyword = keyword + event.unicode
                if len(keyword) >= len(passcode):
                    diff = len(keyword) - len(passcode)
                    keyword = keyword[diff:]
                if keyword == passcode:
                    G.done = True
                    G.won = True
            pygame.display.update()
    stop_song()
    return G.won

'''dialog functions'''
class SceneHandler:
    def __init__(self):
        self.windowSurface = windowSurface
        self.window_width = window_width
        self.window_height = window_height
        self.font = pygame.font.SysFont('Comic Sans MS', 30)
        self.top = int(window_height*.8)
        self.buffer = int(window_height*.07)
        self.background = None
        self.speaker = None

    def set_background(self, filename):
        final_filename = assets+filename+".jpg"
        self.background = pygame.image.load(final_filename)
        pygame.display.update()
        return

    def set_speaker(self, filename):
        self.speaker = pygame.image.load(sprites+filename+".png")
        return

    def display_choice(self, choices, custom_squares = None):
        left_top = (300, 40)
        width = 1280 - left_top[0]*2
        height = 70
        buffer = 20
        x = left_top[0]
        squares = []
        if custom_squares is None:
            for i in range(len(choices)):
                y = left_top[1] + i*(height + buffer)
                s = pygame.Surface((width,height))
                s.set_alpha(200)                # alpha level
                s.fill((0,100,255))
                self.windowSurface.blit(s, (x,y))
                squares.append((x,y,width+x,height+y))
                text = self.font.render(choices[i], True, (255,255,255))
                textRect = text.get_rect()
                textRect.centerx = x + width//2
                textRect.centery = y + height//2
                self.windowSurface.blit(text, textRect)
        else:
            squares = custom_squares
        pygame.display.update()
        i = -1
        while i < 0:
            pos = safe_wait(mouse = True)
            x,y = pos
            j = 0
            while j < len(squares):
                x1,y1,x2,y2 = squares[j]
                if x >= x1 and x <= x2 and y >= y1 and y <= y2:
                    i = j
                    break
                j = j + 1
        play_sound("click")
        return i

    def display_line(self, speaker, line, wait = True):
        self.windowSurface.fill((0,0,0))
        if self.background != None:
            self.windowSurface.blit(self.background, (0,0))
        if self.speaker != None:
            self.windowSurface.blit(self.speaker, (0,0))
        s = pygame.Surface((self.window_width,(self.window_height - self.top)))
        s.set_alpha(200)                # alpha level
        s.fill((0,0,0))
        windowSurface.blit(s, (0,self.top))
        speaker_surface = self.font.render(speaker, False, (0, 255, 255))
        line_surface = self.font.render(line, False, (0, 255, 0))
        self.windowSurface.blit(speaker_surface,(self.buffer,self.top))
        self.windowSurface.blit(line_surface,(self.buffer,self.top+self.buffer))
        pygame.display.update()
        if wait:
            safe_wait(key = 13, mouse = True)
        #play_sound("click")
        return




friends = ["Emily", "Hannah", "Hope", "Lauren", "Tim","Quentin"]
met = []
clues = []
spot = 0

#THE INTRO
def show_intro():
    SH = SceneHandler()
    SH.set_background("culdesac")
    SH.display_line("","Welcome! Click or press Enter to continue.")
    SH.display_line("","In the near future, the friend group moved into a commune together.")
    SH.display_line("","(Some liked to call it a cul-de-sac, to make it sound less cultish...")
    SH.display_line("","...but tbh it wasn't fooling anyone.")
    SH.display_line("","Everything was happy until they appeared. Those only heard about in fairytales.")
    SH.display_line("","Joann and Michael. The crafting masters of legend.")
    SH.display_line("","Having heard of Mallory's great skill, they came in the night and took her away.")
    SH.display_line("","Now it's up to you Azriel. With the help of your friends, you must save Mallory.")
    SH.display_line("","Good luck.")

#FIRST ROUND OF FRIEND PICKING
def pick_friend_1():
    SH = SceneHandler()
    SH.set_background("culdesac")
    SH.display_line("","Which friend would you like to visit?", wait = False)
    i = SH.display_choice(friends)
    friend = friends[i]

    if friend == "Emily":
        decision = help_emily()
        if decision:
            win = wine_game()
            if win:
                friends.remove("Emily")
                give_emily_clue()
                return False
        else:
            return False
    elif friend == "Hannah":
        success = try_hannah()
        return success
    elif friend == "Hope":
        hope_unavailable()
        return False
    elif friend == "Lauren":
        decision = help_lauren()
        if decision:
            win = felony_escape()
            if win:
                friends.remove("Lauren")
                give_lauren_clue()
                return False
        else:
            return False
    elif friend == "Quentin":
        decision = help_quentin()
        if decision:
            win = electric_game()
            if win:
                friends.remove("Quentin")
                give_quentin_clue()
                return False
        else:
            return False
    elif friend == "Tim":
        tim_unavailable()
        return False
    return
def help_emily():
    if "Emily" not in met:
        intro_emily()
        met.append("Emily")
    SH = SceneHandler()
    SH.set_background("emily_house")
    SH.display_line("","Would you like to help Emily sort her wine bottles?", wait = False)
    i = SH.display_choice(["Yes","No"])
    #return input("help emily?: ") == "y"
    return i == 0
def help_quentin():
    if "Quentin" not in met:
        intro_quentin()
        met.append("Quentin")
    SH = SceneHandler()
    SH.set_background("quentin_room")
    SH.display_line("","Do you want to cut Quentin's power?", wait = False)
    i = SH.display_choice(["Yes","No"])
    #return input("help quentin?: ") == "y"
    return i == 0
def help_lauren():
    if "Lauren" not in met:
        intro_lauren()
        met.append("Lauren")
    SH = SceneHandler()
    SH.set_background("lauren_room")
    SH.display_line("","Would you like to help Lauren escape the imposter?", wait = False)
    i = SH.display_choice(["Yes","No"])
    #return input("help lauren?: ") == "y"
    return i == 0
def try_hannah():
    #code = input("got the code?: ") == "y"
    #SH = SceneHandler()
    #SH.set_background("hannah_front_door")
    #SH.display_line("Clues:",str(clues))
    #SH.display_line("TEMPORARY - MUST REPLACE","Do you have the code and all of your friends?", wait = False)
    #i = SH.display_choice(["Yes","No"])
    #return code and len(friends) == 3
    #return i == 0
    return run_game(KeyPuzzle)
def wine_game():
    #return input("win the wine game?: ") == "y"
    return run_game(WineGame)
def felony_escape():
    #return input("win the among us game?: ") == "y"
    return run_game(FelonyEscape)
def electric_game():
    #return input("win the power game?: ") == "y"
    return run_game(ElectricGame)
def hope_unavailable():
    #print("hope unavailable")
    SH = SceneHandler()
    SH.set_background("hope_front_door")
    SH.display_line("","*KNOCK KNOCK KNOCK*")
    SH.display_line("",". . .")
    SH.display_line("","Hope doesn't seem to be home. Maybe try again later.")
    return
def tim_unavailable():
    #print("tim unavailable")
    SH = SceneHandler()
    SH.set_background("tim_front_door")
    SH.display_line("","*KNOCK KNOCK KNOCK*")
    SH.display_line("",". . .")
    SH.display_line("","Tim is home but he's not answering the door for some reason. Maybe try again later.")
    return
def give_emily_clue():
    SH = SceneHandler()
    SH.set_background("emily_house")
    SH.set_speaker("emily_excited")
    SH.display_line("Emily","Thank you so much! It would have taken forever to fix that alone.")
    SH.set_speaker("emily_normal")
    SH.display_line("Emily","So what was that emergency you needed help with?")
    SH.display_line("Azriel","Mallory's missing!")
    SH.set_speaker("emily_concern")
    SH.display_line("Azriel","A mysterious narrator said I had to get my friends to help me find her!")
    SH.display_line("Emily","Oh no! We have to find her!")
    SH.display_line("Emily","Wait what's this on the back of the cabinet?")
    SH.speaker = None
    SH.display_line("","She takes a post-it note off the cabinet door.")
    SH.set_speaker("emily_normal")
    SH.display_line("Emily","This piece of paper says _ _ 1. I wonder what that could mean.")
    if len(friends) == 3:
        SH.display_line("Azriel","I think I might know...Let's go see Hannah.")
    else:
        SH.display_line("Azriel","I'm not sure. Let's check in with the rest of the group.")
    clues.append("_ _ 1")
    #print("emily's clue")
    return
def give_quentin_clue():
    #print("quentin's clue")
    SH = SceneHandler()
    SH.set_speaker("quentin_concern")
    SH.display_line("Quentin","What happened to my electricity?!?")
    SH.display_line("Azriel","I turned it off - Mallory's missing, you have to help me!")
    SH.display_line("Quentin", "Oh no! Alright, let me just turn my power back on before we leave.")
    SH.set_background("quentin_room")
    SH.speaker = None
    SH.display_line("","He leaves and the power whirs back to life.")
    SH.set_speaker("quentin_normal")
    SH.display_line("Quentin", "Hey I found this weird note by the circuit breaker.")
    SH.display_line("Quentin", "It says _3_. Do you know what that means?")
    if len(friends) == 3:
        SH.display_line("Azriel","I think I might know...Let's go see Hannah.")
    else:
        SH.display_line("Azriel","I'm not sure. Let's check in with the rest of the group.")
    clues.append("_ 3 _")
    return
def give_lauren_clue():
    #print("lauren's clue")
    SH = SceneHandler()
    SH.set_background("lauren_room")
    SH.set_speaker("lauren_excited")
    SH.display_line("Lauren","We did it! Thank you for your help!")
    SH.set_speaker("lauren_normal")
    SH.display_line("Lauren","So did you need something?")
    SH.display_line("Azriel","Yeah, Mallory's missing, you have to help me!")
    SH.set_speaker("lauren_concern")
    if len(friends) == 3:
        SH.display_line("Azriel","...I'm starting to sound like a broken record.")
    SH.display_line("Lauren", "Oh no! We've got to find her!")
    SH.display_line("Lauren", "Wait, what's that piece of paper on my desk?")
    SH.speaker = None
    SH.display_line("","...")
    SH.set_speaker("lauren_normal")
    SH.display_line("Lauren","It says 7_ _. Do you know what that means?")
    if len(friends) == 3:
        SH.display_line("Azriel","I think I might know...Let's go see Hannah.")
    else:
        SH.display_line("Azriel","I'm not sure. Let's check in with the rest of the group.")
    clues.append("7 _ _")
    return

def intro_emily():
    #print('oh no emily is having issues')
    SH = SceneHandler()
    SH.set_background("emily_front_door")
    SH.display_line("","*KNOCK KNOCK KNOCK*")
    SH.display_line("","You hear someone scrambling to open the door, audibly upset.")
    SH.set_background("emily_house")
    SH.set_speaker("emily_upset")
    SH.display_line("Emily","I'm so upset! I ruined everything!!!")
    SH.display_line("Azriel", "I'm sure it's not that bad but right now I-")
    SH.display_line("Emily","No it is that bad! There's wine everywhere. I bumped into the cabinet and-")
    SH.display_line("", "*she sobs, unable to finish her sentence*")
def intro_lauren():
    #print('oh no lauren is having issues')
    SH = SceneHandler()
    SH.set_background("lauren_front_door")
    SH.display_line("","*KNOCK KNOCK KNOCK*")
    SH.display_line("","Lauren opens the door and invites you inside.")
    SH.set_background("lauren_room")
    SH.set_speaker("lauren_upset")
    SH.display_line("Lauren","You interrupted me in the middle of my game!")
    SH.set_speaker("lauren_gaming")
    SH.display_line("Lauren","I had almost finished my tasks.")
    SH.display_line("Azriel","I'm sorry but there's an emergen-")
    SH.display_line("Lauren","Oh no the reactor! Hold on I gotta fix it before the imposter gets me.")
def intro_quentin():
    #print("oh no quentin's having issues")
    SH = SceneHandler()
    SH.set_background("quentin_front_door")
    SH.display_line("","*KNOCK KNOCK KNOCK*")
    SH.display_line("","No one answers, but the door appears unlocked, so you enter.")
    SH.set_background("quentin_room")
    SH.set_speaker("quentin_gaming")
    SH.display_line("Azriel","Quentin! You've got to help me - Mallory's gone missing!")
    SH.display_line("Quentin","...")
    SH.display_line("Azriel","... ...")
    SH.display_line("Quentin","... ... ...")
    SH.display_line("Azriel","You aren't listening, are you.")
    SH.display_line("","Very observant.")
    SH.display_line("","Quentin is too wrapped up in his videogame to notice you right now.")
    SH.display_line("","Maybe if you cut the power, he'd pay attention?")
#hannah puzzle segway
def help_hannah():
    if "Hannah" not in met:
        intro_hannah()
        met.append("Hannah")
    #return input("get hannah's attention?: ") == "y"
    SH = SceneHandler()
    SH.set_background("hannah_room")
    SH.display_line("","Do you want to get Hannah's attention?", wait = False)
    i = SH.display_choice(["Yes","No"])
    return i == 0

def intro_hannah():
    #print('hannah is listening to music')
    SH = SceneHandler()
    SH.set_background("hannah_room")
    SH.set_speaker("hannah_excited")
    SH.display_line("","Hannah's jamming out to music, must be why she didn't hear you knock.")
    SH.set_speaker("emily_normal")
    SH.display_line("Emily","Her ults had a comeback today, so we'll have to get her attention.")
    SH.display_line("Azriel", "Okay, but how do we do that?")
    SH.display_line("Emily","There are some photocards here on her table! We need to find her bias!")
def do_hannah_puzzle():
    #return input("win hannah's puzzle?: ") == "y"
    return run_game(MatchingGame)
def tell_to_do_hannah_puzzle():
    #print("you should do hannah's puzzle")
    SH = SceneHandler()
    SH.set_background("hannah_room")
    SH.set_speaker("emily_normal")
    SH.display_line("Emily","I think we should try to get her attention...")
    return
def give_hannah_clue():
    SH = SceneHandler()
    SH.set_background("hannah_room")
    SH.set_speaker("hannah_excited")
    SH.display_line("Azriel","Hannah, look! It's your boy.")
    SH.set_speaker("hannah_concern")
    SH.display_line("Hannah","Ah! He's so precious, I love him.")
    SH.set_speaker("hannah_normal")
    SH.display_line("Hannah","...")
    SH.display_line("Hannah","When did you guys get here?")
    SH.display_line("Azriel","Just now. Mallory's missing! We're rounding up the gang to look for her.")
    SH.set_speaker("hannah_concern")
    SH.display_line("Hannah","Oh no! Who do you have left to talk to?")
    SH.display_line("Azriel","We still haven't been able to see Tim or Hope.")
    SH.display_line("Hannah","Well let's go talk to them now!")
    #print('hannah gives you a clue')

#round 2
def pick_friend_2():
    SH = SceneHandler()
    SH.set_background("culdesac")
    SH.display_line("","Which friend would you like to visit?", wait = False)
    i = SH.display_choice(friends)
    friend = friends[i]
    '''
    friend = ""
    while friend not in friends:
        friend = input("Pick a friend: "+str(friends)+": ")
    '''
    if friend == "Tim":
        decision = help_tim()
        if decision:
            win = schedule_game()
            if win:
                friends.remove("Tim")
                give_tim_clue()
                return False
        else:
            return False
    if friend == "Hope":
        decision = help_hope()
        if decision:
            win = cookie_game()
            if win:
                friends.remove("Hope")
                give_hope_clue()
                return False
def help_tim():
    if "Tim" not in met:
        intro_tim()
        met.append("Tim")
    #return input("help tim?: ") == "y"
    SH = SceneHandler()
    SH.set_background("tim_room")
    SH.display_line("","Do you want to help Tim rearrange his schedule?", wait = False)
    i = SH.display_choice(["Yes","No"])
    return i == 0
def help_hope():
    if "Hope" not in met:
        intro_hope()
        met.append("Hope")
    #return input("help hope?: ") == "y"
    SH = SceneHandler()
    SH.set_background("hope_room")
    SH.display_line("","Do you want to help Hope package cookies?", wait = False)
    i = SH.display_choice(["Yes","No"])
    return i == 0
def schedule_game():
    #return input("win the schedule_game?: ") == "y"
    return run_game(ScheduleGame)
def cookie_game():
    #return input("win the cookie_game?: ") == "y"
    return run_game(CookieGame)
def intro_tim():
    #print('tim schedule busy')
    SH = SceneHandler()
    SH.set_background("tim_front_door")
    SH.display_line("","*KNOCK KNOCK KNOCK*")
    SH.display_line("","Tim opens the door and invites you inside.")
    SH.set_background("tim_room")
    SH.set_speaker("tim_normal")
    SH.display_line("Tim","Azriel! How are you doing today?")
    SH.display_line("Azriel","Tim! Mallory's gone missing! I need your help to find her.")
    SH.set_speaker("tim_concern")
    SH.display_line("Tim","Oh no! Let's leave right away and start looking.")
    SH.speaker = None
    SH.display_line("","Tim runs to the door as you notice a giant pile of homework.")
    SH.display_line("Azriel","Tim...do you have time to help me look for Mallory?")
    SH.set_speaker("tim_concern")
    SH.display_line("Tim","Sure I do. I just have 7 group projects, a few final exams...")
    SH.display_line("Tim","and a lab report where we have to make a COVID vaccine.")
    SH.set_speaker("tim_normal")
    SH.display_line("Tim","So I'll be fine!")
    SH.display_line("Azriel","Tim you need to prioritize. You don't have time to spare!")
    SH.set_speaker("tim_concern")
    SH.display_line("Tim","Maybe you're right, let me check my calendar.")
def intro_hope():
    #print('hope making cookies')
    SH = SceneHandler()
    SH.set_background("hope_front_door")
    SH.display_line("","Hope's car is here, she must be home now.")
    SH.display_line("", "*KNOCK KNOCK KNOCK*")
    SH.display_line("","You hear pots and pans clanking as someone approaches the door.")
    SH.set_background("hope_room")
    SH.set_speaker("hope_normal")
    SH.display_line("Hope","Oh hey! I was just about to take this batch of cookies out of the oven.")
    SH.display_line("Azriel","Hope! Mallory's missing! You got to help me find her!")
    SH.set_speaker("hope_concern")
    SH.display_line("Hope","Oh no! Let me finish packaging these cookies and then I'll help you.")
    SH.display_line("Azriel", "Where are you sending them?")
    SH.set_speaker("hope_normal")
    SH.display_line("Hope","I saw someone's address in the background of a photo on Facebook...")
    SH.display_line("Hope","and I just really thought they deserved some cookies.")
    SH.display_line("Azriel","...")
    SH.display_line("Hope","What? That's just the kind of person I am.")
    SH.display_line("Hope","It's only gonna take a minute to pack these cookies.")
#tim hope segway
def tell_to_do_tim_puzzle():
    #print("you should do tim's puzzle")
    SH = SceneHandler()
    SH.set_background("tim_room")
    SH.set_speaker("lauren_concern")
    SH.display_line("Lauren","I think we need to help him with his schedule...")
    return
def tell_to_do_hope_puzzle():
    #print("you should do hope's puzzle")
    SH = SceneHandler()
    SH.set_background("hope_room")
    SH.set_speaker("hannah_normal")
    SH.display_line("Hannah","I think we should help with the cookies...")
    return
#35.94961428400051, -86.81547052174778
def give_hope_clue():
    #print("hope's clue")
    SH = SceneHandler()
    SH.set_background("hope_room")
    SH.set_speaker("hope_excited")
    SH.display_line("Hope","We did it! Thanks for you help.")
    SH.display_line("Hope","Let me just put these in the fridge for now...")
    SH.speaker = None
    SH.display_line("","...")
    SH.set_speaker("hope_normal")
    SH.display_line("Hope","I found a note taped to the fridge with some numbers on it.")
    SH.display_line("Hope","It says \"35.94961428400051, _\"")
    if "Tim" not in friends:
        SH.display_line("Azriel", "Oh! I know what we have to do.")

    return
def give_tim_clue():
    #print("tim's clue")
    SH = SceneHandler()
    SH.set_background("tim_room")
    SH.set_speaker("tim_excited")
    SH.display_line("Tim","You did it! Now I have time to help you!")
    SH.set_speaker("tim_concern")
    SH.display_line("Tim","Wait, what's on the back of my planner?")
    SH.display_line("Tim","It's a note that says \"_, -86.81547052174778\".")
    if "Hope" not in friends:
        SH.display_line("Azriel", "Oh! I know what we have to do.")
    return
def trans_hope_tim():
    SH = SceneHandler()
    SH.set_background("hope_room")
    SH.set_speaker("hope_normal")
    SH.display_line("Azriel", "Weird. Maybe we should go talk to Tim.")
    #print("you should see tim now")
def trans_tim_hope():
    #print('you should see hope now')
    SH = SceneHandler()
    SH.set_background("tim_room")
    SH.set_speaker("tim_concern")
    SH.display_line("Azriel", "Weird. Maybe we should go talk to Hope.")

#coordinates segway
def enter_coordinates():
    SH = SceneHandler()
    SH.set_background("culdesac")
    SH.set_speaker('all')
    SH.display_line("Azriel","Finally! We have everyone here.")
    SH.display_line("Azriel","I think I know what the notes at Hope's and Tim's houses meant.")
    SH.display_line("Azriel","If you put them together, it's 35.94961428400051, -86.81547052174778.")
    SH.display_line("Azriel","I bet those are coordinates.")
    SH.set_speaker("quentin_concern")
    SH.display_line("Quentin","The GPS says there's a Joann's at that location. Do you think she's there?")
    SH.display_line("Azriel","That must be it. Let's go!")
    SH.background = None
    SH.speaker = None
    SH.display_line("","...")
    SH.set_background("joanns")
    SH.set_speaker("all")
    SH.display_line("Azriel", "We're here! But it looks like the store is closed. What do we do now?")
    SH.set_speaker("emily_normal")
    SH.display_line("Emily","You said you were hearing a narrator earlier. Did they say anything else?")
    SH.set_speaker("all")
    SH.display_line("Azriel","They just said I needed to gather all my friends. But now I don't know why.")
    SH.display_line("The Mysterious Narrator™","Make them look in their pockets.")
    SH.display_line("Azriel","Hey everyone look in your pockets.")
    SH.speaker = None
    SH.display_line("","...")
    SH.set_speaker("all")
    SH.display_line("Everyone","Woah there's a spool of thread!")
    SH.display_line("The Mysterious Narrator™",";)")
    #print("you enter the coordinates. no escape")
    return
def do_mallory_puzzle():
    #return input("do mallory's puzzle?: ") == "y"
    return run_game(MosaicGame)
def tell_to_do_mallory_puzzle():
    #print("you should do Mallory's puzzle")
    SH = SceneHandler()
    SH.display_line("The Mysterious Narrator™","bruh you gotta do the puzzle")
    return
def reunion():
    #print("its a reunion")
    SH = SceneHandler()
    SH.set_background("mallory_saved")
    SH.display_line("The Mysterious Narrator™","You did it!")
    SH.set_background("joanns")
    i = 1
    for friend in ["emily","hannah","hope","lauren","quentin","tim"]:
        SH.set_speaker(friend+"_excited")
        SH.display_line(friend.title(),"IT'S MALLORY"+"!"*i)
        i = i + 1
    SH.background = None
    SH.speaker = None
    SH.display_line("","...")
    return
def credits():
    #print("here are some credits")
    SH = SceneHandler()
    SH.display_line("","Congratulations! You've completed Save Mallory!")
    SH.display_line("","I'm aware this is the worst game to ever exist,")
    SH.display_line("","but thank you for making it this far.")
    SH.display_line("","I was inspired by Myst to make this game.")
    SH.display_line("","I know it's nowhere near Myst's caliber but I thought it'd be fun.")
    SH.display_line("","Merry Christmas!")
    SH.display_line("","and Happy New Year :)")


def main(old_spot = None):
    global spot
    global friends
    '''ALL FUNCTIONS MUST BE DEFINED BEFORE HERE'''
    #'''
    #"""
    #Letting it all happen
    if old_spot == 0 or old_spot == None:
        spot = 0
        show_intro()
        old_spot = None
    if old_spot == 1 or old_spot == None:
        spot = 1
        while not pick_friend_1():
            None
        #print("yay you got hannah's code")
        old_spot = None
    if old_spot == 2 or old_spot == None:
        spot = 2
        if not help_hannah():
            tell_to_do_hannah_puzzle()
        old_spot = None
    if old_spot == 3 or old_spot == None:
        spot = 3
        while not do_hannah_puzzle():
            tell_to_do_hannah_puzzle()
        old_spot = None
    if old_spot == 4 or old_spot == None:
        spot = 4
        if "Hannah" in friends:
            friends.remove("Hannah")
        give_hannah_clue()
        friends = ["Hope","Tim"]
        old_spot = None
        #'''
    if old_spot == 5 or old_spot == None:
        spot = 5
        while not pick_friend_2() and "Tim" in friends and "Hope" in friends:
            None
        old_spot = None
    if old_spot == 6 or old_spot == 7 or old_spot == None:
        if old_spot == 6 or old_spot == None:
            spot = 6
            if "Tim" in friends:
                trans_hope_tim()
                if not help_tim():
                    tell_to_do_tim_puzzle()
                while not schedule_game():
                    tell_to_do_tim_puzzle()
                old_spot = None
                if old_spot == 7 or old_spot == None:
                    spot = 7
                    give_tim_clue()
                    old_spot = None

    if old_spot == 6 or old_spot == 7 or old_spot == None:
        if old_spot == 6 or old_spot == None:
            spot = 6
            if "Hope" in friends:
                trans_tim_hope()
                if not help_hope():
                    tell_to_do_hope_puzzle()
                while not cookie_game():
                    tell_to_do_hope_puzzle()
                old_spot = None
                if old_spot == 7 or old_spot == None:
                    spot = 7
                    give_hope_clue()
                    old_spot = None
    #"""
    if old_spot == 8 or old_spot == None:
        spot = 8
        enter_coordinates()
        old_spot = None
    if old_spot == 9 or old_spot == None:
        spot = 9
        while not do_mallory_puzzle():
            tell_to_do_mallory_puzzle()
        old_spot = None
    if old_spot == 10 or old_spot == None:
        spot = 10
        reunion()
        credits()
    save_game()

'''saving'''
#need to know friend list
#need to know met list
#need to know clue list
#need to know spot
save_exists = load_game()
SH = SceneHandler()
if save_exists:
    SH.set_background("loading_page_reload")
    choices = ["Start New Game", "Continue Old Game"]
    squares = [(241,443,566,568),(715,444,1042,568)]
else:
    SH.set_background("loading_page_new")
    choices = ["Start New Game"]
    squares = [(480,446,807,571)]

SH.windowSurface.blit(SH.background, (0,0))
i = SH.display_choice(choices, custom_squares = squares)
if i == 0:
    friends = ["Emily", "Hannah", "Hope", "Lauren", "Tim","Quentin"]
    met = []
    clues = []
    spot = 0


main(spot)
