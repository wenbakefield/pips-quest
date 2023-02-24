from GameState import GameState

import pygame, sys, os, configparser, pickle, asyncio
from pygame.locals import *
pygame.init()

# config
config = configparser.ConfigParser()
config.read('options.ini')

options_scale = config['Graphics']['scale']
if options_scale == "":
    options_scale = "3"

options_seed = config['Gameplay']['seed']
options_difficulty = config['Gameplay']['difficulty']
options_adaptive_difficulty = config['Gameplay']['adaptive_difficulty']

options_sfx_vol = config['Audio']['sfx_volume']
if options_sfx_vol == "":
    options_sfx_vol = "0.2"

options_mus_vol = config['Audio']['music_volume']
if options_mus_vol == "":
    options_mus_vol = "0.3"

# Colours
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (100, 100, 100)
LIGHT_GRAY = (150, 150, 150)

# Game Setup
FPS = 60
clock = pygame.time.Clock()
SCALE = int(options_scale)
WINDOW_WIDTH = 320 * SCALE
WINDOW_HEIGHT = 240 * SCALE
 
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Pip's Quest")

# assets

# sounds
VOLUME_SFX = float(options_sfx_vol)
VOLUME_MUSIC = float(options_mus_vol)

pygame.mixer.init()

sound_damage = pygame.mixer.Sound(os.path.join('sounds', 'sound_damage.wav'))
sound_smash = pygame.mixer.Sound(os.path.join('sounds', 'sound_smash.wav'))
sound_help = pygame.mixer.Sound(os.path.join('sounds', 'sound_help.wav'))
sound_mortal_damage = pygame.mixer.Sound(os.path.join('sounds', 'sound_mortal_damage.wav'))

sound_enemy_attack = pygame.mixer.Sound(os.path.join('sounds', 'sound_enemy_attack.wav'))
sound_enemy_die = pygame.mixer.Sound(os.path.join('sounds', 'sound_enemy_die.wav'))

sound_player_attack = pygame.mixer.Sound(os.path.join('sounds', 'sound_player_attack.wav'))
sound_player_defend = pygame.mixer.Sound(os.path.join('sounds', 'sound_player_defend.wav'))

sound_player_heal = pygame.mixer.Sound(os.path.join('sounds', 'sound_player_heal.wav'))
sound_player_select = pygame.mixer.Sound(os.path.join('sounds', 'sound_player_select.wav'))
sound_player_spell = pygame.mixer.Sound(os.path.join('sounds', 'sound_player_spell.wav'))
sound_player_sell = pygame.mixer.Sound(os.path.join('sounds', 'sound_player_sell.wav'))

def play_enemy_music(species):
    file_name = ''
    if species == "Bat":
        file_name = 'music_bat.mp3'
    if species == "Bullfrog":
        file_name = 'music_bullfrog.mp3'
    if species == "Bunny":
        file_name = 'music_meerkat.mp3'
    if species == "Rat":
        file_name = 'music_rat.mp3'
    if species == "Spider":
        file_name = 'music_spider.mp3'
    if species == "Snake":
        file_name = 'music_boss.mp3'
    play_music_loop(file_name)

def play_music_loop(file_name):
    pygame.mixer.music.load(os.path.join('sounds', file_name))
    pygame.mixer.music.set_volume(VOLUME_MUSIC)
    pygame.mixer.music.play(-1)

def play_music(file_name):
    pygame.mixer.music.load(os.path.join('sounds', file_name))
    pygame.mixer.music.set_volume(VOLUME_MUSIC)
    pygame.mixer.music.play()

def stop_music():
    pygame.mixer.music.stop()

def play_sound(sound):
    sound.set_volume(VOLUME_SFX)
    sound.play()

# fonts
font_title = pygame.font.Font(os.path.join('fonts', 'AncientModernTales-a7Po.ttf'), 50 * SCALE)
font_subtitle = pygame.font.Font(os.path.join('fonts', 'AncientModernTales-a7Po.ttf'), 20 * SCALE)
font_button = pygame.font.Font(os.path.join('fonts', 'AGoblinAppears-o2aV.ttf'), 5 * SCALE)
font_text = pygame.font.Font(os.path.join('fonts', 'AGoblinAppears-o2aV.ttf'), 5 * SCALE)

# text
txt_title = font_title.render("Pip's Quest", False, WHITE, None)
txt_fork = font_subtitle.render("Where To?", False, WHITE, None)
txt_shop = font_subtitle.render("Buy Food?", False, WHITE, None)
txt_wandering = font_subtitle.render("Wandering...", False, WHITE, None)
txt_game_over = font_title.render("Game Over!", False, WHITE, None)
txt_game_win = font_title.render("You Win!", False, WHITE, None)

# backgrounds
bg_title = pygame.image.load(os.path.join('images', 'bg_title.png')).convert()
bg_title = pygame.transform.scale(bg_title, (WINDOW_WIDTH, WINDOW_HEIGHT))

bg_forest = pygame.image.load(os.path.join('images', 'bg_forest.png')).convert()
bg_forest = pygame.transform.scale(bg_forest, (WINDOW_WIDTH, WINDOW_HEIGHT))

bg_desert = pygame.image.load(os.path.join('images', 'bg_desert.png')).convert()
bg_desert = pygame.transform.scale(bg_desert, (WINDOW_WIDTH, WINDOW_HEIGHT))

bg_cave = pygame.image.load(os.path.join('images', 'bg_cave.png')).convert()
bg_cave = pygame.transform.scale(bg_cave, (WINDOW_WIDTH, WINDOW_HEIGHT))

bg_grassland = pygame.image.load(os.path.join('images', 'bg_grassland.png')).convert()
bg_grassland = pygame.transform.scale(bg_grassland, (WINDOW_WIDTH, WINDOW_HEIGHT))

bg_swamp = pygame.image.load(os.path.join('images', 'bg_swamp.png')).convert()
bg_swamp = pygame.transform.scale(bg_swamp, (WINDOW_WIDTH, WINDOW_HEIGHT))

bg_shop = pygame.image.load(os.path.join('images', 'bg_shop.png')).convert()
bg_shop = pygame.transform.scale(bg_shop, (WINDOW_WIDTH, WINDOW_HEIGHT))

fg_shop = pygame.image.load(os.path.join('images', 'fg_shop.png')).convert_alpha()
fg_shop = pygame.transform.scale(fg_shop, (WINDOW_WIDTH, WINDOW_HEIGHT))

# food
food_berry = pygame.image.load(os.path.join('images', 'food', 'strawberry.png')).convert_alpha()
food_berry = pygame.transform.scale(food_berry, (35 * SCALE * 0.5, 29 * SCALE * 0.5))

food_apple = pygame.image.load(os.path.join('images', 'food', 'apple.png')).convert_alpha()
food_apple = pygame.transform.scale(food_apple, (24 * SCALE * 1.5, 26 * SCALE * 1.5))

# runes
RUNE_SCALE = 0.5

rune_fire_1 = pygame.image.load(os.path.join('images', 'rune_fire', '1.png')).convert_alpha()
rune_fire_1 = pygame.transform.scale(rune_fire_1, (48 * SCALE * RUNE_SCALE, 105 * SCALE * RUNE_SCALE))

rune_fire_2 = pygame.image.load(os.path.join('images', 'rune_fire', '2.png')).convert_alpha()
rune_fire_2 = pygame.transform.scale(rune_fire_2, (48 * SCALE * RUNE_SCALE, 105 * SCALE * RUNE_SCALE))

rune_fire_3 = pygame.image.load(os.path.join('images', 'rune_fire', '3.png')).convert_alpha()
rune_fire_3 = pygame.transform.scale(rune_fire_3, (48 * SCALE * RUNE_SCALE, 105 * SCALE * RUNE_SCALE))

rune_fire_4 = pygame.image.load(os.path.join('images', 'rune_fire', '4.png')).convert_alpha()
rune_fire_4 = pygame.transform.scale(rune_fire_4, (48 * SCALE * RUNE_SCALE, 105 * SCALE * RUNE_SCALE))

rune_spark_1 = pygame.image.load(os.path.join('images', 'rune_spark', '1.png')).convert_alpha()
rune_spark_1 = pygame.transform.scale(rune_spark_1, (48 * SCALE * RUNE_SCALE, 105 * SCALE * RUNE_SCALE))

rune_spark_2 = pygame.image.load(os.path.join('images', 'rune_spark', '2.png')).convert_alpha()
rune_spark_2 = pygame.transform.scale(rune_spark_2, (48 * SCALE * RUNE_SCALE, 105 * SCALE * RUNE_SCALE))

rune_spark_3 = pygame.image.load(os.path.join('images', 'rune_spark', '3.png')).convert_alpha()
rune_spark_3 = pygame.transform.scale(rune_spark_3, (48 * SCALE * RUNE_SCALE, 105 * SCALE * RUNE_SCALE))

rune_spark_4 = pygame.image.load(os.path.join('images', 'rune_spark', '4.png')).convert_alpha()
rune_spark_4 = pygame.transform.scale(rune_spark_4, (48 * SCALE * RUNE_SCALE, 105 * SCALE * RUNE_SCALE))

rune_earth_1 = pygame.image.load(os.path.join('images', 'rune_earth', '1.png')).convert_alpha()
rune_earth_1 = pygame.transform.scale(rune_earth_1, (48 * SCALE * RUNE_SCALE, 105 * SCALE * RUNE_SCALE))

rune_earth_2 = pygame.image.load(os.path.join('images', 'rune_earth', '2.png')).convert_alpha()
rune_earth_2 = pygame.transform.scale(rune_earth_2, (48 * SCALE * RUNE_SCALE, 105 * SCALE * RUNE_SCALE))

rune_earth_3 = pygame.image.load(os.path.join('images', 'rune_earth', '3.png')).convert_alpha()
rune_earth_3 = pygame.transform.scale(rune_earth_3, (48 * SCALE * RUNE_SCALE, 105 * SCALE * RUNE_SCALE))

rune_earth_4 = pygame.image.load(os.path.join('images', 'rune_earth', '4.png')).convert_alpha()
rune_earth_4 = pygame.transform.scale(rune_earth_4, (48 * SCALE * RUNE_SCALE, 105 * SCALE * RUNE_SCALE))

rune_ice_1 = pygame.image.load(os.path.join('images', 'rune_ice', '1.png')).convert_alpha()
rune_ice_1 = pygame.transform.scale(rune_ice_1, (48 * SCALE * RUNE_SCALE, 105 * SCALE * RUNE_SCALE))

rune_ice_2 = pygame.image.load(os.path.join('images', 'rune_ice', '2.png')).convert_alpha()
rune_ice_2 = pygame.transform.scale(rune_ice_2, (48 * SCALE * RUNE_SCALE, 105 * SCALE * RUNE_SCALE))

rune_ice_3 = pygame.image.load(os.path.join('images', 'rune_ice', '3.png')).convert_alpha()
rune_ice_3 = pygame.transform.scale(rune_ice_3, (48 * SCALE * RUNE_SCALE, 105 * SCALE * RUNE_SCALE))

rune_ice_4 = pygame.image.load(os.path.join('images', 'rune_ice', '4.png')).convert_alpha()
rune_ice_4 = pygame.transform.scale(rune_ice_4, (48 * SCALE * RUNE_SCALE, 105 * SCALE * RUNE_SCALE))

rune_arcane = pygame.image.load(os.path.join('images', 'rune_arcane', '1.png')).convert_alpha()
rune_arcane = pygame.transform.scale(rune_arcane, (48 * SCALE * RUNE_SCALE, 105 * SCALE * RUNE_SCALE))

def rune_to_image(rune):
    element = str(rune.get_element())
    power = str(rune.get_power())

    if element == "A":
        return rune_arcane
    elif element == "F":
        if power == "1":
            return rune_fire_1
        elif power == "2":
            return rune_fire_2
        elif power == "3":
            return rune_fire_3
        elif power == "4":
            return rune_fire_4
    elif element == "S":
        if power == "1":
            return rune_spark_1
        elif power == "2":
            return rune_spark_2
        elif power == "3":
            return rune_spark_3
        elif power == "4":
            return rune_spark_4
    elif element == "E":
        if power == "1":
            return rune_earth_1
        elif power == "2":
            return rune_earth_2
        elif power == "3":
            return rune_earth_3
        elif power == "4":
            return rune_earth_4
    elif element == "I":
        if power == "1":
            return rune_ice_1
        elif power == "2":
            return rune_ice_2
        elif power == "3":
            return rune_ice_3
        elif power == "4":
            return rune_ice_4
    else:
        return rune_arcane

# mobs
mob_bat = pygame.image.load(os.path.join('images', 'mob_bat', 'mob_bat.png')).convert_alpha()
mob_bat = pygame.transform.scale(mob_bat, (65 * SCALE, 65 * SCALE))

mob_bullfrog = pygame.image.load(os.path.join('images', 'mob_bullfrog', 'mob_bullfrog.png')).convert_alpha()
mob_bullfrog = pygame.transform.scale(mob_bullfrog, (65 * SCALE, 65 * SCALE))

mob_meerkat = pygame.image.load(os.path.join('images', 'mob_meerkat', 'mob_meerkat.png')).convert_alpha()
mob_meerkat = pygame.transform.scale(mob_meerkat, (65 * SCALE, 65 * SCALE))

mob_rat = pygame.image.load(os.path.join('images', 'mob_rat', 'mob_rat.png')).convert_alpha()
mob_rat = pygame.transform.scale(mob_rat, (65 * SCALE, 65 * SCALE))

mob_spider = pygame.image.load(os.path.join('images', 'mob_spider', 'mob_spider.png')).convert_alpha()
mob_spider = pygame.transform.scale(mob_spider, (65 * SCALE, 65 * SCALE))

mob_snake = pygame.image.load(os.path.join('images', 'mob_snake', 'mob_snake.png')).convert_alpha()
mob_snake = pygame.transform.scale(mob_snake, (160 * SCALE, 120 * SCALE))

# sprites
class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, scale, type):
        super().__init__()
        self.idle_sprites = []
        self.is_animating = True

        for i in range(1, 5):
            image = pygame.image.load(os.path.join('images', type, 'idle', str(i) + '.png')).convert_alpha()
            image = pygame.transform.scale(image, (scale * 65 * SCALE, scale * 65 * SCALE))
            self.idle_sprites.append(image)
        self.current_sprite = 0
        self.image = self.idle_sprites[self.current_sprite]
        self.rect = self.image.get_rect()
        self.rect.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)
        self.rect = self.rect.move((pos_x, pos_y))

    def animate(self):
        self.is_animating = True

    def update(self, speed):
        if self.is_animating == True:
            self.current_sprite += speed
            if self.current_sprite >= len(self.idle_sprites):
                self.current_sprite = 0
                self.is_animating = True
            self.image = self.idle_sprites[int(self.current_sprite)]

class Dog(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__()
        self.idle_sprites = []
        self.is_animating = True
        for i in range(1, 5):
            image = pygame.image.load(os.path.join('images', 'npc_dog', 'idle', str(i) + '.png')).convert_alpha()
            image = pygame.transform.scale(image, (120 * SCALE, 140 * SCALE))
            self.idle_sprites.append(image)
        self.current_sprite = 0
        self.image = self.idle_sprites[self.current_sprite]
        self.rect = self.image.get_rect()
        self.rect.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)
        self.rect = self.rect.move((pos_x, pos_y))

    def animate(self):
        self.is_animating = True

    def update(self, speed):
        if self.is_animating == True:
            self.current_sprite += speed
            if self.current_sprite >= len(self.idle_sprites):
                self.current_sprite = 0
                self.is_animating = True
            self.image = self.idle_sprites[int(self.current_sprite)]

class EncounterStart(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__()
        self.sprites = []
        self.is_animating = True
        for i in range(1, 23):
            image = pygame.image.load(os.path.join('images', 'encounter_start', str(i) + '.png')).convert_alpha()
            image = pygame.transform.scale(image, (WINDOW_WIDTH, WINDOW_HEIGHT))
            self.sprites.append(image)
        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]
        self.rect = self.image.get_rect()
        self.rect.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)
        self.rect = self.rect.move((pos_x, pos_y))

    def animate(self):
        self.is_animating = True

    def update(self, speed):
        if self.is_animating == True:
            self.current_sprite += speed
            if self.current_sprite >= len(self.sprites):
                self.current_sprite = 21
                self.is_animating = False
            self.image = self.sprites[int(self.current_sprite)]

# sprite groups

moving_sprites = pygame.sprite.Group()

# rects
rect_bg = bg_title.get_rect()
rect_bg = rect_bg.move((0, 0))

rect_title = txt_title.get_rect()
rect_title.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)
rect_title = rect_title.move((0, -80 * SCALE))

rect_game_win = txt_game_win.get_rect()
rect_game_win.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)
rect_game_win = rect_game_win.move((0, -80 * SCALE))

rect_game_over = txt_game_over.get_rect()
rect_game_over.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)
rect_game_over = rect_game_over.move((0, -80 * SCALE))

rect_shop = txt_shop.get_rect()
rect_shop.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)
rect_shop = rect_shop.move((0, -80 * SCALE))

rect_subtitle = txt_fork.get_rect()
rect_subtitle.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)
rect_subtitle = rect_subtitle.move((0, -100 * SCALE))

rect_mob = mob_bat.get_rect()
rect_mob.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)
rect_mob = rect_mob.move((0, 30 * SCALE))

rect_boss = mob_snake.get_rect()
rect_boss.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)
rect_boss = rect_boss.move((0, 30 * SCALE))

class button():
    def __init__(self, color, x, y, width, height, text=''):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    def draw(self,win,outline=None):
        #Call this method to draw the button on the screen
        if outline:
            pygame.draw.rect(win, outline, (self.x-2,self.y-2,self.width+4,self.height+4),0)
        
        pygame.draw.rect(win, self.color, (self.x,self.y,self.width,self.height),0)
    
        if self.text != '':
            font = font_button
            text = font.render(self.text, 1, WHITE)
            win.blit(text, (self.x + (self.width/2 - text.get_width()/2), self.y + (self.height/2 - text.get_height()/2)))

    def isOver(self, pos):
        #Pos is the mouse position or a tuple of (x,y) coordinates
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True
        
        return False

class rune_button():
    def __init__(self, rune, color, x, y, width, height, text=''):
        self.rune = rune
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    def draw(self,win,outline=None):
        #Call this method to draw the button on the screen
        if outline:
            pygame.draw.rect(win, outline, (self.x-2,self.y-2,self.width+4,self.height+4),0)
        
        pygame.draw.rect(win, self.color, (self.x,self.y,self.width,self.height),0)
    
        if self.text != '':
            font = font_button
            text = font.render(self.text, 1, WHITE)
            win.blit(text, (self.x + (self.width/2 - text.get_width()/2), self.y + (self.height/2 - text.get_height()/2)))

    def isOver(self, pos):
        #Pos is the mouse position or a tuple of (x,y) coordinates
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True
        
        return False

# buttons
button_new_game = button(BLACK, (WINDOW_WIDTH // 2) - (25 * SCALE), (WINDOW_HEIGHT // 2) + (75 * SCALE), 50 * SCALE, 18 * SCALE, 'New Game')
button_load_game = button(BLACK, (WINDOW_WIDTH // 2) - (25 * SCALE), (WINDOW_HEIGHT // 2) + (95 * SCALE), 50 * SCALE, 18 * SCALE, 'Load Game')
button_fork_left = button(BLACK, (WINDOW_WIDTH // 2) - (105 * SCALE), (WINDOW_HEIGHT // 2), 50 * SCALE, 18 * SCALE, 'Left')
button_fork_right = button(BLACK, (WINDOW_WIDTH // 2) + (55 * SCALE), (WINDOW_HEIGHT // 2), 50 * SCALE, 18 * SCALE, 'Right')
button_cast = button(BLACK, (WINDOW_WIDTH // 2) + (1 * SCALE), (WINDOW_HEIGHT // 2) + (70 * SCALE), 37 * SCALE, 18 * SCALE, 'Cast!')
button_continue = button(BLACK, (WINDOW_WIDTH // 2) - (25 * SCALE), (WINDOW_HEIGHT // 2) + (90 * SCALE), 50 * SCALE, 18 * SCALE, 'Continue')
button_heal_1 = button(BLACK, (WINDOW_WIDTH // 2) - (120 * SCALE), (WINDOW_HEIGHT // 2) - (7 * SCALE), 50 * SCALE, 18 * SCALE, 'Heal 1')
button_heal_all = button(BLACK, (WINDOW_WIDTH // 2) + (70 * SCALE), (WINDOW_HEIGHT // 2) - (7 * SCALE), 50 * SCALE, 18 * SCALE, 'Heal All')
button_reroll = button(BLACK, 1 * SCALE, (WINDOW_HEIGHT // 2) + (70 * SCALE), 38 * SCALE, 18 * SCALE, 'Reroll!')

game = GameState(options_seed, options_difficulty, options_adaptive_difficulty)
hand_rune_buttons = []
spell_rune_buttons = []
lines = 0

TICK = USEREVENT + 1
pygame.time.set_timer(TICK, 1000)
time_in_seconds = 0
time_cache = 0
# The main function that controls the game
async def main () :
    running = True
    play_music('music_title.mp3')
    while running :
        draw_state(game.state)
        pygame.display.update()
        clock.tick(FPS)
        await asyncio.sleep(0)

def draw_background(biome):
    if biome == "Cave":
        screen.blit(bg_cave, rect_bg)
    elif biome == "Desert":
        screen.blit(bg_desert, rect_bg)
    elif biome == "Forest":
        screen.blit(bg_forest, rect_bg)
    elif biome == "Grassland":
        screen.blit(bg_grassland, rect_bg)
    elif biome == "Swamp":
        screen.blit(bg_swamp, rect_bg)
    else:
        screen.blit(bg_forest, rect_bg)

def draw_enemy(enemy_name):
    if enemy_name == "Bat":
        moving_sprites.add(Enemy(0, 0, 1, "mob_bat"))
    if enemy_name == "Bullfrog":
        moving_sprites.add(Enemy(0, 25 * SCALE, 1, "mob_bullfrog"))
    if enemy_name == "Bunny":
        moving_sprites.add(Enemy(0, 25 * SCALE, 1, "mob_meerkat"))
    if enemy_name == "Rat":
        moving_sprites.add(Enemy(0, 25 * SCALE, 1, "mob_rat"))
    if enemy_name == "Spider":
        moving_sprites.add(Enemy(0, 25 * SCALE, 1, "mob_spider"))
    if enemy_name == "Snake":
        moving_sprites.add(Enemy(0, 0, 2, "mob_snake"))

def draw_text_box(string_list, lines):
    if string_list:
        space = 7
        line_num = 0
        for line in range(lines):
            txt_line = font_text.render(str(string_list[line]), False, WHITE, BLACK)
            rect_line = txt_line.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 8))
            rect_line = rect_line.move((0, line_num * space * SCALE))
            screen.blit(txt_line, rect_line)
            line_num += 1

def draw_text_center(text, x, y):
    txt = font_text.render(str(text), False, WHITE, BLACK)
    rect = txt.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 4))
    rect = rect.move((x, y))
    screen.blit(txt, rect)

def draw_rune_buttons(rune_button_list, text, pos_x, pos_y):
    global screen
    offset = 0

    x = (WINDOW_WIDTH // 2) - (pos_x * SCALE)
    y = (WINDOW_HEIGHT // 2) + (pos_y * SCALE)
    button_size = 8 * SCALE

    rune_buttons = []
    for rune in rune_button_list:
        rune_image = rune_to_image(rune)
        screen.blit(rune_image, (x + offset, y))
        current_rune_button = rune_button(rune, BLACK, x + offset + ((48 * SCALE * RUNE_SCALE) / 2) - (button_size / 2), y + (105 * SCALE * RUNE_SCALE), button_size, button_size, str(text))
        current_rune_button.draw(screen)
        rune_buttons.append(current_rune_button)
        offset += 48 * SCALE * RUNE_SCALE
    return rune_buttons

def draw_state(state):
    global game
    global SCALE
    global TICK
    global hand_rune_buttons
    global spell_rune_buttons
    global lines
    global time_in_seconds
    global time_cache
    if state == "title":
        events = pygame.event.get()

        for event in events :
            pos = pygame.mouse.get_pos()

            if event.type == QUIT :
                pygame.quit()
                sys.exit()

            if event.type == MOUSEBUTTONDOWN :
                if button_new_game.isOver(pos):
                    play_sound(sound_player_select)
                    game.choose_next_area_fork()
                    game.state = "fork"
                    play_music_loop('music_wilderness.mp3')

                if button_load_game.isOver(pos):
                    play_sound(sound_player_select)
                    play_music_loop('music_wilderness.mp3')
                    with open("save", "rb") as f:
                        game = pickle.load(f)
                    game.load()

            if event.type == MOUSEMOTION :
                if button_new_game.isOver(pos):
                    button_new_game.color = LIGHT_GRAY
                else:
                    button_new_game.color = BLACK
                if button_load_game.isOver(pos):
                    button_load_game.color = LIGHT_GRAY
                else:
                    button_load_game.color = BLACK

        screen.blit(bg_title, rect_bg)
        screen.blit(txt_title, rect_title)
        button_new_game.draw(screen)
        if os.path.exists("save"):
            button_load_game.draw(screen)
        pygame.display.flip()

    if state == "fork":
        events = pygame.event.get()

        button_fork_left.text = game.next_area1
        button_fork_right.text = game.next_area2

        for event in events :
            pos = pygame.mouse.get_pos()

            if event.type == QUIT :
                pygame.quit()
                sys.exit()
            
            if event.type == TICK :
                time_in_seconds += 1

            if event.type == MOUSEBUTTONDOWN :
                if button_fork_left.isOver(pos):
                    play_sound(sound_player_select)
                    time_cache = time_in_seconds
                    game.next_area(1)
                    play_music_loop('music_wilderness.mp3')
                    game.state = "wandering"
                if button_fork_right.isOver(pos):
                    play_sound(sound_player_select)
                    time_cache = time_in_seconds
                    game.next_area(2)
                    play_music_loop('music_wilderness.mp3')
                    game.state = "wandering"

            if event.type == MOUSEMOTION :
                if button_fork_left.isOver(pos):
                    button_fork_left.color = LIGHT_GRAY
                else:
                    button_fork_left.color = BLACK
                if button_fork_right.isOver(pos):
                    button_fork_right.color = LIGHT_GRAY
                else:
                    button_fork_right.color = BLACK

        draw_background(game.get_current_area_biome())
        screen.blit(txt_fork, rect_subtitle)

        txt_current_area = font_subtitle.render("Area " + str(game.area_num) + "-" + str(game.encounter_num), False, WHITE, BLACK)
        screen.blit(txt_current_area, (258 * SCALE, (1 * SCALE)))

        button_fork_left.draw(screen)
        button_fork_right.draw(screen)
        pygame.display.flip()

    if state == "wandering":
        
        events = pygame.event.get()

        for event in events :

            if event.type == QUIT :
                pygame.quit()
                sys.exit()
            if event.type == TICK :
                time_in_seconds += 1

        if time_in_seconds >= time_cache + 3 :
            moving_sprites.add(EncounterStart(0, 0))
            if game.area_num <= 5:
                play_music('music_encounter.mp3')
            else:
                play_music('music_boss_encounter.mp3')
            time_cache = time_in_seconds
            game.state = "encounter_start"


        draw_background(game.get_current_area_biome())
        screen.blit(txt_wandering, rect_subtitle)
        pygame.display.flip()

    if state == "encounter_start":
        events = pygame.event.get()
        for event in events :

            if event.type == QUIT :
                pygame.quit()
                sys.exit()

            if event.type == TICK :
                time_in_seconds += 1

        if time_in_seconds == time_cache + 4 :
            moving_sprites.empty()
            game.next_encounter()
            draw_enemy(game.get_current_enemy_species())
            play_enemy_music(game.get_current_enemy_species())
            game.state = "encounter"

        draw_background(game.get_current_area_biome())
        screen.blit(txt_wandering, rect_subtitle)
        moving_sprites.draw(screen)
        moving_sprites.update(0.4)
        pygame.display.flip()

    if state == "encounter":
        events = pygame.event.get()

        for event in events :
            pos = pygame.mouse.get_pos()
            if event.type == QUIT :
                pygame.quit()
                sys.exit()

            if event.type == TICK :
                time_in_seconds += 1

            if event.type == MOUSEBUTTONDOWN :

                for rune_button in hand_rune_buttons:
                    if rune_button.isOver(pos):
                        play_sound(sound_player_select)
                        game.player_state.current_spell.append(rune_button.rune)
                        game.player_state.current_hand.remove(rune_button.rune)

                for rune_button in spell_rune_buttons:
                    if rune_button.isOver(pos):
                        play_sound(sound_player_select)
                        game.player_state.current_hand.append(rune_button.rune)
                        game.player_state.current_spell.remove(rune_button.rune)

                if button_cast.isOver(pos):
                    if game.player_state.has_valid_current_spell():
                        play_sound(sound_player_spell)
                        game.next_turn()
                        time_cache = time_in_seconds
                        game.state = "encounter_action"

                if button_reroll.isOver(pos):
                    if game.rerolls > 0:
                        play_sound(sound_player_heal)
                        game.reroll_hand()

            if event.type == MOUSEMOTION :
                if button_cast.isOver(pos):
                    button_cast.color = LIGHT_GRAY
                else:
                    button_cast.color = BLACK
                if button_reroll.isOver(pos):
                    button_reroll.color = LIGHT_GRAY
                else:
                    button_reroll.color = BLACK

        draw_background(game.get_current_area_biome())
        
        moving_sprites.draw(screen)
        moving_sprites.update(0.05)

        txt_enemy_name = font_subtitle.render(game.get_current_enemy_name(), False, WHITE, BLACK)
        txt_enemy_stats = font_text.render(game.get_current_enemy_stats(), False, WHITE, BLACK)

        txt_player_name = font_subtitle.render("Pip", False, WHITE, BLACK)
        txt_player_stats = font_text.render(str(game.get_current_player_stats()), False, WHITE, BLACK)
        txt_player_hand = font_subtitle.render("Hand:", False, WHITE, BLACK)
        txt_player_spell = font_subtitle.render("Spell:", False, WHITE, BLACK)
        
        screen.blit(txt_enemy_name, (1 * SCALE, 1 * SCALE))
        screen.blit(txt_enemy_stats, (1 * SCALE, 25 * SCALE))

        screen.blit(txt_player_name, (1 * SCALE, WINDOW_HEIGHT - (95 * SCALE)))
        screen.blit(txt_player_stats, (1 * SCALE, WINDOW_HEIGHT - (71 * SCALE)))
        screen.blit(txt_player_hand, (1 * SCALE, WINDOW_HEIGHT - (31 * SCALE)))
        screen.blit(txt_player_spell, (161 * SCALE, WINDOW_HEIGHT - (31 * SCALE)))

        txt_current_area = font_subtitle.render("Area " + str(game.area_num) + "-" + str(game.encounter_num), False, WHITE, BLACK)
        screen.blit(txt_current_area, (258 * SCALE, (1 * SCALE)))

        hand_rune_buttons = draw_rune_buttons(game.player_state.current_hand, "+", 120, 59)
        spell_rune_buttons = draw_rune_buttons(game.player_state.current_spell, "-", -39, 59)

        if game.player_state.has_valid_current_spell():
            button_cast.draw(screen)

        if game.rerolls > 0:
            button_reroll.draw(screen)

        pygame.display.flip()

    if state == "encounter_action":
        events = pygame.event.get()

        for event in events :
            pos = pygame.mouse.get_pos()
            if event.type == QUIT :
                pygame.quit()
                sys.exit()

            if event.type == TICK :
                time_in_seconds += 1

            if (time_in_seconds == time_cache + 2) and (lines == 0) :
                lines = 1
                # enemy sprite state action
                play_sound(sound_enemy_attack)

            if (time_in_seconds == time_cache + 3) and (lines == 1) :
                lines = 2
                if game.player_state.current_action == "defend":
                    play_sound(sound_player_defend)
                else:
                    play_sound(sound_player_attack)

            if (time_in_seconds == time_cache + 4) and (lines == 2) :
                lines = 3
                if game.player_is_dead():
                    play_sound(sound_mortal_damage)
                elif game.current_enemy_is_dead():
                    play_sound(sound_mortal_damage)
                elif game.turn_result[2] == "SMAAAASH!!":
                    play_sound(sound_smash)
                elif game.turn_result[2] == "Nothing happens...":
                    play_sound(sound_help)
                else:
                    play_sound(sound_damage)

            if (time_in_seconds == time_cache + 6) and (lines == 3) :
                if game.player_is_dead():
                            moving_sprites.empty()
                            play_music('music_game_over.mp3')
                            game.state = "game_over"
                elif game.current_enemy_is_dead():
                    lines = 0
                    moving_sprites.empty()
                    game.give_current_enemy_gold_to_player()
                    if game.area_num <= 5:
                        play_music('music_win.mp3')
                        game.log_battle()
                        game.state = "encounter_win"
                    else:
                        play_music('music_boss_win.mp3')
                        game.log_battle()
                        game.state = "game_win"
                else:
                    lines = 0
                    game.state = "encounter"

        draw_background(game.get_current_area_biome())
        
        moving_sprites.draw(screen)
        moving_sprites.update(0.1)

        draw_text_box(game.turn_result, lines)

    if state == "encounter_win":
            events = pygame.event.get()

            for event in events :
                pos = pygame.mouse.get_pos()

                if event.type == QUIT :
                    pygame.quit()
                    sys.exit()

                if event.type == TICK :
                    time_in_seconds += 1

                if event.type == MOUSEBUTTONDOWN :
                    if button_continue.isOver(pos):
                        play_sound(sound_player_select)
                        if game.encounter_num >= 3:
                            moving_sprites.add(Dog(0, 25 * SCALE))
                            play_music_loop('music_shop.mp3')
                            game.state = "shop"
                        else:
                            time_cache = time_in_seconds
                            play_music_loop('music_wilderness.mp3')
                            game.state = "wandering"

                if event.type == MOUSEMOTION :
                    if button_continue.isOver(pos):
                        button_continue.color = LIGHT_GRAY
                    else:
                        button_continue.color = BLACK

            draw_background(game.get_current_area_biome())
            screen.blit(txt_game_win, rect_game_win)

            space = 7

            draw_text_center("The " + str(game.get_current_enemy_name()) + " was defeated!", 0, space * 1 * SCALE)
            draw_text_center("You got " + str(game.get_current_enemy_gold()) + " gold!", 0, space * 2 * SCALE)

            button_continue.draw(screen)
            pygame.display.flip()

    if state == "shop":
        events = pygame.event.get()

        for event in events :
            pos = pygame.mouse.get_pos()

            if event.type == QUIT :
                pygame.quit()
                sys.exit()
            
            if event.type == TICK :
                    time_in_seconds += 1

            if event.type == MOUSEBUTTONDOWN :
                if button_heal_1.isOver(pos):
                    play_sound(sound_player_select)
                    game.heal_player()
                if button_heal_all.isOver(pos):
                    play_sound(sound_player_heal)
                    game.heal_player_all()
                if button_continue.isOver(pos):
                    play_sound(sound_player_select)
                    if game.area_num < 5:
                        moving_sprites.empty()
                        game.choose_next_area_fork()
                        play_music_loop('music_wilderness.mp3')
                        game.state = "fork"
                        game.save()
                    else:
                        moving_sprites.empty()
                        time_cache = time_in_seconds
                        game.next_area(3)
                        play_music_loop('music_wilderness.mp3')
                        game.state = "wandering"

            if event.type == MOUSEMOTION :
                if button_heal_1.isOver(pos):
                    button_heal_1.color = LIGHT_GRAY
                else:
                    button_heal_1.color = BLACK
                if button_heal_all.isOver(pos):
                    button_heal_all.color = LIGHT_GRAY
                else:
                    button_heal_all.color = BLACK
                if button_continue.isOver(pos):
                    button_continue.color = LIGHT_GRAY
                else:
                    button_continue.color = BLACK

        screen.blit(bg_shop, rect_bg)

        moving_sprites.draw(screen)
        moving_sprites.update(0.03)

        screen.blit(fg_shop, rect_bg)
        screen.blit(txt_shop, rect_shop)

        txt_player_name = font_subtitle.render("Pip", False, WHITE, BLACK)
        txt_player_stats = font_text.render(game.get_current_player_stats(), False, WHITE, BLACK)
        
        screen.blit(txt_player_name, (1 * SCALE, WINDOW_HEIGHT - (45 * SCALE)))
        screen.blit(txt_player_stats, (1 * SCALE, WINDOW_HEIGHT - (21 * SCALE)))

        screen.blit(food_berry, ((WINDOW_WIDTH // 2) - (105 * SCALE), (WINDOW_HEIGHT // 2) - (25 * SCALE)))
        screen.blit(food_apple, ((WINDOW_WIDTH // 2) + (75 * SCALE), (WINDOW_HEIGHT // 2) - (50 * SCALE)))

        button_heal_1.draw(screen)
        button_heal_all.draw(screen)
        button_continue.draw(screen)
        pygame.display.flip()

    if state == "game_over":
            events = pygame.event.get()

            for event in events :
                pos = pygame.mouse.get_pos()

                if event.type == QUIT :
                    if os.path.exists("save"):
                        os.remove("save")
                    pygame.quit()
                    sys.exit()

                if event.type == MOUSEBUTTONDOWN :
                    if button_new_game.isOver(pos):
                        play_sound(sound_player_select)
                        play_music('music_title.mp3')
                        if os.path.exists("save"):
                            os.remove("save")
                        game = GameState(options_seed, options_difficulty, options_adaptive_difficulty)
                        game.state = "title"

                if event.type == MOUSEMOTION :
                    if button_new_game.isOver(pos):
                        button_new_game.color = LIGHT_GRAY
                    else:
                        button_new_game.color = BLACK

            screen.fill(BLACK)
            screen.blit(txt_game_over, rect_game_over)

            space = 7
            if game.state == "game_over":
                draw_text_center("Score: " + str(round(game.player_state.get_current_gold() * game.difficulty)), 0, space * 1 * SCALE)
                draw_text_center("Seed: " + str(game.seed), 0, space * 2 * SCALE)
                draw_text_center("Total Damage Dealt: " + str(sum(game.encounters_damage_dealt)), 0, space * 4 * SCALE)
                draw_text_center("Total Damage Taken: " + str(sum(game.encounters_damage_taken)), 0, space * 5 * SCALE)
                draw_text_center("Total Damage Blocked: " + str(sum(game.encounters_damage_blocked)), 0, space * 6 * SCALE)
#                draw_text_center("Average Damage Dealt: " + str(round(statistics.mean(game.encounters_damage_dealt))), 0, space * 8 * SCALE)
#                draw_text_center("Average Damage Taken: " + str(round(statistics.mean(game.encounters_damage_taken))), 0, space * 9 * SCALE)
#                draw_text_center("Average Damage Blocked: " + str(round(statistics.mean(game.encounters_damage_blocked))), 0, space * 10 * SCALE)
                draw_text_center("Total Critters Defeated: " + str(len(game.enemies_defeated)), 0, space * 12 * SCALE)
                draw_text_center("Bats: " + str(game.enemies_defeated.count("Bat")), 0, space * 13 * SCALE)
                draw_text_center("Bullfrogs: " + str(game.enemies_defeated.count("Bullfrog")), 0, space * 14 * SCALE)
                draw_text_center("Bunnies: " + str(game.enemies_defeated.count("Bunny")), 0, space * 15 * SCALE)
                draw_text_center("Rats: " + str(game.enemies_defeated.count("Rat")), 0, space * 16 * SCALE)
                draw_text_center("Spiders: " + str(game.enemies_defeated.count("Spider")), 0, space * 17 * SCALE)
                draw_text_center("Snakes: " + str(game.enemies_defeated.count("Snake")), 0, space * 18 * SCALE)

            button_new_game.draw(screen)
            pygame.display.flip()

    if state == "game_win":
            events = pygame.event.get()

            for event in events :
                pos = pygame.mouse.get_pos()

                if event.type == QUIT :
                    if os.path.exists("save"):
                        os.remove("save")
                    pygame.quit()
                    sys.exit()

                if event.type == MOUSEBUTTONDOWN :
                    if button_new_game.isOver(pos):
                        play_sound(sound_player_select)
                        play_music('music_title.mp3')
                        if os.path.exists("save"):
                            os.remove("save")
                        game = GameState(options_seed, options_difficulty, options_adaptive_difficulty)
                        game.state = "title"

                if event.type == MOUSEMOTION :
                    if button_new_game.isOver(pos):
                        button_new_game.color = LIGHT_GRAY
                    else:
                        button_new_game.color = BLACK

            screen.fill(BLACK)
            screen.blit(txt_game_win, rect_game_win)

            space = 7
            if game.state == "game_win":
                draw_text_center("Score: " + str(round(game.player_state.get_current_gold() * game.difficulty)), 0, space * 1 * SCALE)
                draw_text_center("Seed: " + str(game.seed), 0, space * 2 * SCALE)
                draw_text_center("Total Damage Dealt: " + str(sum(game.encounters_damage_dealt)), 0, space * 4 * SCALE)
                draw_text_center("Total Damage Taken: " + str(sum(game.encounters_damage_taken)), 0, space * 5 * SCALE)
                draw_text_center("Total Damage Blocked: " + str(sum(game.encounters_damage_blocked)), 0, space * 6 * SCALE)
#                draw_text_center("Average Damage Dealt: " + str(round(statistics.mean(game.encounters_damage_dealt))), 0, space * 8 * SCALE)
#                draw_text_center("Average Damage Taken: " + str(round(statistics.mean(game.encounters_damage_taken))), 0, space * 9 * SCALE)
#                draw_text_center("Average Damage Blocked: " + str(round(statistics.mean(game.encounters_damage_blocked))), 0, space * 10 * SCALE)
                draw_text_center("Total Critters Defeated: " + str(len(game.enemies_defeated)), 0, space * 12 * SCALE)
                draw_text_center("Bats: " + str(game.enemies_defeated.count("Bat")), 0, space * 13 * SCALE)
                draw_text_center("Bullfrogs: " + str(game.enemies_defeated.count("Bullfrog")), 0, space * 14 * SCALE)
                draw_text_center("Bunnies: " + str(game.enemies_defeated.count("Bunny")), 0, space * 15 * SCALE)
                draw_text_center("Rats: " + str(game.enemies_defeated.count("Rat")), 0, space * 16 * SCALE)
                draw_text_center("Spiders: " + str(game.enemies_defeated.count("Spider")), 0, space * 17 * SCALE)
                draw_text_center("Snakes: " + str(game.enemies_defeated.count("Snake")), 0, space * 18 * SCALE)

            button_new_game.draw(screen)
            pygame.display.flip()

asyncio.run(main())