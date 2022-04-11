from Species import Species
def choose_enemy_species_pool(biome):
    if biome == "Desert":
        return [[Species("Meerkat"), 0.6],
                [Species("Bullfrog"), 0.0],
                [Species("Bat"), 0.2],
                [Species("Rat"), 0.0],
                [Species("Spider"), 0.2]]
    if biome == "Cave":
        return [[Species("Meerkat"), 0.0],
                [Species("Bullfrog"), 0.0],
                [Species("Bat"), 0.6],
                [Species("Rat"), 0.2],
                [Species("Spider"), 0.2]]
    if biome == "Swamp":
        return [[Species("Meerkat"), 0.0],
                [Species("Bullfrog"), 0.6],
                [Species("Bat"), 0.2],
                [Species("Rat"), 0.2],
                [Species("Spider"), 0.0]]
    if biome == "Forest":
        return [[Species("Meerkat"), 0.0],
                [Species("Bullfrog"), 0.1],
                [Species("Bat"), 0.1],
                [Species("Rat"), 0.2],
                [Species("Spider"), 0.6]]
    if biome == "Grassland":
        return [[Species("Meerkat"), 0.2],
                [Species("Bullfrog"), 0.0],
                [Species("Bat"), 0.1],
                [Species("Rat"), 0.6],
                [Species("Spider"), 0.1]]
    else:
        return [[Species("Meerkat"), 0.2],
                [Species("Bullfrog"), 0.2],
                [Species("Bat"), 0.2],
                [Species("Rat"), 0.2],
                [Species("Spider"), 0.2]]

def choose_enemy_level_pool(area_num):
    if area_num == 1:
        return [[0, 0.75],
                [1, 0.25],
                [2, 0.00],
                [3, 0.00]]
    if area_num == 2:
        return [[0, 0.25],
                [1, 0.75],
                [2, 0.00],
                [3, 0.00]]
    if area_num == 3:
        return [[0, 0.00],
                [1, 0.25],
                [2, 0.75],
                [3, 0.00]]
    if area_num == 4:
        return [[0, 0.00],
                [1, 0.00],
                [2, 0.75],
                [3, 0.25]]
    if area_num >= 5:
        return [[0, 0.00],
                [1, 0.00],
                [2, 0.25],
                [3, 0.75]]

class Area:
    def __init__(self, num, biome):
        self.num = num
        self.biome = biome
        self.encounter_num = 0
        self.encounters = []
        self.enemy_species_pool = choose_enemy_species_pool(biome)
        self.enemy_level_pool = choose_enemy_level_pool(num)





