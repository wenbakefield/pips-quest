import random
import requests
import statistics
import time
import pygame

from Species import Species
from Trait import Trait
from Enemy import Enemy
from Player import Player
from Rune import Rune
from Encounter import Encounter

# initialize pools
def enemy_level_pool_init(difficulty):
    if difficulty == "easy":
        return [[0, 0.50],
                [1, 0.25],
                [2, 0.25],
                [3, 0.00]]
    if difficulty == "normal":
        return [[0, 0.10],
                [1, 0.20],
                [2, 0.50],
                [3, 0.20]]
    if difficulty == "hard":
        return [[0, 0.00],
                [1, 0.25],
                [2, 0.25],
                [3, 0.50]]
    if difficulty == "impossible":
        return [[0, 0.00],
                [1, 0.00],
                [2, 0.00],
                [3, 1.00]]

def enemy_species_pool_init():
    return [[Species("Meerkat"), 0.2],
            [Species("Bullfrog"), 0.2],
            [Species("Bat"), 0.2],
            [Species("Rat"), 0.2],
            [Species("Spider"), 0.2]]

def enemy_trait_pool_init():
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

def enemy_health_pool_init(difficulty):
    if difficulty == "easy":
        return [[1, 1.0],
                [2, 0.0],
                [3, 0.0],
                [4, 0.0],
                [5, 0.0],
                [6, 0.0],
                [7, 0.0],
                [8, 0.0],
                [9, 0.0],
                [10, 0.0]]
    if difficulty == "normal":
        return [[1, 0.0],
                [2, 0.0],
                [3, 0.0],
                [4, 0.0],
                [5, 0.0],
                [6, 0.25],
                [7, 0.25],
                [8, 0.25],
                [9, 0.25],
                [10, 0.0]]
    if difficulty == "hard":
        return [[1, 0.0],
                [2, 0.0],
                [3, 0.0],
                [4, 0.0],
                [5, 0.0],
                [6, 0.0],
                [7, 0.0],
                [8, 0.25],
                [9, 0.25],
                [10, 0.50]]
    if difficulty == "impossible":
        return [[1, 0.0],
                [2, 0.0],
                [3, 0.0],
                [4, 0.0],
                [5, 0.0],
                [6, 0.0],
                [7, 0.0],
                [8, 0.0],
                [9, 0.0],
                [10, 1.0]]

def enemy_power_pool_init(difficulty):
    if difficulty == "easy":
        return [[1, 0.0],
                [2, 0.25],
                [3, 0.50],
                [4, 0.25],
                [5, 0.0],
                [6, 0.0],
                [7, 0.0],
                [8, 0.0],
                [9, 0.0],
                [10, 0.0]]
    if difficulty == "normal":
        return [[1, 0.0],
                [2, 0.0],
                [3, 0.25],
                [4, 0.50],
                [5, 0.25],
                [6, 0.0],
                [7, 0.0],
                [8, 0.0],
                [9, 0.0],
                [10, 0.0]]
    if difficulty == "hard":
        return [[1, 0.0],
                [2, 0.0],
                [3, 0.0],
                [4, 0.25],
                [5, 0.50],
                [6, 0.25],
                [7, 0.0],
                [8, 0.0],
                [9, 0.0],
                [10, 0.0]]
    if difficulty == "impossible":
        return [[1, 0.0],
                [2, 0.0],
                [3, 0.0],
                [4, 0.0],
                [5, 0.25],
                [6, 0.50],
                [7, 0.25],
                [8, 0.0],
                [9, 0.0],
                [10, 0.0]]

def player_element_pool_init():
    return [["F", 0.23],
            ["S", 0.23],
            ["I", 0.23],
            ["E", 0.23],
            ["A", 0.08]]

def player_power_pool_init():
    return [[1, 0.25],
            [2, 0.25],
            [3, 0.25],
            [4, 0.25],
            [5, 0.0],
            [6, 0.0],
            [7, 0.0],
            [8, 0.0],
            [9, 0.0],
            [10, 0.0]]

def player_shop_bonus_pool_init(difficulty):
    if difficulty == "easy":
        return [[0, 0.45],
                [1, 0.55]]
    if difficulty == "normal":
        return [[0, 0.65],
                [1, 0.35]]
    if difficulty == "hard":
        return [[0, 0.85],
                [1, 0.15]]
    if difficulty == "impossible":
        return [[0, 0.99],
                [1, 0.01]]

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

def choose_health_to_gold(difficulty):
    rate = 1
    if difficulty == "easy":
        rate = 0.5
    if difficulty == "normal":
        rate = 1
    if difficulty == "hard":
        rate = 2
    if difficulty == "impossible":
        rate = 4
    return rate

def choose_starting_health(difficulty):
    health = 30
    if difficulty == "easy":
        health = 50
    if difficulty == "normal":
        health = 30
    if difficulty == "hard":
        health = 20
    if difficulty == "impossible":
        health = 10
    return health

def choose_difficulty(game_difficulty):
    global enemy_level_pool
    global enemy_species_pool
    global enemy_trait_pool
    global enemy_health_pool
    global enemy_power_pool

    global player_element_pool
    global player_power_pool
    global shop_bonus_pool
    global game_gold_to_health
    global player_health

    enemy_level_pool = enemy_level_pool_init(game_difficulty)
    enemy_species_pool = enemy_species_pool_init()
    enemy_trait_pool = enemy_trait_pool_init()
    enemy_health_pool = enemy_health_pool_init(game_difficulty)
    enemy_power_pool = enemy_power_pool_init(game_difficulty)

    player_element_pool = player_element_pool_init()
    player_power_pool = player_power_pool_init()
    shop_bonus_pool = player_shop_bonus_pool_init(game_difficulty)
    game_gold_to_health = choose_health_to_gold(game_difficulty)
    player_health = choose_starting_health(game_difficulty)

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
    pygame.mixer.music.load(file_name)
    pygame.mixer.music.play(-1)

def play_music(file_name):
    pygame.mixer.music.load(file_name)
    pygame.mixer.music.play()

def stop_music():
    pygame.mixer.music.stop()

def play_sound(sound):
    sound.play()

# Testing Area
while True:

    pygame.init()
    pygame.mixer.init()
    sound_damage = pygame.mixer.Sound('sound_damage.wav')

    sound_enemy_attack = pygame.mixer.Sound('sound_enemy_attack.wav')
    sound_enemy_defend = pygame.mixer.Sound('sound_enemy_defend.wav')

    sound_player_attack = pygame.mixer.Sound('sound_player_attack.wav')
    sound_player_defend = pygame.mixer.Sound('sound_player_defend.wav')

    sound_player_heal = pygame.mixer.Sound('sound_player_heal.wav')
    sound_player_select = pygame.mixer.Sound('sound_player_select.wav')
    sound_player_spell = pygame.mixer.Sound('sound_player_spell.wav')
    sound_player_sell = pygame.mixer.Sound('sound_player_sell.wav')

    enemy_level_pool = []
    enemy_species_pool = []
    enemy_trait_pool = []
    enemy_health_pool = []
    enemy_power_pool = []

    player_element_pool = []
    player_power_pool = []
    shop_bonus_pool = []

    game_gold_to_health = 2
    game_shop_bonus = 0
    game_black_market_bonus = 0
    player_health = 50

    game_seed = ""
    game_difficulty = ""
    game_battles_fought = 0
    game_damage_given = 0
    game_damage_taken = 0
    game_damage_blocked = 0
    game_battle_length_history = []

    print("\n")
    print("Welcome to the Hamster Game Demo!")
    play_music_loop('music_title.mp3')
    print("\n")

    view_rules = input("Would you like to view the rules? (y/n): ")
    if view_rules == "y":
        print("\n")
        print("You will play as a hamster mage trying to collect as much gold as possible.")
        print("You earn gold by defeating other creatures who are trying to stop you.")
        print("\n")
        print("You will have a collection of runes for each encounter that you can use to craft your spell.")
        print("Each rune has an element type and a power level.")
        print("\n")
        print("Offensive element types are: Fire (F) and Spark (S)")
        print("Defensive element types are: Ice (I) and Earth (E)")
        print("The wildcard element type is: Arcane (A)")
        print("The first rune in your spell will determine whether the spell is offensive or defensive.")
        print("You may not use an arcane rune as the first rune in your spell.")
        print("\n")
        print("In your spell, you can chain runes together if their power level differs by 1.")
        print("Arcane runes will automatically be given a power level that satisfies this rule.")
        print("\n")
        print("Valid spells include:")
        print("F10")
        print("S9 S8 S9 A?")
        print("E3 F2 F3")
        print("I4 F3 E2 S3")
        print("I1 F2 A? S4 F5 E4 I5")
        print("\n")
        print("Runes that you don't use will remain in your hand until you have cleared the area.")
        print("\n")
        print("You will journey through ten areas, with three creatures in each.")
        print("At the end of each area, you will come across a town with some shops.")
        print("\n")
        print("If you are running low on health, you can spend your gold to heal.")
        print("However, you are scored at the end of your adventure based on how much gold you have, so spend wisely.")
        print("On the other hand, if you are running low on gold, you can spend your health to gain gold.")
        print("However, this may result in a quicker defeat for you, so spend wisely.")
        print("\n")
        print("Good luck, and have fun!")
    
    print("\n")
    game_difficulty = input("Enter difficulty (easy, normal, hard, impossible): ")
    if not game_difficulty:
        game_difficulty = "normal"

    game_seed = input("Enter a seed or leave blank for a random seed: ")

    if not game_seed:
        word_site = "https://www.mit.edu/~ecprice/wordlist.10000"
        response = requests.get(word_site)
        words = response.content.splitlines()
        game_seed = str((random.choice(words)).decode('UTF-8'))

    print("Selected seed: %s" % (game_seed))
    print("\n")

    random.seed(game_seed)

    # initialize pools
    choose_difficulty(game_difficulty)

    player = Player(player_health, 0)

    # new encounter loop
    while player.get_current_health() > 0 and game_battles_fought < 31:
        if game_battles_fought != 0 and (game_battles_fought % 3 == 0):
            print("You head to the town to do some shopping...")
            time.sleep(3)
            print("\n")
            print("Welcome to the shop!")
            play_music_loop('music_shop.mp3')

            if game_shop_bonus > 0:
                print("\n")
                print("My favorite customer!")
                print("Ready for a chance to win bonus health?")
                time.sleep(1)
                print("Flipping a coin...")
                time.sleep(3)
                if choose_from(shop_bonus_pool) == 1:
                    print("You win!")
                    print("Here's %s health on the house!" % (game_shop_bonus))
                    print("\n")
                    play_sound(sound_player_heal)
                    player.change_current_health(game_shop_bonus)
                    time.sleep(2)
                else:
                    print("You lose!")
                    print("Better luck next time!")
                    print("\n")
                    time.sleep(2)
                game_shop_bonus = 0

            choose_buy_health = input("Would you like to buy some health? (y/n): ")
            if choose_buy_health == "y":
                game_black_market_bonus = 0
                max_buy_health = player.get_current_gold() // game_gold_to_health
                print("\n")
                print("Your Gold: %s" % (player.get_current_gold()))
                print("Your Health: %s" % (player.get_current_health()))
                print("\n")
                print("The rate is %s gold for 1 health." % (game_gold_to_health))
                print("You can buy a maximum of %s health." % (max_buy_health))
                while True:
                    print("\n")
                    health_to_buy = int(input("How much health would you like to buy? "))
                    if health_to_buy > max_buy_health:
                        print("You can't afford that much health!")
                    elif health_to_buy == 0:
                        print("Second thoughts? No worries, see you next time!")
                        time.sleep(4)
                        break
                    elif health_to_buy == max_buy_health:
                        print("Wow! Big spender!")
                        print("Come see me next time for a chance to win bonus health!")
                        play_sound(sound_player_heal)
                        player.change_current_health(health_to_buy)
                        player.change_current_gold(-health_to_buy * game_gold_to_health)
                        game_shop_bonus = health_to_buy // 2
                        print("\n")
                        print("You now have %s health and %s gold!" % (player.get_current_health(), player.get_current_gold()))
                        print("\n")
                        time.sleep(4)
                        break
                    else:
                        print("Thank you for your purchase!")
                        play_sound(sound_player_heal)
                        player.change_current_health(health_to_buy)
                        player.change_current_gold(-health_to_buy * game_gold_to_health)
                        print("\n")
                        print("You now have %s health and %s gold!" % (player.get_current_health(), player.get_current_gold()))
                        print("\n")
                        time.sleep(4)
                        break
            else:
                print("\n")
                print("Welcome to the black market...")
                play_music_loop('music_black_market.mp3')
                if game_black_market_bonus > 0:
                    print("\n")
                    print("My favorite customer...")
                    print("Ready for a chance to win bonus gold?")
                    time.sleep(1)
                    print("Flipping a coin...")
                    time.sleep(3)
                    if choose_from(shop_bonus_pool) == 1:
                        print("You win...")
                        print("Here's %s gold..." % (game_black_market_bonus))
                        print("\n")
                        play_sound(sound_player_sell)
                        player.change_current_gold(game_black_market_bonus)
                        time.sleep(2)
                    else:
                        print("You lose...")
                        print("Better luck next time...")
                        print("\n")
                        time.sleep(2)
                    game_shop_bonus = 0

                choose_sell_health = input("Would you like to sell some health? (y/n): ")
                if choose_sell_health == "y":
                    max_sell_health = player.get_current_health() - 1
                    print("\n")
                    print("Your Gold: %s" % (player.get_current_gold()))
                    print("Your Health: %s" % (player.get_current_health()))
                    print("\n")
                    print("The rate is 1 health for %s gold..." % (game_gold_to_health / 2))
                    print("You can sell a maximum of %s health..." % (max_sell_health))
                    while True:
                        print("\n")
                        health_to_sell = int(input("How much health would you like to sell? "))
                        if health_to_sell > max_sell_health:
                            print("You can't sell all your health...")
                        elif health_to_sell == 0:
                            print("Understandable. Have a nice day...")
                            time.sleep(4)
                            break
                        elif health_to_sell == max_sell_health:
                            print("Wow... That's a lot of health to part with...")
                            print("Tell you what, if you don't visit the health shop tomorrow and come here instead...")
                            print("I'll give you a chance to win some bonus gold...")
                            play_sound(sound_player_sell)
                            player.change_current_health(-health_to_sell)
                            player.change_current_gold(health_to_sell * (game_gold_to_health / 2))
                            game_black_market_bonus = (health_to_sell // 2) * (game_gold_to_health / 2)
                            time.sleep(4)
                            break
                        else:
                            print("Thank you for your business...")
                            play_sound(sound_player_sell)
                            player.change_current_health(-health_to_sell)
                            player.change_current_gold(health_to_sell * (game_gold_to_health / 2))
                            time.sleep(4)
                            break

        enemy = generate_enemy(enemy_level_pool, enemy_species_pool, enemy_trait_pool, enemy_health_pool, enemy_power_pool)
        player.set_current_hand(generate_player_hand(player.get_current_hand(), player_element_pool, player_power_pool))

        encounter = Encounter(player, enemy)

        print("\n")
        play_music_loop('music_wilderness.mp3')
        print("You journey onward into the wilderness...")
        time.sleep(4)
        print("When suddenly!")
        play_music('music_encounter.mp3')
        time.sleep(4)
        print("A Level %s %s blocks your path!" % (enemy.get_level(), enemy.print_name()))
        play_enemy_music(enemy.get_species().get_name())
        time.sleep(2)

        game_battles_fought += 1
        game_battle_length = 0
        # battle loop
        while True:
            player = encounter.get_player_state()
            enemy = encounter.get_enemy_state()
            print("\n")
            print("The %s's Health: %s" % (enemy.print_name(), enemy.get_current_health()))
            print("Your Health: %s" % (player.get_current_health()))
            time.sleep(1)
            print("It looks like they're going to %s!" % (enemy.get_current_action()))
            time.sleep(1)
            print("\n")
            print("Your rune bag currently contains: %s" % (' '.join([str(rune) for rune in player.get_current_hand()])))
            time.sleep(1)

            while True:
                spell_str = input("Craft your spell: ")
                spell = string_to_spell(spell_str)

                player.set_current_spell(spell)
                if player.has_valid_current_spell():
                    cast = input("Ready to cast? (y/n): ")
                    if cast == "y":
                        player.cast_spell()
                        player.set_current_hand(generate_player_hand(player.get_current_hand(), player_element_pool, player_power_pool))
                        break

            print("Casting spell: %s" % (' '.join([str(rune) for rune in player.get_current_spell()])))
            play_sound(sound_player_spell)
            time.sleep(2)
            print("\n")

            encounter.do_turn(player)
            encounter.display_turn()
            encounter.choose_enemy_action()

            if player.is_dead():
                print("\n")
                print("You were defeated!")
                play_music('music_game_over.mp3')
                time.sleep(3)

                game_battle_length_history.append(game_battle_length)
                break

            if enemy.is_dead():
                print("\n")
                print("The %s was defeated!" % (enemy.print_name()))
                play_music('music_win.mp3')
                time.sleep(4)

                player.change_current_gold(enemy.get_gold())
                print("\n")
                print("You got %s gold!" % (enemy.get_gold()))
                print("You now have %s gold." % (player.get_current_gold()))
                print("\n")
                time.sleep(3)

                input("Press any key to continue...")

                game_battle_length_history.append(game_battle_length)
                break

    print("\n")
    if player.is_dead():
        print("Game over!")
    else:
        print("You win!")
    print("\n")
    print("Difficulty: %s" % (game_difficulty))
    print("Seed: %s" % (game_seed))
    print("Score: %s" % (player.get_current_gold()))
    print("\n")
    print("Battles fought: %s" % (game_battles_fought))
    print("Average turns per battle: %s" % (statistics.mean(game_battle_length_history)))
    print("\n")
    print("Total damage inflicted: %s" % (game_damage_given))
    print("Total damage taken: %s" % (game_damage_taken))
    print("Total damage blocked: %s" % (game_damage_blocked))
    print("\n")
    print("Damage inflicted per battle: %s" % (game_damage_given / game_battles_fought))
    print("Damage taken per battle: %s" % (game_damage_taken / game_battles_fought))
    print("Damage blocked per battle: %s" % (game_damage_blocked / game_battles_fought))
    print("\n")
    print("Thanks for playing!")
    print("\n")
    playing = input("Would you like to play again? (y/n): ")
    if playing == "n":
        break