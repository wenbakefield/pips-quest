import random

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

    def set_current_power(self, power):
        self.current_power = power

    def set_current_action(self, action):
        self.current_action = action

    def change_current_health(self, amount):
        self.current_health += amount

    def change_max_health(self, amount):
        self.max_health += amount

    def change_current_gold(self, amount):
        self.current_gold += amount

    def choose_from(self, pool):
        r, s = random.random(), 0
        for item in pool:
            s += item[1]
            if s >= r:
                return item[0]

    def draw_hand(self, player_power_pool):
        num_cards_needed = self.max_hand - len(self.current_hand)
        count = 0
        while count < num_cards_needed:
            new_card = self.choose_from(player_power_pool)
            self.current_hand.append(new_card)
            count += 1

    def remove_spell_from_hand(self):
        for card in self.current_spell:
            if (card in self.current_hand):
                self.current_hand.remove(card)

    def has_valid_current_spell(self):
        if not self.current_spell:
            return False
        hand_temp = self.current_hand.copy()
        for card in self.current_spell:
            if (card in hand_temp):
                hand_temp.remove(card)
            else:
                return False
        for i in range(1, len(self.current_spell)):
            if abs(self.current_spell[i - 1] - self.current_spell[i]) != 1:
                return False
        return True

    def cast_spell(self, player_power_pool):
        if self.has_valid_current_spell():
            self.set_current_power(sum(self.current_spell))
            self.remove_spell_from_hand()
            self.draw_hand(player_power_pool)
        else:
            self.set_current_spell([])

    def is_dead(self):
        return self.current_health <= 0