from Player import Player
from Enemy import Enemy

class Encounter:
    def __init__(self, player_state_initial, enemy_state_initial):
        self.turn = 0
        self.player_state = player_state_initial
        self.enemy_state = enemy_state_initial
        self.player_damage_dealt = []
        self.player_damage_taken = []
        self.player_damage_blocked = []

    def __repr__(self):
        return "<Encounter |Turn:%s |Player:%s |Enemy:%s >" % (self.turn, self.player_state, self.enemy_state)
    def __str__(self):
        return "<Encounter |Turn:%s |Player:%s |Enemy:%s >" % (self.turn, self.player_state, self.enemy_state)
    def __eq__(self, other):
        if isinstance(other, Encounter):
            return self.turn == other.turn and self.player_state == other.player_state and self.enemy_state == other.enemy_state

    def get_turn(self):
        return self.turn

    def get_player_state(self):
        return self.player_state

    def get_enemy_state(self):
        return self.enemy_state

    def update_player_state(self, new_player_state):
        self.player_state = new_player_state

    def update_enemy_state(self, new_enemy_state):
        self.enemy_state = new_enemy_state

    def get_player_damage_dealt(self):
        return self.player_damage_dealt[-1]

    def get_player_damage_taken(self):
        return self.player_damage_taken[-1]

    def get_player_damage_blocked(self):
        return self.player_damage_blocked[-1]

    def do_turn(self, player_state):
        self.update_player_state(player_state)
        player = self.get_player_state()
        enemy = self.get_enemy_state()

        player_health = player.get_current_health()
        enemy_health = enemy.get_current_health()
        player_action = player.get_current_action()
        enemy_action = enemy.get_current_action()
        player_power = player.get_current_power()
        enemy_power = enemy.get_current_power()
        power_difference = abs(player_power - enemy_power)

        if enemy_action == "attack" and player_action == "attack":
            enemy_power += enemy.get_base_attack()
            if enemy_power > player_health:
                enemy_power = player_health
            if player_power > enemy_health:
                player_power = enemy_health
            player.change_current_health(-enemy_power)
            enemy.change_current_health(-player_power)
            self.player_damage_dealt.append(player_power)
            self.player_damage_taken.append(enemy_power)
            self.player_damage_blocked.append(0)

        elif enemy_action == "defend" and player_action == "attack":
            enemy_power += enemy.get_base_defense()
            power_difference = abs(player_power - enemy_power)
            if player_power > enemy_power:
                if power_difference > enemy_health:
                    power_difference = enemy_health
                enemy.change_current_health(-power_difference)
                self.player_damage_dealt.append(power_difference)
                self.player_damage_taken.append(0)
                self.player_damage_blocked.append(0)

            else:
                self.player_damage_dealt.append(0)
                self.player_damage_taken.append(0)
                self.player_damage_blocked.append(0)

        elif enemy_action == "attack" and player_action == "defend":
            enemy_power += enemy.get_base_attack()
            power_difference = abs(player_power - enemy_power)
            if enemy_power > player_power:
                if power_difference > player_health:
                    power_difference = player_health
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
        self.update_player_state(player)
        self.update_enemy_state(enemy)

    def display_turn(self):
        result = []

        player = self.get_player_state()
        enemy = self.get_enemy_state()
        player_action = player.get_current_action()
        enemy_action = enemy.get_current_action()
        player_power = player.get_current_power()
        enemy_power = enemy.get_current_power()
        enemy_name = enemy.print_name()

        if enemy_action == "attack" and player_action == "attack":
            enemy_power += enemy.get_base_attack()
            result.append("The %s attacks for %s!" % (enemy_name, enemy_power))
            result.append("You attack for %s!" % (player_power))
            result.append("SMAAAASH!!")

        elif enemy_action == "defend" and player_action == "attack":
            enemy_power += enemy.get_base_defense()
            result.append("The %s defends for %s!" % (enemy_name, enemy_power))
            result.append("You attack for %s!" % (player_power))

            if player_power > enemy_power:
                result.append("You do %s damage!" % (self.get_player_damage_dealt()))

            else:
                result.append("The %s blocks your attack!" % (enemy_name))

        elif enemy_action == "attack" and player_action == "defend":
            enemy_power += enemy.get_base_attack()
            result.append("The %s attacks for %s!" % (enemy_name, enemy_power))
            result.append("You defend for %s!" % (player_power))

            if enemy_power > player_power:
                result.append("You take %s damage!" % (self.get_player_damage_taken()))

            else:
                result.append("You block the attack!")

        elif enemy_action == "defend" and player_action == "defend":
            enemy_power += enemy.get_base_defense()
            result.append("The %s defends for %s!" % (enemy_name, enemy_power))
            result.append("You defend for %s!" % (player_power))
            result.append("Nothing happens...")

        else:
            result = []

        return result


    def choose_enemy_action(self):
        self.get_enemy_state().choose_action()