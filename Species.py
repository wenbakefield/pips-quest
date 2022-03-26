class Species:
    def __init__(self, name):
        self.name = name
        self.attack_mod = []
        self.defense_mod = []
        self.health_mod = []
        self.action_pool = []
        self.special = []
        self.gold_drop = []

        if name == "Meerkat":
            self.attack_mod = [0, 1, 2, 3]
            self.defense_mod = [0, 1, 2, 3]
            self.health_mod = [2, 3, 4, 5]
            self.action_pool = [["attack", 0.5], ["defend", 0.5]]
            self.special = []
            self.gold_drop = [3, 4, 5, 6]

        if name == "Bullfrog":
            self.attack_mod = [0, 0, 1, 2]
            self.defense_mod = [2, 3, 4, 5]
            self.health_mod = [0, 1, 2, 4]
            self.action_pool = [["attack", 0.3], ["defend", 0.7]]
            self.special = []
            self.gold_drop = [1, 2, 3, 4]

        if name == "Bat":
            self.attack_mod = [0, 1, 1, 2]
            self.defense_mod = [0, 1, 1, 1]
            self.health_mod = [2, 3, 4, 5]
            self.action_pool = [["attack", 1.0], ["defend", 0.0]]
            self.special = [0.5, 0.75, 0.5, 0.75]
            self.gold_drop = [1, 2, 3, 3]

        if name == "Rat":
            self.attack_mod = [2, 3, 4, 5]
            self.defense_mod = [0, 1, 2, 4]
            self.health_mod = [0, 1, 1, 2]
            self.action_pool = [["attack", 0.7], ["defend", 0.3]]
            self.special = []
            self.gold_drop = [2, 3, 4, 5]

        if name == "Spider":
            self.attack_mod = [1, 1, 2, 2]
            self.defense_mod = [0, 1, 1, 2]
            self.health_mod = [1, 2, 3, 4]
            self.action_pool = [["attack", 0.2], ["defend", 0.8]]
            self.special = [1, 1, 2, 2]
            self.gold_drop = [1, 2, 2, 3]

    def __repr__(self):
        return "<Species |Name:%s |Attack Mod:%s |Defense Mod:%s |Health Mod:%s |Attack Rate:%s |Block Rate:%s |Special:%s |Gold Drop:%s >" % (self.name, self.attack_mod, self.defense_mod, self.health_mod, self.attack_rate, self.block_rate, self.special, self.gold_drop)
    def __str__(self):
        return "%s" % (self.name)
    def __eq__(self, other):
        if isinstance(other, Species):
            return self.name == other.name and self.attack_mod == other.attack_mod and self.defense_mod == other.defense_mod and self.health_mod == other.health_mod and self.attack_rate == other.attack_rate and self.block_rate == other.block_rate and self.special == other.special and self.gold_drop == other.gold_drop

    def get_name(self):
        return self.name

    def get_attack_mod(self, level):
        return self.attack_mod[level]

    def get_defense_mod(self, level):
        return self.defense_mod[level]

    def get_health_mod(self, level):
        return self.health_mod[level]

    def get_action_pool(self):
        return self.action_pool

    def get_special(self, level):
        return self.special[level]

    def get_gold_drop(self, level):
        return self.gold_drop[level]