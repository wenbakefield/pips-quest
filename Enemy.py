from Species import Species

class Enemy:
    def __init__(self, level, species, trait, health):
        self.level = level
        self.species = species
        self.trait = trait
        self.health = health
    def __repr__(self):
        return "<Enemy |Level:%s |Species:%s |Trait:%s |Health:%s >" % (self.level,
                                                                          self.species, 
                                                                          self.trait, 
                                                                          self.health)
    def __str__(self):
        return "%s %s (Level: %s | Health: %s)" % (self.trait, 
                                                   self.species, 
                                                   self.level + 1,
                                                   self.get_health())
    def __eq__(self, other):
        if isinstance(other, Enemy):
            return self.level == other.level and self.species == other.species and self.trait == other.trait and self.health == other.health

    def get_level(self):
        return self.level

    def get_species(self):
        return self.species

    def get_trait(self):
        return self.trait

    def get_health(self):
        return sum(self.health) + self.species.get_health_mod(self.level) + self.trait.get_health_mod()

    def get_attack(self):
        return self.species.get_attack_mod(self.level) + self.trait.get_attack_mod()

    def get_defense(self):
        return self.species.get_defense_mod(self.level) + self.trait.get_defense_mod()

    def get_action_pool(self):
        return self.species.get_action_pool()

    def get_gold_drop(self):
        return self.species.get_gold_drop(self.level)

    def get_name(self):
        return self.trait.get_name() + " " + self.species.get_name()

