from Species import Species
import random

class Enemy:
    def __init__(self, level, species, trait, max_health, current_health, base_attack, base_defense, current_power, current_action, gold):
        self.level = level
        self.species = species
        self.trait = trait
        self.max_health = max_health
        self.current_health = current_health
        self.base_attack = base_attack
        self.base_defense = base_defense
        self.current_power = current_power
        self.current_action = current_action
        self.gold = gold

    def __repr__(self):
        return "<Enemy |Level:%s |Species:%s |Trait:%s |Max Health:%s |Current Health:%s |Base Attack:%s |Base Defense:%s |Current Power:%s |Current Action:%s |Gold:%s >" % (self.level,
                                                                          self.species, 
                                                                          self.trait, 
                                                                          self.max_health,
                                                                          self.current_health,
                                                                          self.base_attack,
                                                                          self.base_defense,
                                                                          self.current_power,
                                                                          self.current_action,
                                                                          self.gold)
    def __str__(self):
        return "%s %s (Level: %s)" % (self.trait, 
                                        self.species, 
                                        self.level)

    
    
    def get_level(self):
        return self.level

    def get_species(self):
        return self.species

    def get_trait(self):
        return self.trait

    def get_max_health(self):
        return self.max_health

    def get_current_health(self):
        return self.current_health

    def get_base_attack(self):
        return self.base_attack

    def get_base_defense(self):
        return self.base_defense

    def get_current_power(self):
        return self.current_power

    def get_current_action(self):
        return self.current_action

    def get_gold(self):
        return self.gold

    def get_action_pool(self):
        return self.species.get_action_pool()

    def set_current_health(self, health):
        self.current_health = health

    def set_current_power(self, power):
        self.current_power = power

    def set_current_action(self, action):
        self.current_action = action

    def change_current_health(self, amount):
        self.current_health += amount

    def choose_action(self):
        pool = self.get_action_pool()
        sample_list, weight_list = zip(*pool)
        choice = random.choices(sample_list, weight_list, k = 1)
        result = choice[0]
        self.set_current_action(result)

    def is_dead(self):
        return self.current_health <= 0

    def print_name(self):
        return self.trait.get_name() + " " + self.species.get_name()

    def print_stats(self):
        return "Level: " + str(self.level) + " | Health: " + str(self.current_health) + " | Intent: " + str(self.current_action)