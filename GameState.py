import random
import requests
import statistics
import time
import pygame
import sys

from pygame.locals import *

from Species import Species
from Trait import Trait
from Enemy import Enemy
from Player import Player
from Rune import Rune
from Encounter import Encounter
from Area import Area

# initialize pools
def choose_enemy_trait_pool():
    return [[Trait("Pesky", -2,-1,0),       (1/60)], 
            [Trait("Annoying", -2,0,-1),    (1/60)], 
            [Trait("Weak", -1,-2,0),        (1/60)], 
            [Trait("Frail", -1,0,-2),       (1/60)], 
            [Trait("Feeble", 0,-2,-1),      (1/60)], 
            [Trait("Sickly", 0,-1,-2),      (1/60)], 
            [Trait("Brash", -2,-1,1),       (1/60)], 
            [Trait("Irritating", -2,1,-1),  (1/60)], 
            [Trait("Cocky", -1,-2,1),       (1/60)], 
            [Trait("Lonely", -1,1,-2),      (1/60)], 
            [Trait("Desperate", 1,-2,-1),   (1/60)], 
            [Trait("Skittish", 1,-1,-2),    (1/60)], 
            [Trait("Shy", -2,-1,2),         (1/60)], 
            [Trait("Coy", -2,0,1),          (1/60)], 
            [Trait("Sheepish", -2,1,0),     (1/60)], 
            [Trait("Nervous", -2,2,-1),     (1/60)], 
            [Trait("Bashful", -1,-2,2),     (1/60)], 
            [Trait("Cautious", -1,2,-2),    (1/60)], 
            [Trait("Sloppy", 0,-2,1),       (1/60)], 
            [Trait("Stubborn", 0,1,-2),     (1/60)], 
            [Trait("Jittery", 1,-2,0),      (1/60)], 
            [Trait("Jumpy", 1,0,-2),        (1/60)], 
            [Trait("Stressed", 2,-2,-1),    (1/60)], 
            [Trait("Frantic", 2,-1,-2),     (1/60)], 
            [Trait("Nonchalant", -2,0,2),   (1/60)], 
            [Trait("Aloof", -2,2,0),        (1/60)], 
            [Trait("Haughty", -1,0,1),      (1/60)], 
            [Trait("Indifferent", -1,1,0),  (1/60)], 
            [Trait("Lazy", 0,-2,2),         (1/60)], 
            [Trait("Calm", 0,-1,1),         (1/60)], 
            [Trait("Reluctant", 0,1,-1),    (1/60)], 
            [Trait("Oblivious", 0,2,-2),    (1/60)], 
            [Trait("Casual", 1,-1,0),       (1/60)], 
            [Trait("Wary", 1,0,-1),         (1/60)], 
            [Trait("Careless", 2,-2,0),     (1/60)], 
            [Trait("Apathetic", 2,0,-2),    (1/60)], 
            [Trait("Placid", -2,1,2),       (1/60)], 
            [Trait("Gentle", -2,2,1),       (1/60)], 
            [Trait("Cool", -1,0,2),         (1/60)], 
            [Trait("Composed", -1,2,0),     (1/60)], 
            [Trait("Chipper", 0,-1,2),      (1/60)], 
            [Trait("Tough", 0,2,-1),        (1/60)], 
            [Trait("Reckless", 1,-2,2),     (1/60)], 
            [Trait("Bold", 1,2,-2),         (1/60)], 
            [Trait("Crazy", 2,-2,1),        (1/60)], 
            [Trait("Lively", 2,-1,0),       (1/60)], 
            [Trait("Vicious", 2,0,-1),      (1/60)], 
            [Trait("Bloodthirsty", 2,1,-2), (1/60)], 
            [Trait("Gritty", -1,1,2),       (1/60)], 
            [Trait("Gutsy", -1,2,1),        (1/60)], 
            [Trait("Daring", 1,-1,2),       (1/60)], 
            [Trait("Fierce", 1,2,-1),       (1/60)], 
            [Trait("Fearless", 2,-1,1),     (1/60)], 
            [Trait("Dangerous", 2,1,-1),    (1/60)], 
            [Trait("Burly", 0,1,2),         (1/60)], 
            [Trait("Sturdy", 0,2,1),        (1/60)], 
            [Trait("Buff", 1,0,2),          (1/60)], 
            [Trait("Mighty", 1,2,0),        (1/60)], 
            [Trait("Brawny", 2,0,1),        (1/60)], 
            [Trait("Heroic", 2,1,0),        (1/60)]]

def choose_enemy_health_pool(difficulty):
    if difficulty < 0:
        return [[6, 0.50],
                [7, 0.25],
                [8, 0.25],
                [9, 0.00]]
    if difficulty == 0:
        return [[6, 0.25],
                [7, 0.25],
                [8, 0.25],
                [9, 0.25]]
    if difficulty > 0:
        return [[6, 0.00],
                [7, 0.25],
                [8, 0.25],
                [9, 0.50]]

def choose_enemy_power_pool(difficulty):
    if difficulty < 0:
        return [[4, 0.25],
                [5, 0.50],
                [6, 0.25]]
    if difficulty == 0:
        return [[5, 0.25],
                [6, 0.50],
                [7, 0.25]]
    if difficulty > 0:
        return [[6, 0.25],
                [7, 0.50],
                [8, 0.25]]

def choose_player_element_pool():
    return [["F", 0.23],
            ["S", 0.23],
            ["I", 0.23],
            ["E", 0.23],
            ["A", 0.08]]

def choose_player_power_pool():
    return [[1, 0.25],
            [2, 0.25],
            [3, 0.25],
            [4, 0.25]]

def choose_area_biome_pool():
    return ["Desert",
            "Cave",
            "Forest",
            "Swamp",
            "Grassland"]

def choose_from(pool):
    sample_list, weight_list = zip(*pool)
    choice = random.choices(sample_list, weight_list, k = 1)
    result = choice[0]
    return result

def generate_rune(element_pool, power_pool):
    element = choose_from(element_pool)
    power = choose_from(power_pool)
    if element == "A":
        power = "?"
    rune = Rune(element, power)
    return rune

def generate_enemy(level_pool, species_pool, trait_pool, health_pool, power_pool):
    level = choose_from(level_pool)
    species = choose_from(species_pool)
    trait = choose_from(trait_pool)

    health = choose_from(health_pool)
    health += choose_from(health_pool)
    health += species.get_health_mod(level)
    health += trait.get_health_mod()

    base_attack = species.get_attack_mod(level)
    base_attack += trait.get_attack_mod()

    base_defense = species.get_defense_mod(level)
    base_defense += trait.get_defense_mod()

    power = choose_from(power_pool)

    action = choose_from(species.get_action_pool())

    gold = species.get_gold_drop(level)
    gold += (trait.get_score() + 4)

    enemy = Enemy(level, species, trait, health, health, base_attack, base_defense, power, action, gold)
    return enemy

def generate_player_hand(current_player_hand, player_element_pool, player_power_pool):
    num_runes_needed = 7 - len(current_player_hand)
    new_player_hand = current_player_hand.copy()
    count = 0
    while count < num_runes_needed:
        new_rune = generate_rune(player_element_pool, player_power_pool)
        if new_rune not in new_player_hand:
            new_player_hand.append(new_rune)
            count += 1
    return new_player_hand

def string_to_spell(spell_str):
    rune_str_list = spell_str.split()
    spell = []
    for rune_str in rune_str_list:
        element = str(rune_str[0])
        power = 0
        if element == "A":
            power = "?"
        else:
            power = int(rune_str[1:])
        rune = Rune(element, power)
        spell.append(rune)
    return spell

def choose_seed():
    word_site = "https://www.mit.edu/~ecprice/wordlist.10000"
    response = requests.get(word_site)
    words = response.content.splitlines()
    game_seed = str((random.choice(words)).decode('UTF-8'))
    return game_seed

class GameState:
    def __init__(self):
        self.seed = choose_seed()
        self.difficulty = 0
        self.adaptive_difficulty = True
        self.enemy_trait_pool = choose_enemy_trait_pool()
        self.enemy_health_pool = choose_enemy_health_pool(self.difficulty)
        self.enemy_power_pool = choose_enemy_power_pool(self.difficulty)
        self.player_power_pool = choose_player_power_pool()
        self.player_element_pool = choose_player_element_pool()
        self.area_biome_pool = choose_area_biome_pool()
        self.player_state = Player(30, 7)
        self.spell_str = ""
        self.area_num = 0
        self.encounter_num = 0
        self.current_area = Area(0, "none")
        self.next_area1 = "none"
        self.next_area2 = "none"
        self.state = "title"

    # game logic

    def set_seed(self, seed):
        self.seed = seed

    def set_difficulty(self, difficulty):
        self.difficulty = difficulty
        self.enemy_health_pool = choose_enemy_health_pool(difficulty)
        self.enemy_power_pool = choose_enemy_power_pool(difficulty)

    def choose_next_area_fork(self):
        biomes = self.area_biome_pool.copy()
        if self.current_area.get_biome() in biomes:
            biomes.remove(self.current_area.get_biome())
        choices = random.sample(biomes, 2)
        self.next_area1 = choices[0]
        self.next_area2 = choices[1]
        self.state = "fork"

    def next_area(self, choice):
        biome = "none"
        if choice == 1:
            biome = self.next_area1
        if choice == 2:
            biome = self.next_area2
        self.area_num += 1
        self.current_area = Area(self.area_num, biome)
        self.encounter_num = 0
        self.state = "wandering"

    def next_encounter(self):
        self.encounter_num += 1
        self.player_state.set_current_hand(generate_player_hand(self.player_state.get_current_hand(), self.player_element_pool, self.player_power_pool))
        enemy = generate_enemy(self.current_area.get_enemy_level_pool(), self.current_area.get_enemy_species_pool(), self.enemy_trait_pool, self.enemy_health_pool, self.enemy_power_pool)
        self.current_area.next_encounter(self.player_state, enemy)
        self.state = "encounter"

    def next_turn(self):
        self.current_area.current_encounter.do_turn(self.player_state)
        if self.player_is_dead():
            self.state = "game over"
        if self.current_enemy_is_dead():
            if self.encounter_num >= 3:
                self.choose_next_area_fork()
        self.current_area.current_encounter.choose_enemy_action()

    def player_cast_spell(self):
        self.player_state.set_current_spell(string_to_spell(self.spell_str))

        if self.player_state.has_valid_current_spell():
            self.player_state.cast_spell()
            self.player_state.set_current_hand(generate_player_hand(self.player_state.get_current_hand(), self.player_element_pool, self.player_power_pool))
            self.next_turn()
        else:
            self.player_state.set_current_spell([])
            self.spell_str = ""

    def current_enemy_is_dead(self):
        return self.current_area.current_encounter.get_enemy_state().is_dead()

    def player_is_dead(self):
        return self.player_state.is_dead()

    def get_current_enemy_species(self):
        return self.current_area.current_encounter.enemy_state.species.name

    def get_current_area_biome(self):
        return self.current_area.get_biome()

    def get_current_enemy_name(self):
        return self.current_area.current_encounter.enemy_state.print_name()

    def get_current_enemy_stats(self):
        return self.current_area.current_encounter.enemy_state.print_stats()

    def get_current_player_stats(self):
        return self.player_state.print_stats()

    def get_current_player_hand(self):
        return "Hand: " + str(' '.join([str(rune) for rune in self.player_state.get_current_hand()]))