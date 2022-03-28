class Trait:
    def __init__(self, name, attack_mod, defense_mod, health_mod):
        self.name = name
        self.attack_mod = attack_mod
        self.defense_mod = defense_mod
        self.health_mod = health_mod

    def __repr__(self):
        return "<Trait |Name:%s |Attack Mod:%s |Defense Mod:%s |Health Mod:%s >" % (self.name, self.attack_mod, self.defense_mod, self.health_mod)
    def __str__(self):
        return "%s" % (self.name)
    def __eq__(self, other):
        if isinstance(other, Trait):
            return self.name == other.name and self.attack_mod == other.attack_mod and self.defense_mod == other.defense_mod and self.health_mod == other.health_mod

    def get_name(self):
        return self.name

    def get_attack_mod(self):
        return self.attack_mod

    def get_defense_mod(self):
        return self.defense_mod

    def get_health_mod(self):
        return self.health_mod

    def get_score(self):
        return self.attack_mod + self.defense_mod + self.health_mod