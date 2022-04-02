from Rune import Rune

class Player:
    def __init__(self, current_health, max_health, current_gold, current_hand, max_hand, current_spell, current_power, current_action):
        self.current_health = current_health
        self.max_health = max_health
        self.current_gold = current_gold
        self.current_hand = current_hand
        self.max_hand = max_hand
        self.current_spell = current_spell
        self.current_power = current_power
        self.current_action = current_action

    def __repr__(self):
        return "<Player |Current Health:%s |Max Health:%s |Gold:%s |Hand:%s |Max Hand:%s |Spell:%s |Power:%s |Action:%s >" % (self.current_health,
                                                                                                           self.max_health, 
                                                                                                           self.current_gold, 
                                                                                                           self.current_hand,
                                                                                                           self.max_hand,
                                                                                                           self.current_spell,
                                                                                                           self.current_power,
                                                                                                           self.current_action)
    
    def __str__(self):
        return "<Player |Current Health:%s |Max Health:%s |Gold:%s |Hand:%s |Max Hand:%s |Spell:%s |Power:%s |Action:%s >" % (self.current_health,
                                                                                                           self.max_health, 
                                                                                                           self.current_gold, 
                                                                                                           self.current_hand,
                                                                                                           self.max_hand,
                                                                                                           self.current_spell,
                                                                                                           self.current_power,
                                                                                                           self.current_action)

    def get_current_health(self):
        return self.current_health

    def get_max_health(self):
        return self.max_health

    def get_current_gold(self):
        return self.current_gold

    def get_current_hand(self):
        return self.current_hand

    def get_current_spell(self):
        return self.current_spell

    def get_current_power(self):
        return self.current_power

    def get_current_action(self):
        return self.current_action

    def set_current_health(self, health):
        self.current_health = health

    def set_max_health(self, health):
        self.max_health = health

    def set_current_gold(self, gold):
        self.current_gold = gold

    def set_current_hand(self, hand):
        self.current_hand = hand

    def set_current_spell(self, spell):
        self.current_spell = spell

    def set_current_power(self):
        self.current_power = 0
        for rune in self.current_spell:
            self.current_power += rune.get_power()

    def set_current_action(self):
        if not self.current_spell:
            self.current_action = ""
        else:
            first_rune = self.current_spell[0]
            if first_rune.get_element() == "F" or first_rune.get_element() == "A":
                self.current_action = "attack"
            if first_rune.get_element() == "I" or first_rune.get_element() == "E":
                self.current_action = "defend"

    def change_current_health(self, amount):
        self.current_health += amount

    def change_max_health(self, amount):
        self.max_health += amount

    def change_current_gold(self, amount):
        self.current_gold += amount

    """
    def draw_hand(self, player_element_pool, player_power_pool):
        num_runes_needed = self.max_hand - len(self.current_hand)
        count = 0
        while count < num_runes_needed:
            new_rune = make_rune(player_element_pool, player_power_pool)
            self.current_hand.append(new_rune)
            count += 1

    """

    def remove_spell_from_hand(self):
        for rune in self.current_spell:
            if (rune in self.current_hand):
                self.current_hand.remove(rune)

    def has_valid_current_spell(self):
        if not self.current_spell:
            return False
        hand_temp = self.current_hand.copy()
        for rune in self.current_spell:
            if (rune in hand_temp):
                hand_temp.remove(rune)
            else:
                return False
        for i in range(1, len(self.current_spell)):
            previous_rune = self.current_spell[i - 1]
            current_rune = self.current_spell[i]
            if abs(previous_rune.get_power() - current_rune.get_power()) != 1:
                return False
        return True

    def cast_spell(self):
        if self.has_valid_current_spell():
            self.set_current_action()
            self.set_current_power()
            self.remove_spell_from_hand()
        else:
            self.set_current_spell([])

    def is_dead(self):
        return self.current_health <= 0