from Player import Player
from Enemy import Enemy
import time

class Encounter:
    def __init__(self, enemy_initial_state):
        self.turn = 0
        self.pre_player_states = []
        self.post_player_states = []
        self.pre_enemy_states = [enemy_initial_state]
        self.post_enemy_states = []
        self.player_damage_dealt = []
        self.player_damage_taken = []
        self.player_damage_blocked = []


    def __repr__(self):
        return "<Encounter |Turn:%s |Player:%s |Enemy:%s >" % (self.turn, self.pre_player_states[0], self.pre_enemy_states[0])
    def __str__(self):
        return "<Encounter |Turn:%s |Player:%s |Enemy:%s >" % (self.turn, self.pre_player_states[0], self.pre_enemy_states[0])
    def __eq__(self, other):
        if isinstance(other, Encounter):
            return self.turn == other.turn and self.pre_player_states == other.pre_player_states and self.pre_enemy_states == other.pre_enemy_states and self.post_player_states == other.post_player_states and self.post_enemy_states == other.post_enemy_states

    def get_turn(self):
        return self.turn

    def get_current_player_state(self):
        return self.pre_player_states[-1]

    def get_current_enemy_state(self):
        return self.pre_enemy_states[-1]

    def update_pre_player_state(self, new_player_state):
        self.pre_player_states.append(new_player_state)

    def update_pre_enemy_state(self, new_enemy_state):
        self.pre_enemy_states.append(new_enemy_state)

    def update_post_player_state(self, new_player_state):
        self.post_player_states.append(new_player_state)

    def update_post_enemy_state(self, new_enemy_state):
        self.post_enemy_states.append(new_enemy_state)

    def get_player_damage_dealt(self):
        return self.player_damage_dealt[-1]

    def get_player_damage_taken(self):
        return self.player_damage_taken[-1]

    def get_player_damage_blocked(self):
        return self.player_damage_blocked[-1]

    def do_turn(self, player):
        enemy = self.get_current_enemy_state()
        self.update_pre_player_state(player)

        player_action = player.get_current_action()
        enemy_action = enemy.get_current_action()
        player_power = player.get_current_power()
        enemy_power = enemy.get_current_power()
        power_difference = abs(player_power - enemy_power)

        if enemy_action == "attack" and player_action == "attack":
            player.change_current_health(-enemy_power)
            enemy.change_current_health(-player_power)
            self.player_damage_dealt.append(player_power)
            self.player_damage_taken.append(enemy_power)
            self.player_damage_blocked.append(0)

        elif enemy_action == "defend" and player_action == "attack":

            if player_power > enemy_power:
                enemy.change_current_health(-power_difference)
                self.player_damage_dealt.append(power_difference)
                self.player_damage_taken.append(0)
                self.player_damage_blocked.append(0)

            else:
                self.player_damage_dealt.append(0)
                self.player_damage_taken.append(0)
                self.player_damage_blocked.append(0)

        elif enemy_action == "attack" and player_action == "defend":

            if enemy_power > player_power:
                player.change_current_health(-power_difference)
                self.player_damage_dealt.append(0)
                self.player_damage_taken.append(power_difference)
                self.player_damage_blocked.append(enemy_power - power_difference)

            else:
                self.player_damage_dealt.append(0)
                self.player_damage_taken.append(0)
                self.player_damage_blocked.append(enemy_power)

        else:
            self.player_damage_dealt.append(0)
            self.player_damage_taken.append(0)
            self.player_damage_blocked.append(0)

        self.turn += 1
        self.update_post_player_state(player)
        self.update_post_enemy_state(enemy)

        enemy.choose_action()

        self.update_pre_enemy_state(enemy)

    def display_turn(self):
        pre_player = self.pre_player_states[-1]
        pre_enemy = self.pre_enemy_states[-2]
        player_action = pre_player.get_current_action()
        enemy_action = pre_enemy.get_current_action()
        player_power = pre_player.get_current_power()
        enemy_power = pre_enemy.get_current_power()
        enemy_name = pre_enemy.print_name()

        if enemy_action == "attack" and player_action == "attack":
            print("The %s attacks for %s!" % (enemy_name, enemy_power))
            print("You attack for %s!" % (player_power))

        elif enemy_action == "defend" and player_action == "attack":
            print("The %s defends for %s!" % (enemy_name, enemy_power))
            print("You attack for %s!" % (player_power))

            if player_power > enemy_power:
                print("You do %s damage!" % (self.get_player_damage_dealt()))

            else:
                print("The %s blocks your attack!" % (enemy_name))

        elif enemy_action == "attack" and player_action == "defend":
            print("You defend for %s!" % (player_power))
            print("The %s attacks for %s!" % (enemy_name, enemy_power))

            if enemy_power > player_power:
                print("You take %s damage!" % (self.get_player_damage_taken()))

            else:
                print("You block the attack!")

        else:
            print("You both defend!")
            print("Nothing happens...")