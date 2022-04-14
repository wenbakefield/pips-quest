from GameState import GameState

import pygame, sys, random, os
import pygame_textinput
from pygame.locals import *
pygame.init()
 
# Colours
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (100, 100, 100)
LIGHT_GRAY = (150, 150, 150)
 
# Game Setup
FPS = 60
clock = pygame.time.Clock()
SCALE = 3
WINDOW_WIDTH = 320 * SCALE
WINDOW_HEIGHT = 240 * SCALE
 
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Pip's Quest")

# assets

# sounds
pygame.mixer.init()

sound_damage = pygame.mixer.Sound(os.path.join('sounds', 'sound_damage.wav'))

sound_enemy_attack = pygame.mixer.Sound(os.path.join('sounds', 'sound_enemy_attack.wav'))
sound_enemy_defend = pygame.mixer.Sound(os.path.join('sounds', 'sound_enemy_defend.wav'))

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
    if species == "Meerkat":
        file_name = 'music_meerkat.mp3'
    if species == "Rat":
        file_name = 'music_rat.mp3'
    if species == "Spider":
        file_name = 'music_spider.mp3'
    play_music_loop(file_name)

def play_music_loop(file_name):
    pygame.mixer.music.load(os.path.join('sounds', file_name))
    pygame.mixer.music.play(-1)

def play_music(file_name):
    pygame.mixer.music.load(os.path.join('sounds', file_name))
    pygame.mixer.music.play()

def stop_music():
    pygame.mixer.music.stop()

def play_sound(sound):
    sound.play()

# fonts
font_title = pygame.font.Font(os.path.join('fonts', 'AncientModernTales-a7Po.ttf'), 50 * SCALE)
font_subtitle = pygame.font.Font(os.path.join('fonts', 'AncientModernTales-a7Po.ttf'), 20 * SCALE)
font_button = pygame.font.Font(os.path.join('fonts', 'AGoblinAppears-o2aV.ttf'), 5 * SCALE)
font_text = pygame.font.Font(os.path.join('fonts', 'AGoblinAppears-o2aV.ttf'), 5 * SCALE)

# text
txt_title = font_title.render("Pip's Quest", False, WHITE, None)
txt_options = font_subtitle.render("Options", False, WHITE, None)
txt_seed = font_text.render("Seed:                                            ", False, WHITE, BLACK)
txt_fork = font_subtitle.render("Where To?", False, WHITE, None)
txt_wandering = font_subtitle.render("Wandering...", False, WHITE, None)
txt_spell = font_text.render("Spell:                                          ", False, WHITE, BLACK)
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

class Bat(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__()
        self.idle_sprites = []
        self.is_animating = True
        for i in range(1, 5):
            image = pygame.image.load(os.path.join('images', 'mob_bat', 'idle', str(i) + '.png')).convert_alpha()
            image = pygame.transform.scale(image, (65 * SCALE, 65 * SCALE))
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

class Bullfrog(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__()
        self.idle_sprites = []
        self.is_animating = True
        for i in range(1, 5):
            image = pygame.image.load(os.path.join('images', 'mob_bullfrog', 'idle', str(i) + '.png')).convert_alpha()
            image = pygame.transform.scale(image, (65 * SCALE, 65 * SCALE))
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

class Meerkat(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__()
        self.idle_sprites = []
        self.is_animating = True
        for i in range(1, 5):
            image = pygame.image.load(os.path.join('images', 'mob_meerkat', 'idle', str(i) + '.png')).convert_alpha()
            image = pygame.transform.scale(image, (65 * SCALE, 65 * SCALE))
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

class Rat(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__()
        self.idle_sprites = []
        self.is_animating = True
        for i in range(1, 5):
            image = pygame.image.load(os.path.join('images', 'mob_rat', 'idle', str(i) + '.png')).convert_alpha()
            image = pygame.transform.scale(image, (65 * SCALE, 65 * SCALE))
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

class Snake(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__()
        self.idle_sprites = []
        self.is_animating = True
        for i in range(1, 5):
            image = pygame.image.load(os.path.join('images', 'mob_snake', 'idle', str(i) + '.png')).convert_alpha()
            image = pygame.transform.scale(image, (65 * SCALE, 65 * SCALE))
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

class Spider(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__()
        self.idle_sprites = []
        self.is_animating = True
        for i in range(1, 5):
            image = pygame.image.load(os.path.join('images', 'mob_spider', 'idle', str(i) + '.png')).convert_alpha()
            image = pygame.transform.scale(image, (65 * SCALE, 65 * SCALE))
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

# sprite groups

moving_sprites = pygame.sprite.Group()

# rects
rect_bg = bg_title.get_rect()
rect_bg = rect_bg.move((0, 0))

rect_title = txt_title.get_rect()
rect_title.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)
rect_title = rect_title.move((0, -400 / 5 * SCALE))

rect_seed = txt_seed.get_rect()
rect_seed.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)
rect_seed = rect_seed.move((0, -300 / 5 * SCALE))

rect_spell = txt_spell.get_rect()
rect_spell.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)
rect_spell = rect_spell.move((0, 575 / 5 * SCALE))

rect_subtitle = txt_fork.get_rect()
rect_subtitle.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)
rect_subtitle = rect_subtitle.move((0, -500 / 5 * SCALE))

rect_mob = mob_bat.get_rect()
rect_mob.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)
rect_mob = rect_mob.move((0, 150 / 5 * SCALE))

rect_boss = mob_snake.get_rect()
rect_boss.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)
rect_boss = rect_boss.move((0, 150 / 5 * SCALE))

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

# buttons
button_new_game = button(BLACK, (WINDOW_WIDTH // 2) - (125 / 5 * SCALE), (WINDOW_HEIGHT // 2) + (450 / 5 * SCALE), 250 / 5 * SCALE, 90 / 5 * SCALE, 'new game')
button_confirm = button(BLACK, (WINDOW_WIDTH // 2) - (125 / 5 * SCALE), (WINDOW_HEIGHT // 2) + (450 / 5 * SCALE), 250 / 5 * SCALE, 90 / 5 * SCALE, 'confirm')
button_fork_left = button(BLACK, (WINDOW_WIDTH // 2) - (525 / 5 * SCALE), (WINDOW_HEIGHT // 2), (250  / 5 * SCALE), (90 / 5 * SCALE), 'left')
button_fork_right = button(BLACK, (WINDOW_WIDTH // 2) + (275 / 5 * SCALE), (WINDOW_HEIGHT // 2), (250 / 5 * SCALE), (90 / 5 * SCALE), 'right')

# text input
seed_input = pygame_textinput.TextInputVisualizer()
seed_input.font_color = WHITE
seed_input.font_object = font_text
seed_input.cursor_color = WHITE

spell_input = pygame_textinput.TextInputVisualizer()
spell_input.font_color = WHITE
spell_input.font_object = font_text
spell_input.cursor_color = WHITE

game = GameState()
seed_input.value = game.seed
seed_input.manager.cursor_pos = len(seed_input.value)
turn_results = []

# The main function that controls the game
def main () :
    running = True
    play_music('music_title.mp3')
    while running :
        draw_state(game.state)
        pygame.display.update()
        clock.tick(FPS)

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
        moving_sprites.add(Bat(0, 0))
    if enemy_name == "Bullfrog":
        moving_sprites.add(Bullfrog(0, 140 / 5 * SCALE))
    if enemy_name == "Meerkat":
        moving_sprites.add(Meerkat(0, 140 / 5 * SCALE))
    if enemy_name == "Rat":
        moving_sprites.add(Rat(0, 140 / 5 * SCALE))
    if enemy_name == "Spider":
        moving_sprites.add(Spider(0, 140 / 5 * SCALE))

def draw_turn_result(turn_result):
    if turn_result:
        space = 0
        for line in turn_result:
            txt_result = font_text.render(str(line), False, WHITE, BLACK)
            screen.blit(txt_result, (5 / 5 * SCALE, (160 + space) / 5 * SCALE))
            space += txt_result.get_rect().height * 2

def draw_state(state):
    global game
    global turn_result
    if state == "title":
        events = pygame.event.get()

        for event in events :
            pos = pygame.mouse.get_pos()

            if event.type == QUIT :
                pygame.quit()
                sys.exit()

            if event.type == MOUSEBUTTONDOWN :
                if button_new_game.isOver(pos):
                    play_sound(sound_player_attack)
                    play_music_loop('music_options.mp3')
                    game.state = "options"

            if event.type == MOUSEMOTION :
                if button_new_game.isOver(pos):
                    button_new_game.color = LIGHT_GRAY
                else:
                    button_new_game.color = BLACK

        screen.blit(bg_title, rect_bg)
        screen.blit(txt_title, rect_title)
        button_new_game.draw(screen)
        pygame.display.flip()

    if state == "options":
        events = pygame.event.get()

        seed_input.update(events)

        for event in events :
            pos = pygame.mouse.get_pos()

            if event.type == QUIT :
                pygame.quit()
                sys.exit()

            if event.type == MOUSEBUTTONDOWN :
                if button_confirm.isOver(pos):

                    moving_sprites.empty() # fix this

                    play_sound(sound_player_select)
                    game.seed = seed_input.value
                    game.choose_next_area_fork()
                    game.state = "fork"
                    play_music_loop('music_wilderness.mp3')

            if event.type == MOUSEMOTION :
                if button_confirm.isOver(pos):
                    button_confirm.color = LIGHT_GRAY
                else:
                    button_confirm.color = BLACK

        screen.blit(bg_title, rect_bg)
        screen.blit(txt_options, rect_subtitle)
        screen.blit(txt_seed, rect_seed)
        screen.blit(seed_input.surface, rect_seed.move(150 / 5 * SCALE, 0))
        button_confirm.draw(screen)
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

            if event.type == MOUSEBUTTONDOWN :
                if button_fork_left.isOver(pos):
                    play_sound(sound_player_select)
                    pygame.time.set_timer(pygame.USEREVENT + 1, 2000, 1)
                    game.next_area(1)
                    if game.area_num >= 6:
                        play_music('music_game_win.mp3')
                        game.state = "game_win"
                    else:
                        play_music_loop('music_wilderness.mp3')
                        game.state = "wandering"
                if button_fork_right.isOver(pos):
                    play_sound(sound_player_select)
                    pygame.time.set_timer(pygame.USEREVENT + 1, 2000, 1)
                    game.next_area(2)
                    if game.area_num >= 6:
                        play_music('music_game_win.mp3')
                        game.state = "game_win"
                    else:
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
        button_fork_left.draw(screen)
        button_fork_right.draw(screen)
        pygame.display.flip()

    if state == "wandering":
        
        events = pygame.event.get()

        for event in events :

            if event.type == QUIT :
                pygame.quit()
                sys.exit()

            if event.type == USEREVENT + 2:
                game.next_encounter()
                draw_enemy(game.get_current_enemy_species())
                play_enemy_music(game.get_current_enemy_species())
                game.state = "encounter"

            if event.type == USEREVENT + 1:
                play_music('music_encounter.mp3')
                pygame.time.set_timer(pygame.USEREVENT + 2, 4000, 1)

        draw_background(game.get_current_area_biome())
        screen.blit(txt_wandering, rect_subtitle)
        pygame.display.flip()

    if state == "encounter":
        events = pygame.event.get()
        spell_input.update(events)

        game.spell_str = spell_input.value

        for event in events :
            if event.type == QUIT :
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    play_sound(sound_player_spell)
                    game.player_cast_spell()
                    spell_input.value = ""

                    if game.player_is_dead():
                        game.state = "game_over"
                        play_music('music_game_over.mp3')

                    if game.current_enemy_is_dead():
                        moving_sprites.empty()
                        game.give_current_enemy_gold_to_player()
                        if game.encounter_num >= 3:
                            game.choose_next_area_fork()
                            game.state = "fork"
                        else:
                            pygame.time.set_timer(pygame.USEREVENT + 1, 2000, 1)
                            game.state = "wandering"
                        play_music_loop('music_wilderness.mp3')

        draw_background(game.get_current_area_biome())
        
        moving_sprites.draw(screen)
        moving_sprites.update(0.1)

        txt_enemy_name = font_subtitle.render(game.get_current_enemy_name(), False, WHITE, BLACK)
        txt_enemy_stats = font_text.render(game.get_current_enemy_stats(), False, WHITE, BLACK)
        txt_player_name = font_subtitle.render("Pip", False, WHITE, BLACK)
        txt_player_stats = font_text.render(game.get_current_player_stats(), False, WHITE, BLACK)

        txt_player_hand = font_text.render(game.get_current_player_hand(), False, WHITE, BLACK)
        
        screen.blit(txt_enemy_name, (5 / 5 * SCALE, 10 / 5 * SCALE))
        screen.blit(txt_enemy_stats, (5 / 5 * SCALE, 130 / 5 * SCALE))
        screen.blit(txt_player_name, (5 / 5 * SCALE, WINDOW_HEIGHT - (150 / 5 * SCALE)))
        screen.blit(txt_player_stats, (5 / 5 * SCALE, WINDOW_HEIGHT - (30 / 5 * SCALE)))

        screen.blit(txt_player_hand, ((WINDOW_WIDTH // 2) - (280 / 5 * SCALE), WINDOW_HEIGHT - (65 / 5 * SCALE)))
        screen.blit(txt_spell, rect_spell)
        screen.blit(spell_input.surface, rect_spell.move(120 / 5 * SCALE, 0))

        draw_turn_result(game.turn_result)

        pygame.display.flip()

    if state == "game_over":
            events = pygame.event.get()

            for event in events :
                pos = pygame.mouse.get_pos()

                if event.type == QUIT :
                    pygame.quit()
                    sys.exit()

                if event.type == MOUSEBUTTONDOWN :
                    if button_new_game.isOver(pos):
                        play_sound(sound_player_select)
                        play_music_loop('music_options.mp3')
                        game = GameState()
                        game.state = "options"

                if event.type == MOUSEMOTION :
                    if button_new_game.isOver(pos):
                        button_new_game.color = LIGHT_GRAY
                    else:
                        button_new_game.color = BLACK

            screen.blit(bg_title, rect_bg)
            screen.blit(txt_game_over, rect_title)
            txt_score = font_subtitle.render("Score: " + str(game.player_state.get_current_gold()), False, WHITE, None)
            rect_score = txt_score.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
            screen.blit(txt_score, rect_score)
            button_new_game.draw(screen)
            pygame.display.flip()

    if state == "game_win":
            events = pygame.event.get()

            for event in events :
                pos = pygame.mouse.get_pos()

                if event.type == QUIT :
                    pygame.quit()
                    sys.exit()

                if event.type == MOUSEBUTTONDOWN :
                    if button_new_game.isOver(pos):
                        play_sound(sound_player_select)
                        play_music_loop('music_options.mp3')
                        game = GameState()
                        game.state = "options"

                if event.type == MOUSEMOTION :
                    if button_new_game.isOver(pos):
                        button_new_game.color = LIGHT_GRAY
                    else:
                        button_new_game.color = BLACK

            screen.blit(bg_title, rect_bg)
            screen.blit(txt_game_win, rect_title)
            txt_score = font_subtitle.render("Score: " + str(game.player_state.get_current_gold()), False, WHITE, None)
            rect_score = txt_score.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
            screen.blit(txt_score, rect_score)
            button_new_game.draw(screen)
            pygame.display.flip()

if __name__=="__main__":
    main()