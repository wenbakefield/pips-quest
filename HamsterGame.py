import random
import requests
import statistics
import time
import pygame

from Species import Species
from Trait import Trait
from Enemy import Enemy

# initialize pools
def enemy_level_pool_init(difficulty):
    if difficulty == "easy":
        return [[0, 0.50],
                [1, 0.25],
                [2, 0.25],
                [3, 0.00]]
    if difficulty == "normal":
        return [[0, 0.25],
                [1, 0.25],
                [2, 0.25],
                [3, 0.25]]
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
    return [[Trait("Reserved"), 0.1],
            [Trait("Brave"), 0.1],
            [Trait("Reckless"), 0.1],
            [Trait("Cocky"), 0.1],
            [Trait("Buff"), 0.1],
            [Trait("Cheerful"), 0.1],
            [Trait("Lonely"), 0.1],
            [Trait("Desperate"), 0.1],
            [Trait("Weird"), 0.1],
            [Trait("Aloof"), 0.1]]

def enemy_health_pool_init(difficulty):
    if difficulty == "easy":
        return [[1, 0.2],
                [2, 0.2],
                [3, 0.2],
                [4, 0.2],
                [5, 0.2],
                [6, 0.0],
                [7, 0.0],
                [8, 0.0],
                [9, 0.0],
                [10, 0.0]]
    if difficulty == "normal":
        return [[1, 0.1],
                [2, 0.1],
                [3, 0.1],
                [4, 0.1],
                [5, 0.1],
                [6, 0.1],
                [7, 0.1],
                [8, 0.1],
                [9, 0.1],
                [10, 0.1]]
    if difficulty == "hard":
        return [[1, 0.0],
                [2, 0.0],
                [3, 0.0],
                [4, 0.0],
                [5, 0.0],
                [6, 0.2],
                [7, 0.2],
                [8, 0.2],
                [9, 0.2],
                [10, 0.2]]
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
        return [[1, 0.2],
                [2, 0.2],
                [3, 0.2],
                [4, 0.2],
                [5, 0.2],
                [6, 0.0],
                [7, 0.0],
                [8, 0.0],
                [9, 0.0],
                [10, 0.0]]
    if difficulty == "normal":
        return [[1, 0.1],
                [2, 0.1],
                [3, 0.1],
                [4, 0.1],
                [5, 0.1],
                [6, 0.1],
                [7, 0.1],
                [8, 0.1],
                [9, 0.1],
                [10, 0.1]]
    if difficulty == "hard":
        return [[1, 0.0],
                [2, 0.0],
                [3, 0.0],
                [4, 0.0],
                [5, 0.0],
                [6, 0.2],
                [7, 0.2],
                [8, 0.2],
                [9, 0.2],
                [10, 0.2]]
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

def player_power_pool_init():
    return [[1, 0.1],
            [2, 0.1],
            [3, 0.1],
            [4, 0.1],
            [5, 0.1],
            [6, 0.1],
            [7, 0.1],
            [8, 0.1],
            [9, 0.1],
            [10, 0.1]]

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
    r, s = random.random(), 0
    for item in pool:
        s += item[1]
        if s >= r:
            return item[0]

def make_enemy(level_pool, species_pool, trait_pool, health_pool):
    level = choose_from(level_pool)
    species = choose_from(species_pool)
    trait = choose_from(trait_pool)
    health = []
    health.append(choose_from(health_pool))
    health.append(choose_from(health_pool))
    enemy = Enemy(level, species, trait, health)
    return enemy

def make_enemies(num_enemies, level_pool, species_pool, trait_pool, health_pool):
    enemies = []
    count = 0
    while count < num_enemies:
        current_enemy = make_enemy(level_pool, species_pool, trait_pool, health_pool)
        enemies.append(current_enemy)
        count += 1
    return enemies

def draw_hand(current_player_hand, player_power_pool):
    num_cards_needed = 7 - len(current_player_hand)
    new_player_hand = current_player_hand.copy()
    count = 0
    while count < num_cards_needed:
        new_card = choose_from(player_power_pool)
        new_player_hand.append(new_card)
        count += 1
    return new_player_hand

def remove_spell_from_hand(spell, hand):
    hand_temp = hand.copy()
    for card in spell:
        if (card in hand_temp):
            hand_temp.remove(card)
    return hand_temp

def is_valid_spell(spell, hand):
    if not spell:
        return False
    hand_temp = hand.copy()
    for card in spell:
        if (card in hand_temp):
            hand_temp.remove(card)
        else:
            return False
    for i in range(1, len(spell)):
        if abs(spell[i - 1] - spell[i]) != 1:
            return False
    return True

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
    health = 50
    if difficulty == "easy":
        health = 100
    if difficulty == "normal":
        health = 50
    if difficulty == "hard":
        health = 25
    if difficulty == "impossible":
        health = 10
    return health

def choose_difficulty(player_difficulty):
    global enemy_level_pool
    global enemy_species_pool
    global enemy_trait_pool
    global enemy_health_pool
    global enemy_power_pool

    global player_power_pool
    global player_shop_bonus_pool
    global player_gold_to_health
    global player_health

    enemy_level_pool = enemy_level_pool_init(player_difficulty)
    enemy_species_pool = enemy_species_pool_init()
    enemy_trait_pool = enemy_trait_pool_init()
    enemy_health_pool = enemy_health_pool_init(player_difficulty)
    enemy_power_pool = enemy_power_pool_init(player_difficulty)

    player_power_pool = player_power_pool_init()
    player_shop_bonus_pool = player_shop_bonus_pool_init(player_difficulty)
    player_gold_to_health = choose_health_to_gold(player_difficulty)
    player_health = choose_starting_health(player_difficulty)

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

player_power_pool = []
player_shop_bonus_pool = []
player_gold_to_health = 2
player_shop_bonus = 0
player_black_market_bonus = 0
player_health = 50

player_gold = 0
player_hand = []
player_spell = []
player_action = ""
player_seed = ""
player_difficulty = ""
player_battles_fought = 0
player_total_damage_inflicted = 0
player_total_damage_taken = 0
player_total_damage_blocked = 0
player_battle_lengths = []

while True:
    print("\n")
    print("Welcome to the Critter Battle Simulator!")
    play_music_loop('music_title.mp3')

    player_difficulty = input("Enter difficulty (easy, normal, hard, impossible): ")
    if not player_difficulty:
        player_difficulty = "normal"

    player_seed = input("Enter a seed or leave blank for a random seed: ")

    if not player_seed:
        word_site = "https://www.mit.edu/~ecprice/wordlist.10000"
        response = requests.get(word_site)
        words = response.content.splitlines()
        player_seed = str((random.choice(words)).decode('UTF-8'))

    print("Selected seed: %s" % (player_seed))
    print("\n")

    random.seed(player_seed)

    # initialize pools
    choose_difficulty(player_difficulty)

    # new encounter loop
    while player_health > 0:
        if player_battles_fought > 2:
            print("You head to the town to do some shopping...")
            time.sleep(3)
            print("\n")
            print("Welcome to the shop!")
            play_music_loop('music_shop.mp3')

            if player_shop_bonus > 0:
                print("\n")
                print("My favorite customer!")
                print("Ready for a chance to win bonus health?")
                time.sleep(1)
                print("Flipping a coin...")
                time.sleep(3)
                if choose_from(player_shop_bonus_pool) == 1:
                    print("You win!")
                    print("Here's %s health on the house!" % (player_shop_bonus))
                    print("\n")
                    play_sound(sound_player_heal)
                    player_health += player_shop_bonus
                    time.sleep(2)
                else:
                    print("You lose!")
                    print("Better luck next time!")
                    print("\n")
                    time.sleep(2)
                player_shop_bonus = 0

            choose_buy_health = input("Would you like to buy some health? (yes/no): ")
            if choose_buy_health == "yes":
                player_black_market_bonus = 0
                max_buy_health = player_gold // player_gold_to_health
                print("\n")
                print("The rate is %s gold for 1 health." % (player_gold_to_health))
                print("You have %s gold." % (player_gold))
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
                        player_health += health_to_buy
                        player_gold -= health_to_buy * player_gold_to_health
                        player_shop_bonus = health_to_buy // 2
                        time.sleep(4)
                        break
                    else:
                        print("Thank you for your purchase!")
                        play_sound(sound_player_heal)
                        player_health += health_to_buy
                        player_gold -= health_to_buy * player_gold_to_health
                        time.sleep(4)
                        break
            else:
                print("\n")
                print("Welcome to the black market...")
                play_music_loop('music_black_market.mp3')
                if player_black_market_bonus > 0:
                    print("\n")
                    print("My favorite customer...")
                    print("Ready for a chance to win bonus gold?")
                    time.sleep(1)
                    print("Flipping a coin...")
                    time.sleep(3)
                    if choose_from(player_shop_bonus_pool) == 1:
                        print("You win...")
                        print("Here's %s gold..." % (player_black_market_bonus))
                        print("\n")
                        play_sound(sound_player_sell)
                        player_gold += player_black_market_bonus
                        time.sleep(2)
                    else:
                        print("You lose...")
                        print("Better luck next time...")
                        print("\n")
                        time.sleep(2)
                    player_shop_bonus = 0

                choose_sell_health = input("Would you like to sell some health? (yes/no): ")
                if choose_sell_health == "yes":
                    max_sell_health = player_health - 1
                    print("\n")
                    print("The rate is 1 health for %s gold..." % (player_gold_to_health / 2))
                    print("You have %s health..." % (player_health))
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
                            player_black_market_bonus = (health_to_sell // 2) * (player_gold_to_health / 2)
                            time.sleep(4)
                            break
                        else:
                            print("Thank you for your business...")
                            play_sound(sound_player_sell)
                            player_health -= health_to_sell
                            player_gold += health_to_sell * (player_gold_to_health / 2)
                            time.sleep(4)
                            break

        current_enemy = make_enemy(enemy_level_pool, enemy_species_pool, enemy_trait_pool, enemy_health_pool)
        current_enemy_health = current_enemy.get_health()
        current_enemy_base_attack = current_enemy.get_attack()
        current_enemy_base_defense = current_enemy.get_defense()
        current_enemy_action_pool = current_enemy.get_action_pool()
        current_enemy_gold_drop = current_enemy.get_gold_drop()
        current_enemy_name = current_enemy.get_name()
        current_enemy_level = current_enemy.get_level()
        print("\n")
        play_music_loop('music_wilderness.mp3')
        print("Day %s" % (player_battles_fought + 1))
        print("You're out scrounging for food in the wilderness...")
        time.sleep(4)
        print("When suddenly!")
        play_music('music_encounter.mp3')
        time.sleep(4)

        print("You encounter a %s (Level %s)!" % (current_enemy_name, current_enemy_level + 1))
        play_enemy_music(current_enemy.get_species().get_name())
        time.sleep(2)

        player_battles_fought += 1
        player_num_turns = 0
        # battle loop
        while True:
            print("\n")
            
            print("The %s's Health: %s" % (current_enemy_name, current_enemy_health))
            print("Your Health: %s" % (player_health))
            time.sleep(1)

            current_enemy_action = choose_from(current_enemy_action_pool)
            print("It looks like they're going to %s!" % (current_enemy_action))
            time.sleep(1)

            current_enemy_power = choose_from(enemy_power_pool)

            print("\n")

            player_hand = draw_hand(player_hand, player_power_pool)
            print("Your current hand is: %s" % (' '.join([str(card) for card in player_hand])))
            time.sleep(1)

            while True:
                player_action = input("Would you like to attack or defend?: ")
                if player_action == "attack" or player_action == "defend":
                    break
                else:
                    print("Invalid action!")

            while not is_valid_spell(player_spell, player_hand):
                spell_str = input("Craft your spell: ")
                player_spell = [int(num) for num in spell_str.split()]
                if not is_valid_spell(player_spell, player_hand):
                    print("That's not a spell! Numbers in your spell must only be one apart and can only be used once from your hand.")

            play_sound(sound_player_spell)
            time.sleep(2)
            player_hand = remove_spell_from_hand(player_spell, player_hand)
            player_power = sum(player_spell)

            print("\n")

            if current_enemy_action == "attack" and player_action == "attack":
                player_health = player_health - current_enemy_power
                current_enemy_health = current_enemy_health - player_power

                player_total_damage_inflicted += player_power
                player_total_damage_taken += current_enemy_power

                print("The %s attacks for %s!" % (current_enemy_name, current_enemy_power))
                play_sound(sound_enemy_attack)
                time.sleep(1)
                play_sound(sound_damage)
                time.sleep(1)

                print("You attack for %s!" % (player_power))
                play_sound(sound_player_attack)
                time.sleep(1)
                play_sound(sound_damage)
                time.sleep(1)

            elif current_enemy_action == "defend" and player_action == "attack":
                print("The %s defends for %s!" % (current_enemy_name, current_enemy_power))
                play_sound(sound_enemy_defend)
                time.sleep(1)
                print("You attack for %s!" % (player_power))
                play_sound(sound_player_attack)
                time.sleep(1)

                if player_power > current_enemy_power:
                    player_damage = abs(current_enemy_power - player_power)
                    current_enemy_health -= player_damage

                    player_total_damage_inflicted += player_damage

                    print("You do %s damage!" % (player_damage))
                    play_sound(sound_damage)
                    time.sleep(1)

                else:
                    print("The %s blocks your attack!" % (current_enemy_name))
                    play_sound(sound_damage)
                    time.sleep(1)


            elif current_enemy_action == "attack" and player_action == "defend":
                print("You defend for %s!" % (player_power))
                play_sound(sound_player_defend)
                time.sleep(1)

                print("The %s attacks for %s!" % (current_enemy_name, current_enemy_power))
                play_sound(sound_enemy_attack)
                time.sleep(1)

                if current_enemy_power > player_power:
                    current_enemy_damage = abs(player_power - current_enemy_power)
                    player_health -= current_enemy_damage

                    player_total_damage_taken += current_enemy_damage

                    print("You take %s damage!" % (current_enemy_damage))
                    play_sound(sound_damage)
                    time.sleep(1)

                else:
                    player_total_damage_blocked += current_enemy_power
                    print("You block the attack!")
                    play_sound(sound_damage)
                    time.sleep(1)

            else:
                print("You both defend!")
                play_sound(sound_player_defend)
                time.sleep(1)
                play_sound(sound_enemy_defend)
                time.sleep(1)
                print("Nothing happens...")
                time.sleep(2)

            player_num_turns += 1

            player_action = ""
            player_spell = []

            if player_health <= 0:
                print("\n")
                print("You were defeated!")
                play_music('music_game_over.mp3')
                time.sleep(3)

                player_battle_lengths.append(player_num_turns)
                break

            if current_enemy_health <= 0:
                print("\n")
                print("The %s was defeated!" % (current_enemy_name))
                play_music('music_win.mp3')
                time.sleep(4)

                player_gold += current_enemy_gold_drop
                print("\n")
                print("You got %s gold!" % (current_enemy_gold_drop))
                print("You now have %s gold." % (player_gold))
                print("\n")
                time.sleep(3)

                input("Time to head back...")

                player_battle_lengths.append(player_num_turns)
                break

    print("\n")
    print("Game over!")
    print("\n")
    print("Difficulty: %s" % (player_difficulty))
    print("Seed: %s" % (player_seed))
    print("Score: %s" % (player_gold))
    print("\n")
    print("Battles fought: %s" % (player_battles_fought))
    print("Average turns per battle: %s" % (statistics.mean(player_battle_lengths)))
    print("\n")
    print("Total damage inflicted: %s" % (player_total_damage_inflicted))
    print("Total damage taken: %s" % (player_total_damage_taken))
    print("Total damage blocked: %s" % (player_total_damage_blocked))
    print("\n")
    print("Damage inflicted per battle: %s" % (player_total_damage_inflicted / player_battles_fought))
    print("Damage taken per battle: %s" % (player_total_damage_taken / player_battles_fought))
    print("Damage blocked per battle: %s" % (player_total_damage_blocked / player_battles_fought))
    print("\n")
    print("Thanks for playing!")
    print("\n")
    playing = input("Would you like to play again? (yes/no): ")
    if playing == "no":
        break