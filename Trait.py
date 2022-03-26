class Trait:
    def __init__(self, name):
        self.name = name
        self.attack_mod = 0
        self.defense_mod = 0
        self.health_mod = 0

        if name == "Reserved":
            self.attack_mod = -1
            self.defense_mod = 2
            self.health_mod = 0
        if name == "Brave":
            self.attack_mod = 1
            self.defense_mod = 0
            self.health_mod = -1
        if name == "Reckless":
            self.attack_mod = 2
            self.defense_mod = 0
            self.health_mod = -1
        if name == "Cocky":
            self.attack_mod = 0
            self.defense_mod = -2
            self.health_mod = 0
        if name == "Buff":
            self.attack_mod = 1
            self.defense_mod = 1
            self.health_mod = 2
        if name == "Cheerful":
            self.attack_mod = 0
            self.defense_mod = 0
            self.health_mod = 0
        if name == "Lonely":
            self.attack_mod = -1
            self.defense_mod = -1
            self.health_mod = 0
        if name == "Desperate":
            self.attack_mod = 2
            self.defense_mod = 0
            self.health_mod = -2
        if name == "Weird":
            self.attack_mod = 0
            self.defense_mod = 0
            self.health_mod = 0
        if name == "Aloof":
            self.attack_mod = -1
            self.defense_mod = 0
            self.health_mod = 1

    def __repr__(self):
        return "<Trait |Name:%s |Attack Mod:%s |Defense Mod:%s |Health Mod:%s >" % (self.name, self.attack_mod, self.defense_mod, self.health_mod)
    def __str__(self):
        return "%s" % (self.name)
    def __eq__(self, other):
        if isinstance(other, Trait):
            return self.name == other.name and self.attack_mod == other.attack_mod and self.defense_mod == other.defense_mod and self.health_mod == other.health_mod

    def get_attack_mod(self):
        return self.attack_mod

    def get_defense_mod(self):
        return self.defense_mod

    def get_health_mod(self):
        return self.health_mod

    def get_score(self):
        return self.attack_mod + self.defense_mod + self.health_mod

    def get_name(self):
        return self.name